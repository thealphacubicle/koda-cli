// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://thealphacubicle.github.io',
  base: '/koda-cli',
  output: 'static',
  vite: {
    plugins: [tailwindcss()]
  }
});