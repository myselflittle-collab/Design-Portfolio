# Screen Inventory

Every screen is a route in the prototype. Exports are generated straight from it by `tools/export_screens.py`; the list of exported screens is in `exports/screens/manifest.json`.

| # | Export id | Route | Screen / state |
|---|---|---|---|
| 1 | 01-welcome-1 | `#/welcome/1` | Welcome · Your skin, understood |
| 2 | 02-welcome-2 | `#/welcome/2` | Welcome · Skipping a step is fine |
| 3 | 03-welcome-3 | `#/welcome/3` | Welcome · Personal, not prescriptive |
| 4 | 04-setup | `#/setup` | Optional setup (skin type, focus) |
| 5 | 05-home | `#/home` | Home: today's progress, check-in, shelf, picks |
| 6 | 06-routine-am | `#/routine` | Routine · morning |
| 7 | 07-routine-pm | `#/routine?time=PM` | Routine · evening |
| 8 | 08-discover | `#/discover` | Discover · all products |
| 9 | 09-discover-treat | `#/discover?cat=treat` | Discover · category filter |
| 10 | 10-discover-focus | `#/discover?focus=1` | Discover · suits my focus |
| 11 | 11-discover-no-results | `#/discover?q=retinol` | **State:** no results |
| 12 | 12-product | `#/product/butter-balm-cream` | Product dialog (bottom sheet on mobile) |
| 13 | 13-product-spf | `#/product/daylight-spf-50` | Product dialog · SPF |
| 14 | 14-shelf | `#/shelf` | Shelf |
| 15 | 15-shelf-empty | `#/shelf?demo=empty` | **State:** empty shelf |
| 16 | 16-journal | `#/journal` | Skin journal |
| 17 | 17-journal-empty | `#/journal?demo=empty` | **State:** empty journal |
| 18 | 18-journal-new | `#/journal/new` | New note |
| 19 | 19-journal-error | `#/journal/new?demo=error` | **State:** validation error |
| 20 | 20-profile | `#/profile` | Profile & preferences |
| 21 | 21-about | `#/about` | About this concept |
| 22 | 22-home-checkin | `#/home` + tap a mood | **State:** confirmation toast |

Desktop exports (1440 × 900 at 2×): Home, Routine, Discover, Product, Journal and Profile.

The `?demo=empty` and `?demo=error` parameters only change what is shown. They exist so the states can be reviewed and exported.
