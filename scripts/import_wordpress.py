#!/usr/bin/env python3
"""Import a WordPress WXR backup into Astro-ready content and media assets."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from html import unescape
from pathlib import Path, PurePosixPath
from shutil import copyfileobj
from typing import Iterable
from urllib.parse import unquote, urlparse
import re
import tarfile
import xml.etree.ElementTree as ET

NAMESPACES = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "wp": "http://wordpress.org/export/1.2/",
}
MEDIA_URL_PATTERN = re.compile(r"https?://durchsieben\.de/wp-content/uploads/[^\"'<>\s)]+")


@dataclass(frozen=True)
class Attachment:
    source_url: str
    archive_path: str
    public_url: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backup", type=Path, default=Path("backup/wordpress"))
    parser.add_argument("--content", type=Path, default=Path("src/content"))
    parser.add_argument("--media", type=Path, default=Path("public/media"))
    parser.add_argument("--routes", type=Path, default=Path("src/data/legacy-routes.json"))
    parser.add_argument("--sitemap-routes", type=Path)
    return parser.parse_args()


def text(item: ET.Element, selector: str, *, namespace: str | None = None) -> str:
    namespaces = NAMESPACES if namespace else None
    return (item.findtext(selector, default="", namespaces=namespaces) or "").strip()


def relative_upload_path(url: str) -> str:
    path = unquote(urlparse(url).path)
    marker = "/wp-content/uploads/"
    if marker not in path:
        raise ValueError(f"attachment is outside wp-content/uploads: {url}")
    relative = path.split(marker, 1)[1]
    pure_path = PurePosixPath(relative)
    if pure_path.is_absolute() or ".." in pure_path.parts or not relative:
        raise ValueError(f"unsafe attachment path: {url}")
    return pure_path.as_posix()


def extract_media(archive_path: Path, target: Path) -> dict[str, str]:
    if target.exists():
        raise FileExistsError(f"media output already exists: {target}")
    target.mkdir(parents=True)
    extracted: dict[str, str] = {}
    with tarfile.open(archive_path, "r") as archive:
        for member in archive.getmembers():
            if not member.isfile():
                continue
            relative = PurePosixPath(member.name)
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError(f"unsafe archive member: {member.name}")
            destination = target.joinpath(*relative.parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            source = archive.extractfile(member)
            if source is None:
                raise ValueError(f"cannot extract archive member: {member.name}")
            with source, destination.open("xb") as output:
                copyfileobj(source, output)
            extracted[relative.as_posix()] = f"/media/{relative.as_posix()}"
    return extracted


def archived_media(archive_path: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    with tarfile.open(archive_path, "r") as archive:
        for member in archive.getmembers():
            if not member.isfile():
                continue
            relative = PurePosixPath(member.name)
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError(f"unsafe archive member: {member.name}")
            files[relative.as_posix()] = f"/media/{relative.as_posix()}"
    return files


def attachment_map(root: ET.Element, media: dict[str, str]) -> dict[str, Attachment]:
    attachments: dict[str, Attachment] = {}
    for item in root.findall("./channel/item"):
        if text(item, "wp:post_type", namespace="wp") != "attachment":
            continue
        source_url = text(item, "wp:attachment_url", namespace="wp")
        if not source_url:
            continue
        archive_path = relative_upload_path(source_url)
        try:
            public_url = media[archive_path]
        except KeyError as exc:
            raise ValueError(f"attachment missing from media export: {source_url}") from exc
        attachments[source_url] = Attachment(source_url, archive_path, public_url)
    if len(attachments) != len(media):
        raise ValueError(
            f"WXR/media mismatch: {len(attachments)} WXR attachments, {len(media)} media files"
        )
    return attachments


def rewrite_media(content: str, attachments: dict[str, Attachment]) -> tuple[str, list[str]]:
    unresolved: list[str] = []

    def replace(match: re.Match[str]) -> str:
        source_url = match.group(0)
        parsed = urlparse(source_url)
        canonical_url = f"https://durchsieben.de{parsed.path}"
        attachment = attachments.get(canonical_url)
        if attachment is None:
            unresolved.append(source_url)
            return source_url
        return attachment.public_url

    rewritten = MEDIA_URL_PATTERN.sub(replace, unescape(content))
    return "\n".join(line.rstrip() for line in rewritten.splitlines()), unresolved


def source_path(item: ET.Element) -> str:
    value = text(item, "link")
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or parsed.netloc != "durchsieben.de":
        raise ValueError(f"unsupported source URL: {value}")
    return parsed.path or "/"


def content_path(root: Path, kind: str, route: str) -> Path:
    parts = [unquote(segment) for segment in route.strip("/").split("/") if segment]
    if not parts:
        parts = ["index"]
    if any(part in {".", ".."} for part in parts):
        raise ValueError(f"unsafe route: {route}")
    return root / kind / Path(*parts) / "index.md"


def frontmatter(record: dict[str, str]) -> str:
    lines = ["---"]
    lines.extend(f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in record.items())
    lines.append("---")
    return "\n".join(lines)


def published_items(root: ET.Element) -> Iterable[ET.Element]:
    for item in root.findall("./channel/item"):
        kind = text(item, "wp:post_type", namespace="wp")
        status = text(item, "wp:status", namespace="wp")
        if kind in {"post", "page"} and status == "publish":
            yield item


def run(args: argparse.Namespace) -> dict[str, object]:
    wxr = args.backup / "management.WordPress.2026-08-10.xml"
    media_archive = args.backup / "media-export-4925442-from-0-to-2313.tar"
    sitemap_routes_path = args.sitemap_routes or args.backup / "sitemap-route-seed.json"
    if not wxr.is_file() or not media_archive.is_file() or not sitemap_routes_path.is_file():
        raise FileNotFoundError("expected WXR, media archive, and sitemap route seed")
    if args.content.exists() or args.routes.exists():
        raise FileExistsError("content or route output already exists; import into a clean checkout")

    root = ET.parse(wxr).getroot()
    media = archived_media(media_archive)
    attachments = attachment_map(root, media)
    sitemap_routes = json.loads(sitemap_routes_path.read_text(encoding="utf-8"))
    expected_paths = {route["path"] for route in sitemap_routes["routes"]}
    imported_paths = {source_path(item) for item in published_items(root)} | {"/"}
    if expected_paths != imported_paths:
        missing = sorted(expected_paths - imported_paths)
        unexpected = sorted(imported_paths - expected_paths)
        raise ValueError(f"WXR/sitemap route mismatch; missing={missing}, unexpected={unexpected}")
    unresolved_media = {
        url
        for item in published_items(root)
        for url in rewrite_media(text(item, "content:encoded", namespace="content"), attachments)[1]
    }
    if unresolved_media:
        raise ValueError("unresolved WordPress media URLs: " + ", ".join(sorted(unresolved_media)))
    extracted_media = extract_media(media_archive, args.media)
    if extracted_media != media:
        raise ValueError("media archive changed between validation and extraction")
    args.content.mkdir(parents=True)
    routes: list[dict[str, str]] = [{"sourcePath": "/", "contentFile": "src/pages/index.astro", "kind": "homepage"}]
    counts = {"post": 0, "page": 0}

    for item in published_items(root):
        kind = text(item, "wp:post_type", namespace="wp")
        route = source_path(item)
        content, _ = rewrite_media(text(item, "content:encoded", namespace="content"), attachments)
        destination = content_path(args.content, f"{kind}s", route)
        destination.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "title": text(item, "title"),
            "date": text(item, "wp:post_date", namespace="wp"),
            "sourcePath": route,
            "sourceUrl": text(item, "link"),
            "wordpressId": text(item, "wp:post_id", namespace="wp"),
        }
        destination.write_text(frontmatter(record) + "\n" + content.rstrip() + "\n", encoding="utf-8")
        routes.append({"sourcePath": route, "contentFile": destination.as_posix(), "kind": kind})
        counts[kind] += 1

    args.routes.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "source": {
            "wxr": {"file": wxr.name, "sha256": hashlib.sha256(wxr.read_bytes()).hexdigest()},
            "mediaArchive": {
                "file": media_archive.name,
                "sha256": hashlib.sha256(media_archive.read_bytes()).hexdigest(),
            },
            "sitemapRoutes": {
                "file": sitemap_routes_path.name,
                "sha256": hashlib.sha256(sitemap_routes_path.read_bytes()).hexdigest(),
            },
        },
        "counts": {"posts": counts["post"], "pages": counts["page"], "media": len(media)},
        "routes": sorted(routes, key=lambda route: route["sourcePath"]),
        "media": [
            {"sourceUrl": attachment.source_url, "archivePath": attachment.archive_path, "publicUrl": attachment.public_url}
            for attachment in sorted(attachments.values(), key=lambda attachment: attachment.source_url)
        ],
    }
    args.routes.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest["counts"]


def main() -> int:
    args = parse_args()
    try:
        counts = run(args)
    except (ET.ParseError, FileNotFoundError, FileExistsError, ValueError, tarfile.TarError) as error:
        print(f"import failed: {error}")
        return 1
    print(json.dumps(counts, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
