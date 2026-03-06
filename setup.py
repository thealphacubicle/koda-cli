from setuptools import find_packages, setup

setup(
    name="koda-cli",
    version="1.0.0",
    description="An AI-powered project bootstrapper for developers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="thealphacubicle",
    url="https://github.com/thealphacubicle/koda-cli",
    packages=find_packages(),
    scripts=["koda"],
    install_requires=[
        "anthropic",
        "openai",
        "google-generativeai",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
    ],
)
