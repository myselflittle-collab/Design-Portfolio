# ButterSkin: real care for real skin (concept)

> **Self-initiated concept.** ButterSkin is a fictional brand and shopping app made for a design portfolio. Products, formulations, prices and journal entries are illustrative. Product images are photorealistic 3D renders, not photographs. The checkout is a demo: no order is placed and nothing is charged. Nothing here is medical advice, and no user research or usability testing was carried out.

**Idea:** a premium botanical skincare label with its own shopping app. Discover eight essentials, read key ingredients in plain words, build a morning and evening routine, and check out without friction. The visual direction is "Botanical Luxury": deep emerald, sage, ivory and champagne, a line-drawn lotus, and sunlit 3D product scenes.

## Open the prototype
1. Download the `butterskin-concept` branch (GitHub → **Code → Download ZIP**) and unzip it.
2. Open `portfolio-projects/butterskin/prototype/index.html` in Chrome, Edge, Firefox or Safari.

It works offline: the fonts and images are local, with no external requests. GitHub's website shows the code rather than running it, so use the downloaded copy.

Any screen or state can be opened directly by its route, for example `index.html#/shop?cat=treat` or `index.html#/bag?demo=empty`. The full list is in `documentation/screen-inventory.md`.

## What's inside
```
portfolio-projects/butterskin/
├── README.md
├── data/products.json            single source of truth: products, routines, demo bag, delivery rules (fictional)
├── prototype/                    index.html, app.js, styles.css
│   └── assets/                   fonts/, products/ (24 renders), photo/ (hero, range, detail), logos, data.js, tokens.css
├── design/
│   ├── brand/                    logo/, app-icon/, packaging/ (renders/, labels/), brand-guidelines.md
│   ├── tokens/                   tokens.json (with contrast table), tokens.css
│   └── mockups/                  HTML sources of the device mockups
├── behance/                      case-study.md, captions.md, project-description.md, slides/ (HTML sources)
├── exports/                      PNGs, usable without the prototype
│   ├── behance/                  01–17 boards, 3200 px wide, in upload order
│   ├── mockups/                  3 mockup compositions
│   └── screens/                  mobile/ (1170 × 2532), mobile-full/, desktop/ (2880 × 1800), manifest.json
├── tools/                        brand.py, build_data.py, export_screens.py, boards.py, inventory.py
│   └── render/                   3D packaging models, labels and render scripts (Blender Cycles)
├── tests/                        run_checks.py, results.json, vendor/axe.min.js (axe-core 4.10.2, MPL-2.0)
└── documentation/                validation-report.md, screen-inventory.md, known-limitations.md, file-inventory.md
```

## Rebuild
From `portfolio-projects/butterskin/` (needs Python 3 with `playwright`, `fonttools`, `brotli`, `uharfbuzz` and `pillow`):
```
python3 tools/brand.py           # tokens, lotus emblem, logos, app icon
python3 tools/build_data.py      # data/products.json → prototype/assets/data.js
python3 tools/export_screens.py  # screen PNGs from the prototype
python3 tools/boards.py          # mockups and Behance boards
python3 tests/run_checks.py      # checks → documentation/validation-report.md
python3 tools/inventory.py       # documentation/file-inventory.md
```
The product renders are already included. To re-render them (about 75 minutes on 2 CPU cores, needs `pip install bpy==5.2.3`):
```
sh tools/render/render_all.sh    # renders every image, then installs them as JPGs
```

## Status
- The "Botanical Luxury" revision (approved Option 1) is complete on `butterskin-concept`.
- Validation results are in [`documentation/validation-report.md`](documentation/validation-report.md).
- Nothing is published, and nothing is merged into `main`.

## Credits
Concept & art direction: Purnananda Mishra

Typefaces: Playfair Display and Inter (SIL Open Font License 1.1). 3D renders: Blender (Cycles). Accessibility engine: axe-core 4.10.2 (Mozilla Public License 2.0), used only in tests. The logo, packaging, labels and 3D models are original to this concept.
