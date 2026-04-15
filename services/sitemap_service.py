from collections.abc import Iterable
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin
from xml.sax.saxutils import escape

from django.conf import settings

from catalog_app.models import Category, Compilation, Good


DEFAULT_STATIC_PATHS = ["/"]


def _normalize_path(path: str) -> str:
    normalized_path = path.strip()
    if not normalized_path:
        return ""
    if normalized_path.startswith("http://") or normalized_path.startswith("https://"):
        return normalized_path
    if not normalized_path.startswith("/"):
        normalized_path = f"/{normalized_path}"
    return normalized_path


def _build_absolute_url(path: str) -> str:
    normalized_path = _normalize_path(path)
    if not normalized_path:
        return ""
    if normalized_path.startswith("http://") or normalized_path.startswith("https://"):
        return normalized_path
    return urljoin(f"{settings.SITE_URL.rstrip('/')}/", normalized_path.lstrip("/"))


def _format_lastmod(value: datetime | None) -> str:
    if value is None:
        return ""
    return value.date().isoformat()


def _append_entry(
    entries: list[dict[str, str]],
    *,
    loc: str,
    lastmod: datetime | None,
    changefreq: str,
    priority: str,
) -> None:
    absolute_url = _build_absolute_url(loc)
    if not absolute_url:
        return
    entries.append(
        {
            "loc": absolute_url,
            "lastmod": _format_lastmod(lastmod),
            "changefreq": changefreq,
            "priority": priority,
        }
    )


def build_sitemap_entries(static_paths: Iterable[str] | None = None) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    merged_static_paths = list(DEFAULT_STATIC_PATHS)
    merged_static_paths.extend(settings.SITEMAP_STATIC_PATHS)
    if static_paths:
        merged_static_paths.extend(static_paths)

    seen_static_paths: set[str] = set()
    for path in merged_static_paths:
        normalized_path = _normalize_path(path)
        if not normalized_path or normalized_path in seen_static_paths:
            continue
        seen_static_paths.add(normalized_path)
        _append_entry(
            entries,
            loc=normalized_path,
            lastmod=None,
            changefreq="weekly",
            priority="1.0" if normalized_path == "/" else "0.8",
        )

    categories = Category.active_objects.exclude(slug="")
    for category in categories.iterator():
        _append_entry(
            entries,
            loc=category.get_absolute_url(),
            lastmod=category.updated_at,
            changefreq="weekly",
            priority="0.9",
        )

    compilations = Compilation.active_objects.exclude(slug="")
    for compilation in compilations.iterator():
        _append_entry(
            entries,
            loc=compilation.get_absolute_url(),
            lastmod=compilation.updated_at,
            changefreq="weekly",
            priority="0.8",
        )

    goods = Good.active_objects.exclude(slug="")
    for good in goods.iterator():
        _append_entry(
            entries,
            loc=good.get_absolute_url(),
            lastmod=good.updated_at,
            changefreq="weekly",
            priority="0.7",
        )

    entries.sort(key=lambda item: item["loc"])
    return entries


def render_sitemap_xml(entries: Iterable[dict[str, str]]) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for entry in entries:
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(entry['loc'])}</loc>")
        if entry.get("lastmod"):
            lines.append(f"    <lastmod>{entry['lastmod']}</lastmod>")
        if entry.get("changefreq"):
            lines.append(f"    <changefreq>{entry['changefreq']}</changefreq>")
        if entry.get("priority"):
            lines.append(f"    <priority>{entry['priority']}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def build_sitemap_xml(static_paths: Iterable[str] | None = None) -> str:
    entries = build_sitemap_entries(static_paths=static_paths)
    return render_sitemap_xml(entries)


def save_sitemap_file(xml_content: str) -> Path:
    settings.SITEMAP_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    settings.SITEMAP_FILE_PATH.write_text(xml_content, encoding="utf-8")
    return settings.SITEMAP_FILE_PATH
