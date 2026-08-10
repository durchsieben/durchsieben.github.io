import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = await getCollection('posts');
  return rss({
    title: 'Management÷7',
    description: 'Management-Wissen für die Praxis.',
    site: context.site ?? 'https://durchsieben.de',
    items: posts.map((post) => ({ title: post.data.title, pubDate: new Date(post.data.date), link: post.data.sourcePath })),
  });
}
