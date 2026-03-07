#!/usr/bin/env python3
"""Build a static no-JS gallery page from data/works.json."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parent.parent
WORKS_JSON = ROOT / "data" / "works.json"
OUTPUT_HTML = ROOT / "works-noscript.html"


def url_path(value: str) -> str:
    return quote(value, safe="/._-~()+")


def build_page(works: list[dict]) -> str:
    cards = []
    for work in works:
        title = str(work.get("title", "Untitled"))
        alt = str(work.get("alt", title))
        thumb_src = url_path(str(work.get("thumbSrc", "")))
        full_src = url_path(str(work.get("fullSrc", work.get("thumbSrc", ""))))
        width = work.get("width")
        height = work.get("height")

        size_attrs = ""
        if isinstance(width, int) and isinstance(height, int):
            size_attrs = f' width="{width}" height="{height}"'

        cards.append(
            f"""            <div class="work-item">
                <div class="image-placeholder">
                    <a href="{full_src}" class="link">
                        <img src="{thumb_src}" alt="{escape(alt, quote=True)}"{size_attrs} loading="lazy" decoding="async">
                    </a>
                </div>
                <p class="work-title">{escape(title)}</p>
            </div>"""
        )

    cards_html = "\n".join(cards)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jooeun Kim - Works (No JavaScript)</title>
    <link rel="stylesheet" href="css/html5reset.css">
    <link rel="stylesheet" href="css/style.css">
</head>
<body>

    <header>
        <div class="logo">
            <a href="index.html">Jooeun Kim</a>
        </div>
        <nav>
            <ul>
                <li><a href="works-noscript.html" class="active">Works</a></li>
                <li><a href="contact.html">Contact</a></li>
                <li><a href="cv.html">CV</a></li>
                <li class="lang-switch">
                    <a href="#" class="active">Eng</a> / <a href="#">한국어</a>
                </li>
            </ul>
        </nav>
    </header>

    <main>
        <div class="works-grid">
{cards_html}
        </div>
    </main>

    <footer>
        <p>&copy; 2026 Jooeun Kim. All rights reserved.</p>
    </footer>

</body>
</html>
"""


def main() -> int:
    works = json.loads(WORKS_JSON.read_text(encoding="utf-8"))
    if not isinstance(works, list):
        raise ValueError("data/works.json root must be an array")

    OUTPUT_HTML.write_text(build_page(works), encoding="utf-8")
    print(f"Built {OUTPUT_HTML.relative_to(ROOT)} from {WORKS_JSON.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
