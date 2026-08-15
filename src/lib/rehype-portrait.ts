const PNG = '/images/raphael-bossek-portrait.png';
const SRCSET = (ext: string) =>
  `/images/portrait/raphael-bossek-640.${ext} 640w, /images/portrait/raphael-bossek-960.${ext} 960w`;
const SIZES = 'min(13rem, 58vw)';

/** Replace the importer PNG with sized AVIF/WebP. Does not edit Markdown. */
export function rewritePortraitHtml(html: string): string {
  return html.replace(
    /<img\b([^>]*?)\bsrc="\/images\/raphael-bossek-portrait\.png"([^>]*)\/?>/gi,
    (_match, before: string, after: string) => {
      const alt = /\balt="([^"]*)"/.exec(`${before} ${after}`)?.[1] ?? '';
      return (
        `<picture class="about-portrait">` +
        `<source type="image/avif" srcset="${SRCSET('avif')}" sizes="${SIZES}" />` +
        `<source type="image/webp" srcset="${SRCSET('webp')}" sizes="${SIZES}" />` +
        `<img src="/images/portrait/raphael-bossek-640.webp" alt="${alt}" width="640" height="823" decoding="async" />` +
        `</picture>`
      );
    },
  );
}

export const PORTRAIT_PNG = PNG;
