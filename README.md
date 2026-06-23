# jooeunkim.github.io

## Data-Driven Portfolio

- `index.html` now renders the grid from `data/works.json`.
- `work.html?id=...` renders a single artwork detail view from the same JSON.
- Existing `html/*.html` pages are still kept as fallback/legacy pages.
- `works-noscript.html` is a static no-JavaScript fallback gallery generated from `data/works.json`.

## Add New Artwork

```bash
python3 scripts/add_artwork.py \
  --title "New Work Title" \
  --thumb "assets/p/New Work.jpg" \
  --full "assets/p/New Work.jpg" \
  --id "New Work.html" \
  --alt "New Work, 2026, Jooeun Kim" \
  --media-line "New Work, 2026" \
  --media-line "Oil on canvas" \
  --media-line "24 x 30 in / 61 x 76 cm"
```

Notes:
- `--id` is optional. If omitted, it uses the thumb image filename stem + `.html`.
- `--alt` is optional. If omitted, it uses `--title`.
- `--full` is optional. If omitted, it uses `--thumb`.
- If you skip `--media-line`, one line with `--title` is used.
- To control order: use `--position start` or `--after-id "Existing Work.html"`.
- The script also rebuilds `works-noscript.html` automatically.

## Manual Edit

You can also edit `data/works.json` directly.
Each item uses:

- `id`
- `title`
- `thumbSrc`
- `fullSrc`
- `alt`
- `width`, `height`
- `mediaLines` (array of lines shown in detail view)

If you edit `data/works.json` manually and want to refresh the no-JS page:

```bash
python3 scripts/build_noscript_gallery.py
```
