import { getCollection, type CollectionEntry } from 'astro:content';

export type PostEntry = CollectionEntry<'posts'>;

export interface PostSummary {
  path: string;
  title: string;
  date: string;
  isoDate: string;
  displayDate: string;
  year: string;
  excerpt: string;
  minutes: number;
  words: number;
  searchText: string;
}

const WORDS_PER_MINUTE = 200;

/** Strip Gutenberg comments, HTML tags, and entities down to readable text. */
export function plainText(body: string): string {
  return body
    .replace(/<!--[\s\S]*?-->/g, ' ')
    .replace(/<(script|style)[\s\S]*?<\/\1>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#0?39;|&#x27;|&apos;/g, "'")
    .replace(/&(?:#\d+|#x[0-9a-f]+|[a-z]+);/gi, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

export function excerptOf(body: string, limit = 220): string {
  const text = plainText(body);
  if (text.length <= limit) return text;
  const cut = text.slice(0, limit);
  const stop = Math.max(cut.lastIndexOf('. '), cut.lastIndexOf(' '));
  return `${cut.slice(0, stop > limit * 0.5 ? stop : limit).replace(/[\s,;:.–-]+$/, '')} …`;
}

const dateFormat = new Intl.DateTimeFormat('de-DE', { day: '2-digit', month: 'long', year: 'numeric' });

/** ISO-8601 date part of the importer's "YYYY-MM-DD HH:MM:SS" value. */
export function isoDateOf(date: string): string {
  return date.slice(0, 10);
}

export function summarize(entry: PostEntry): PostSummary {
  const body = entry.body ?? '';
  const text = plainText(body);
  const words = text ? text.split(' ').length : 0;
  const isoDate = isoDateOf(entry.data.date);
  return {
    path: entry.data.sourcePath,
    title: entry.data.title,
    date: entry.data.date,
    isoDate,
    displayDate: dateFormat.format(new Date(`${isoDate}T00:00:00Z`)),
    year: isoDate.slice(0, 4),
    excerpt: excerptOf(body),
    minutes: Math.max(1, Math.round(words / WORDS_PER_MINUTE)),
    words,
    searchText: `${entry.data.title} ${text}`.toLowerCase(),
  };
}

/** All published posts, newest first. */
export async function newestFirst(): Promise<PostSummary[]> {
  const posts = await getCollection('posts');
  return posts
    .sort((a: PostEntry, b: PostEntry) => b.data.date.localeCompare(a.data.date))
    .map(summarize);
}

const STOPWORDS = new Set([
  'der', 'die', 'das', 'und', 'von', 'mit', 'für', 'fur', 'ein', 'eine', 'zur', 'zum',
  'ist', 'sind', 'des', 'den', 'dem', 'auf', 'im', 'in', 'an', 'am', 'über', 'uber',
  'als', 'aus', 'was', 'wie', 'wer', 'wenn', 'noch', 'sich', 'nicht', 'auch', 'oder',
  'durch', 'bei', 'zum', 'zur', 'ihre', 'ihr', 'ihren', 'einer', 'eines', 'einem',
  'art', 'artikel', 'kommentar', 'kommentare', 'update', 'neu',
]);

/** Suggested topic pills derived from titles. */
export function topics(posts: PostSummary[], limit = 8): { slug: string; label: string; count: number }[] {
  const counts = new Map<string, { label: string; count: number }>();
  for (const post of posts) {
    const words = post.title
      .toLowerCase()
      .replace(/[^\p{L}\p{N}\s-]/gu, ' ')
      .split(/\s+/)
      .filter((word) => word.length > 3 && !STOPWORDS.has(word));
    const seen = new Set<string>();
    for (const word of words) {
      if (seen.has(word)) continue;
      seen.add(word);
      const entry = counts.get(word) ?? { label: word.replace(/^./u, (c) => c.toUpperCase()), count: 0 };
      entry.count += 1;
      counts.set(word, entry);
    }
  }
  return [...counts.entries()]
    .filter(([, info]) => info.count >= 2)
    .sort((a, b) => b[1].count - a[1].count)
    .slice(0, limit)
    .map(([slug, info]) => ({ slug, label: info.label, count: info.count }));
}
