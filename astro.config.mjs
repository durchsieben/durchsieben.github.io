import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://durchsieben.de',
  output: 'static',
  build: {
    // Global CSS is small (~15 KB). Inlining removes the render-blocking
    // /_astro/*.css hop on first paint (GitHub Pages has no HTTP/2 push).
    inlineStylesheets: 'always',
  },
  integrations: [
    sitemap({
      filter: (page) => !page.includes('search-index'),
    }),
  ],
});
