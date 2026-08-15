import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://durchsieben.de',
  output: 'static',
  integrations: [
    sitemap({
      filter: (page) => !page.includes('search-index'),
    }),
  ],
});
