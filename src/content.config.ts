import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const entrySchema = z.object({
  title: z.string(),
  date: z.string(),
  sourcePath: z.string(),
  sourceUrl: z.string().url(),
  wordpressId: z.string(),
});

export const collections = {
  posts: defineCollection({
    loader: glob({ base: './src/content/posts', pattern: '**/*.md' }),
    schema: entrySchema,
  }),
  pages: defineCollection({
    loader: glob({ base: './src/content/pages', pattern: '**/*.md' }),
    schema: entrySchema,
  }),
};
