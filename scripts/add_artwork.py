#!/usr/bin/env python3
"""Append a new artwork entry to data/works.json."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
WORKS_JSON = ROOT / "data" / "works.json"


def get_dimensions(image_path: Path) -> tuple[int, int] | None:
    try:
        result = subprocess.run(
            ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(image_path)],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None

    width = None
    height = None
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("pixelWidth:"):
            width = line.split(":", 1)[1].strip()
        elif line.startswith("pixelHeight:"):
            height = line.split(":", 1)[1].strip()

    if width and height and width.isdigit() and height.isdigit():
        return int(width), int(height)
    return None


def ensure_repo_relative(path_value: str, label: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        raise ValueError(f"{label} must be repo-relative, got absolute path: {path_value}")
    full_path = ROOT / path
    if not full_path.exists():
        raise FileNotFoundError(f"{label} does not exist: {path_value}")
    return full_path


def default_id_from_path(image_path: str) -> str:
    return f"{Path(image_path).stem}.html"


def load_works() -> list[dict]:
    if not WORKS_JSON.exists():
        raise FileNotFoundError(f"Missing {WORKS_JSON.relative_to(ROOT)}")
    with WORKS_JSON.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        raise ValueError("works.json root must be an array")
    return data


def save_works(works: list[dict]) -> None:
    WORKS_JSON.write_text(
        json.dumps(works, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add a new artwork to data/works.json")
    parser.add_argument("--title", required=True, help="Artwork title")
    parser.add_argument("--thumb", required=True, help="Grid image path (repo-relative)")
    parser.add_argument("--full", default="", help="Detail image path (defaults to --thumb)")
    parser.add_argument("--id", default="", help="Artwork id used in work.html?id=... (defaults to thumb stem + .html)")
    parser.add_argument("--alt", default="", help="Alt text (defaults to title)")
    parser.add_argument(
        "--media-line",
        action="append",
        default=[],
        help="Line in detail metadata (repeatable). Defaults to title.",
    )
    parser.add_argument(
        "--position",
        choices=["start", "end"],
        default="end",
        help="Where to insert in works order",
    )
    parser.add_argument(
        "--after-id",
        default="",
        help="Insert after an existing id (overrides --position)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    works = load_works()

    thumb_full_path = ensure_repo_relative(args.thumb, "--thumb")
    full_src = args.full.strip() if args.full.strip() else args.thumb.strip()
    ensure_repo_relative(full_src, "--full")

    work_id = args.id.strip() if args.id.strip() else default_id_from_path(args.thumb)
    if any(work.get("id") == work_id for work in works):
        raise ValueError(f"Duplicate id exists: {work_id}")

    alt = args.alt.strip() if args.alt.strip() else args.title.strip()
    media_lines = args.media_line if args.media_line else [args.title.strip()]

    dimensions = get_dimensions(thumb_full_path)
    width, height = dimensions if dimensions else (None, None)

    new_work = {
        "id": work_id,
        "title": args.title.strip(),
        "legacyPage": f"html/{work_id}",
        "thumbSrc": args.thumb.strip(),
        "fullSrc": full_src,
        "alt": alt,
        "width": width,
        "height": height,
        "mediaLines": media_lines,
    }

    if args.after_id:
        for i, work in enumerate(works):
            if work.get("id") == args.after_id:
                works.insert(i + 1, new_work)
                break
        else:
            raise ValueError(f"--after-id not found: {args.after_id}")
    elif args.position == "start":
        works.insert(0, new_work)
    else:
        works.append(new_work)

    save_works(works)
    print(f"Added artwork id={work_id} to {WORKS_JSON.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
