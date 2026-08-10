#!/usr/bin/env python3
"""Verify imported content, preserved routes, and local links in Astro's static output."""

from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
MANIFEST = ROOT / "src/data/legacy-routes.json"


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.hrefs.append(value)


def public_path(output: Path) -> str:
    relative = output.relative_to(DIST)
    if relative == Path("index.html"):
        return "/"
    return f"/{relative.parent.as_posix()}/"


def output_for(path: str) -> Path:
    normalized = unquote(path)
    return DIST / "index.html" if normalized == "/" else DIST / normalized.strip("/") / "index.html"


def local_target(path: str) -> Path:
    normalized = unquote(path)
    if normalized == "/":
        return DIST / "index.html"
    if normalized.endswith("/") or "." not in Path(normalized).name:
        return DIST / normalized.strip("/") / "index.html"
    return DIST / normalized.strip("/")


def main() -> int:
    if not DIST.is_dir():
        raise SystemExit("dist/ is missing; run pnpm build first")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected_counts = {"posts": 109, "pages": 3, "media": 78}
    if manifest["counts"] != expected_counts:
        raise SystemExit(f"unexpected import counts: {manifest['counts']}")

    routes = manifest["routes"]
    source_paths = {route["sourcePath"] for route in routes}
    if len(routes) != 113 or len(source_paths) != 113:
        raise SystemExit("expected exactly 113 unique legacy routes")

    missing_routes = [path for path in sorted(source_paths) if not output_for(path).is_file()]
    missing_content = [route["contentFile"] for route in routes if not (ROOT / route["contentFile"]).is_file()]
    media = [path for path in (ROOT / "public/media").rglob("*") if path.is_file()]
    if missing_routes or missing_content or len(media) != expected_counts["media"]:
        raise SystemExit(json.dumps({"missingRoutes": missing_routes, "missingContent": missing_content, "media": len(media)}, ensure_ascii=False))

    broken: list[tuple[str, str]] = []
    for page in DIST.rglob("*.html"):
        parser = Links()
        parser.feed(page.read_text(encoding="utf-8"))
        base = f"https://durchsieben.de{public_path(page)}"
        for href in parser.hrefs:
            if href.startswith(("#", "mailto:", "tel:", "data:")):
                continue
            parsed = urlparse(href)
            if parsed.netloc and parsed.netloc not in {"durchsieben.de", "www.durchsieben.de"}:
                continue
            target_path = urlparse(urljoin(base, href)).path or "/"
            if not local_target(target_path).is_file():
                broken.append((public_path(page), href))
    if broken:
        raise SystemExit(json.dumps({"brokenLocalLinks": broken}, ensure_ascii=False))

    print(json.dumps({"routes": len(routes), "posts": 109, "pages": 3, "media": len(media), "localLinks": "PASS"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
