# ButterSkin: skincare, made softer (concept)

> **Self-initiated concept.** ButterSkin is a fictional brand and app made for a design portfolio. Products, formulations, prices, people and journal entries are illustrative. Nothing is sold, stored or sent, and nothing here is medical advice. No user research or usability testing was carried out.

**Idea:** a calm skincare companion. Keep a simple routine, find everyday essentials and notice how your skin feels, with no scores, streaks or promises.

## Open the prototype
1. Download the `butterskin-concept` branch (GitHub → **Code → Download ZIP**) and unzip it.
2. Open `portfolio-projects/butterskin/prototype/index.html` in Chrome, Edge, Firefox or Safari.

It works offline: the fonts and images are local, with no external requests. GitHub's website shows the code rather than running it, so use the downloaded copy.

Any screen or state can be opened directly by its route, e.g. `index.html#/discover?cat=treat` or `index.html#/shelf?demo=empty`. The full list is in `documentation/screen-inventory.md`.

## What's inside
```
portfolio-projects/butterskin/
├── README.md
├── data/products.json            single source of truth for products, routines, journal and preferences (fictional)
├── prototype/                    index.html, app.js, styles.css, assets/ (fonts, logo, packaging, data.js, tokens.css)
├── design/
│   ├── brand/                    logo/, app-icon/, packaging/, brand-guidelines.md
│   ├── tokens/                   tokens.json (with contrast table), tokens.css
│   └── mockups/                  HTML sources of the device mockups
├── behance/                      case-study.md, captions.md, project-description.md, slides/ (HTML sources)
├── exports/                      PNGs, usable without the prototype
│   ├── behance/                  01–17 boards, 3200 px wide, in upload order
│   ├── mockups/                  3 mockup compositions
│   └── screens/                  mobile/ (1170 × 2532), mobile-full/, desktop/ (2880 × 1800), manifest.json
├── tools/                        brand.py, build_data.py, export_screens.py, boards.py
├── tests/                        run_checks.py, results.json, vendor/axe.min.js (axe-core 4.10.2, MPL-2.0)
└── documentation/                validation-report.md, screen-inventory.md, known-limitations.md, file-inventory.md
```

## Rebuild
From `portfolio-projects/butterskin/` (needs Python 3 with `playwright`, `fonttools`, `brotli`, `uharfbuzz`, `pillow`):
```
python3 tools/brand.py           # tokens, logos, app icon, packaging
python3 tools/build_data.py      # data/products.json → prototype/assets/data.js
python3 tools/export_screens.py  # screen PNGs from the prototype
python3 tests/run_checks.py      # checks → documentation/validation-report.md
python3 tools/boards.py          # mockups and Behance boards (the accessibility board quotes the latest results)
```

## Status
- Phases 1–3 are complete on `butterskin-concept`.
- Validation results are in [`documentation/validation-report.md`](documentation/validation-report.md).
- Nothing is published, and nothing is merged into `main`.

## Credits
Concept & art direction: Purnananda Mishra · AI-assisted design and production

Typefaces: Playfair Display and DM Sans (SIL Open Font License 1.1). Accessibility engine: axe-core 4.10.2 (Mozilla Public License 2.0), used only in tests. All illustrations, packaging and logos are original to this concept.
