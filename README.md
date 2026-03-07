# jooeunkim.github.io

## Add New Artwork

Use this script to create a new detail page and append a new card to `index.html` in one step.

```bash
python3 scripts/add_artwork.py \
  --title "New Work Title" \
  --image "assets/p/New Work.jpg" \
  --page "New Work.html" \
  --alt "New Work, 2026, Jooeun Kim" \
  --media-line "New Work, 2026" \
  --media-line "Oil on canvas" \
  --media-line "24 x 30 in / 61 x 76 cm"
```

Notes:
- `--page` is optional. If omitted, the script uses the image filename stem + `.html`.
- `--alt` is optional. If omitted, it uses `--title`.
- If you skip `--media-line`, the detail page will show one line using `--title`.
- The script blocks duplicates by default. Use `--force` only if you intentionally want to overwrite an existing detail page or add a duplicate card.
