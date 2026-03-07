#!/usr/bin/env python3
"""Create a new artwork detail page and append its card to index.html."""

from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "index.html"
DETAIL_DIR = ROOT / "html"


def get_dimensions(image_path: Path) -> tuple[int, int] | None:
    """Read image dimensions via macOS sips."""
    try:
        result = subprocess.run(
            ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(image_path)],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

    width = None
    height = None
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("pixelWidth:"):
            width = line.split(":", 1)[1].strip()
        if line.startswith("pixelHeight:"):
            height = line.split(":", 1)[1].strip()

    if width and height and width.isdigit() and height.isdigit():
        return int(width), int(height)
    return None


def build_detail_html(
    page_title: str,
    image_src: str,
    alt_text: str,
    width: int | None,
    height: int | None,
    media_lines: list[str],
) -> str:
    escaped_page_title = html.escape(page_title, quote=True)
    escaped_alt = html.escape(alt_text, quote=True)
    media_block = "<br>\n                   ".join(
        html.escape(line, quote=False) for line in media_lines
    )

    size_attrs = ""
    if width and height:
        size_attrs = f' width="{width}" height="{height}"'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jooeun Kim - Works</title>
    <link rel="stylesheet" href="../css/html5reset.css">
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>

    <header>
        <div class="logo">
            <a href="../index.html">Jooeun Kim</a>
        </div>
        <nav>
            <ul>
                <li><a href="../index.html" class="active">Works</a></li>
                <li><a href="../contact.html">Contact</a></li>
                <li><a href="../cv.html">CV</a></li>
                <li class="lang-switch">
                    <a href="#" class="active">Eng</a> / <a href="#">한국어</a>
                </li>
            </ul>
        </nav>
    </header>

    <main>
        <div>
            <img src="../{image_src}" alt="{escaped_alt}" class="work-expanded"{size_attrs}>
            <div id='media_info'>
                &nbsp;
                <p>{media_block}</p>
            </div>
        </div>
    </main>

    <footer>
        <p>&copy; 2026 Jooeun Kim. All rights reserved.</p>
    </footer>

</body>
</html>
"""


def build_index_card(
    detail_page_name: str,
    image_src: str,
    alt_text: str,
    width: int | None,
    height: int | None,
) -> str:
    escaped_alt = html.escape(alt_text, quote=True)
    size_attrs = ""
    if width and height:
        size_attrs = f' width="{width}" height="{height}"'

    return f"""            <div class="work-item">
                <div class="image-placeholder">
                    <a href="html/{detail_page_name}" class="link">
                        <img src="{image_src}" alt="{escaped_alt}"{size_attrs} loading="lazy" decoding="async">
                    </a>
                </div>
            </div>
"""


def append_card_to_index(index_path: Path, card_block: str) -> None:
    index_html = index_path.read_text(encoding="utf-8")
    close_grid = "\n        </div>\n    </main>"
    if close_grid not in index_html:
        raise RuntimeError("Could not find closing </div> for works-grid in index.html")

    updated = index_html.replace(close_grid, f"\n{card_block}        </div>\n    </main>", 1)
    index_path.write_text(updated, encoding="utf-8")


def validate_image_path(image_path: str) -> Path:
    normalized = Path(image_path)
    if normalized.is_absolute():
        raise ValueError("Use a repo-relative image path like assets/p/new-work.jpg")
    full_path = ROOT / normalized
    if not full_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    return full_path


def default_page_name_from_image(image_path: str) -> str:
    stem = Path(image_path).stem
    return f"{stem}.html"


def ensure_page_name(page_name: str) -> str:
    if not page_name.endswith(".html"):
        return f"{page_name}.html"
    return page_name


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a new artwork detail page and append a card to index.html."
    )
    parser.add_argument("--title", required=True, help="Displayed work title")
    parser.add_argument(
        "--image",
        required=True,
        help="Repo-relative image path used in index/detail, e.g. assets/p/My Work.jpg",
    )
    parser.add_argument(
        "--page",
        default="",
        help="Detail filename under html/, defaults to image filename stem + .html",
    )
    parser.add_argument(
        "--alt",
        default="",
        help="Alt text for images (defaults to --title)",
    )
    parser.add_argument(
        "--media-line",
        action="append",
        default=[],
        help="Add a line to the detail media info paragraph (can repeat).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow overwriting an existing detail page and duplicate index card.",
    )
    args = parser.parse_args()

    image_full_path = validate_image_path(args.image)
    page_name = ensure_page_name(args.page) if args.page else default_page_name_from_image(args.image)
    detail_path = DETAIL_DIR / page_name
    alt_text = args.alt.strip() if args.alt.strip() else args.title.strip()
    media_lines = args.media_line if args.media_line else [args.title.strip()]

    if detail_path.exists() and not args.force:
        print(
            f"Detail page already exists: {detail_path.relative_to(ROOT)}\n"
            "Use --force to overwrite.",
            file=sys.stderr,
        )
        return 1

    index_html = INDEX_PATH.read_text(encoding="utf-8")
    href_snippet = f'href="html/{page_name}"'
    if href_snippet in index_html and not args.force:
        print(
            f"Index already contains a card for {page_name}.\n"
            "Use --force to allow duplicates.",
            file=sys.stderr,
        )
        return 1

    dimensions = get_dimensions(image_full_path)
    width, height = (dimensions if dimensions else (None, None))

    detail_html = build_detail_html(
        page_title=args.title.strip(),
        image_src=args.image,
        alt_text=alt_text,
        width=width,
        height=height,
        media_lines=media_lines,
    )
    detail_path.write_text(detail_html, encoding="utf-8")

    card_html = build_index_card(
        detail_page_name=page_name,
        image_src=args.image,
        alt_text=alt_text,
        width=width,
        height=height,
    )
    append_card_to_index(INDEX_PATH, card_html)

    print(f"Created detail page: {detail_path.relative_to(ROOT)}")
    print(f"Updated index card list: {INDEX_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
