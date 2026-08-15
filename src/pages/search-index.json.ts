import { newestFirst } from '../lib/posts';

export async function GET() {
  const posts = await newestFirst();
  const payload = posts.map(({ words: _words, date: _date, ...rest }) => rest);
  return new Response(JSON.stringify(payload), {
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'public, max-age=300',
    },
  });
}
