#!/usr/bin/env python3
"""Remove retained WordPress draft or released articles from the Astro project.

The ignored WXR backup is deliberately left intact, so a clean import can restore
removed articles later.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "src/content"
MANIFEST = ROOT / "src/data/legacy-routes.json"
WORDPRESS_ID = re.compile(r'^wordpressId:\s+"(?P<id>\d+)"\s*$', re.MULTILINE)


@dataclass(frozen=True)
class Article:
    wordpress_id: str
    status: str
    path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wordpress_ids", metavar="WORDPRESS_ID", nargs="+", help="one or more numeric WordPress post IDs")
    parser.add_argument("--dry-run", action="store_true", help="report the articles that would be removed without changing files")
    return parser.parse_args()


def article_id(path: Path) -> str:
    match = WORDPRESS_ID.search(path.read_text(encoding="utf-8"))
    if match is None:
        raise ValueError(f"missing wordpressId frontmatter: {path.relative_to(ROOT)}")
    return match.group("id")


def retained_articles() -> dict[str, Article]:
    articles: dict[str, Article] = {}
    for directory, status in (("posts", "publish"), ("drafts", "draft")):
        for path in sorted((CONTENT / directory).rglob("index.md")):
            wordpress_id = article_id(path)
            if wordpress_id in articles:
                raise ValueError(f"duplicate WordPress ID {wordpress_id}: {path.relative_to(ROOT)}")
            articles[wordpress_id] = Article(wordpress_id, status, path)
    return articles


def count_content(directory: str) -> int:
    return len(list((CONTENT / directory).rglob("index.md")))


def validate_manifest(manifest: dict[str, object], articles: dict[str, Article]) -> None:
    counts = manifest.get("counts")
    if not isinstance(counts, dict):
        raise ValueError("route manifest has no counts")
    actual = {"posts": count_content("posts"), "drafts": count_content("drafts"), "pages": count_content("pages")}
    expected = {key: counts.get(key) for key in actual}
    if actual != expected:
        raise ValueError(f"content counts do not match route manifest; expected={expected}, actual={actual}")
    routes = manifest.get("routes")
    if not isinstance(routes, list):
        raise ValueError("route manifest has no routes")
    released_paths = {article.path.relative_to(ROOT).as_posix() for article in articles.values() if article.status == "publish"}
    route_paths = {route.get("contentFile") for route in routes if isinstance(route, dict) and route.get("kind") == "post"}
    if released_paths != route_paths:
        raise ValueError("released article files do not match the route manifest")


def remove_articles(articles: list[Article], manifest: dict[str, object], dry_run: bool) -> None:
    if dry_run:
        return
    removed_files = {article.path.relative_to(ROOT).as_posix() for article in articles}
    for article in articles:
        article.path.unlink()
        article.path.parent.rmdir()
    routes = manifest["routes"]
    assert isinstance(routes, list)
    manifest["routes"] = [
        route
        for route in routes
        if not (isinstance(route, dict) and route.get("contentFile") in removed_files)
    ]
    counts = manifest["counts"]
    assert isinstance(counts, dict)
    counts["posts"] = count_content("posts")
    counts["drafts"] = count_content("drafts")
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    if any(not wordpress_id.isdecimal() for wordpress_id in args.wordpress_ids):
        raise SystemExit("WORDPRESS_ID values must be numeric")
    if len(set(args.wordpress_ids)) != len(args.wordpress_ids):
        raise SystemExit("WORDPRESS_ID values must be unique")

    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        articles_by_id = retained_articles()
        validate_manifest(manifest, articles_by_id)
        missing = sorted(set(args.wordpress_ids) - articles_by_id.keys())
        if missing:
            raise ValueError(f"WordPress article IDs not retained in this project: {', '.join(missing)}")
        selected = [articles_by_id[wordpress_id] for wordpress_id in args.wordpress_ids]
        remove_articles(selected, manifest, args.dry_run)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as error:
        print(f"removal failed: {error}")
        return 1

    print(json.dumps({
        "dryRun": args.dry_run,
        "removed": [
            {"wordpressId": article.wordpress_id, "status": article.status, "contentFile": article.path.relative_to(ROOT).as_posix()}
            for article in selected
        ],
        "backupRetained": "backup/wordpress/management.WordPress.2026-08-10.xml",
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
