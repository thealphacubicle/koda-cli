"""Provider-agnostic AI wrapper for koda CLI."""

from __future__ import annotations

import json
import os
import sys
import time

CONFIG_PATH = os.path.expanduser("~/.koda/config.json")
CONFIG_KEYS = {
    "claude": "anthropic",
    "openai": "openai",
    "gemini": "google",
}


def _ensure_config_dir():
    """Create ~/.koda/ if it doesn't exist."""
    config_dir = os.path.dirname(CONFIG_PATH)
    os.makedirs(config_dir, exist_ok=True)


def _load_config() -> dict:
    """Load config from ~/.koda/config.json."""
    _ensure_config_dir()
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}


def _save_config(config: dict) -> None:
    """Save config to ~/.koda/config.json."""
    _ensure_config_dir()
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)


def _get_key(provider: str) -> str | None:
    """Get API key for provider. Prompts if missing and saves to config."""
    config = _load_config()
    key_name = CONFIG_KEYS.get(provider, provider)
    key = config.get(key_name)

    if not key:
        key = input(f"Enter {key_name} API key: ").strip()
        if key:
            config[key_name] = key
            _save_config(config)
    return key or None


def ask_ai(prompt: str, provider: str) -> str:
    """Call AI provider with prompt, stream response char-by-char. Returns full response."""
    provider_lower = provider.lower()
    if provider_lower == "claude":
        return _ask_claude(prompt)
    if provider_lower == "openai":
        return _ask_openai(prompt)
    if provider_lower == "gemini":
        return _ask_gemini(prompt)
    raise ValueError(f"Unknown provider: {provider}")


def _ask_claude(prompt: str) -> str:
    """Stream response from Claude."""
    key = _get_key("claude")
    if not key:
        raise ValueError("Anthropic API key not found. Run 'koda config' to set it.")

    import anthropic

    client = anthropic.Anthropic(api_key=key)
    full_text = []

    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            full_text.append(text)
            for char in text:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.01)

    sys.stdout.write("\n")
    sys.stdout.flush()
    return "".join(full_text)


def _ask_openai(prompt: str) -> str:
    """Stream response from OpenAI."""
    key = _get_key("openai")
    if not key:
        raise ValueError("OpenAI API key not found. Run 'koda config' to set it.")

    from openai import OpenAI

    client = OpenAI(api_key=key)
    full_text = []

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            text = chunk.choices[0].delta.content
            full_text.append(text)
            for char in text:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.01)

    sys.stdout.write("\n")
    sys.stdout.flush()
    return "".join(full_text)


def _ask_gemini(prompt: str) -> str:
    """Stream response from Gemini."""
    key = _get_key("gemini")
    if not key:
        raise ValueError("Google API key not found. Run 'koda config' to set it.")

    import google.generativeai as genai

    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-1.5-pro")
    full_text = []

    response = model.generate_content(prompt, stream=True)

    for chunk in response:
        if chunk.text:
            full_text.append(chunk.text)
            for char in chunk.text:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.01)

    sys.stdout.write("\n")
    sys.stdout.flush()
    return "".join(full_text)
