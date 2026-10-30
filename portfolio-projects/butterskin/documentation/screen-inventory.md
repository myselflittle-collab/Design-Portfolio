# Screen Inventory

All screens are exported from the prototype by `tools/export_screens.py`, so the PNGs always match the code. Open any route by adding it to `prototype/index.html`.

Mobile: 390 × 844 at 3× → 1170 × 2532 (`exports/screens/mobile/`), plus full-length versions in `mobile-full/`.

| # | File | Route | Screen |
|---|------|-------|--------|
| 1 | 01-welcome-1 | `#/welcome/1` | Welcome · 1 of 3 |
| 2 | 02-welcome-2 | `#/welcome/2` | Welcome · 2 of 3 |
| 3 | 03-welcome-3 | `#/welcome/3` | Welcome · 3 of 3 |
| 4 | 04-personalise | `#/setup` | Personalise (optional) |
| 5 | 05-home | `#/home` | Home |
| 6 | 06-shop | `#/shop` | Shop all |
| 7 | 07-shop-treat | `#/shop?cat=treat` | Shop · category |
| 8 | 08-shop-focus | `#/shop?focus=1&sort=price-asc` | Shop · focus filter, sorted |
| 9 | 09-shop-no-results | `#/shop?q=retinol` | Shop · no results |
| 10 | 10-product | `#/product/dewdrop-hydration-serum` | Product detail |
| 11 | 11-product-ingredients | `#/product/butter-balm-cream` | Product detail · ingredients |
| 12 | 12-added-to-bag | `#/product/butter-balm-cream` | Added to bag dialog |
| 13 | 13-bag | `#/bag` | Shopping bag |
| 14 | 14-bag-empty | `#/bag?demo=empty` | Shopping bag · empty |
| 15 | 15-checkout | `#/checkout` | Demo checkout |
| 16 | 16-checkout-error | `#/checkout?demo=error` | Demo checkout · validation |
| 17 | 17-order | `#/order` | Demo order confirmation |
| 18 | 18-wishlist | `#/wishlist` | Wishlist |
| 19 | 19-wishlist-empty | `#/wishlist?demo=empty` | Wishlist · empty |
| 20 | 20-routine-am | `#/routine` | Routine · morning |
| 21 | 21-routine-pm | `#/routine?time=PM` | Routine · evening |
| 22 | 22-journal | `#/journal` | Skin journal |
| 23 | 23-journal-new | `#/journal/new` | New note |
| 24 | 24-journal-error | `#/journal/new?demo=error` | New note · validation |
| 25 | 25-account | `#/account` | Account & skin profile |
| 26 | 26-about | `#/about` | About this concept |
| 27 | 27-home-checkin | `#/home` | Home · check-in confirmation |

Desktop exports (1440 × 900 at 2× → 2880 × 1800, `exports/screens/desktop/`): Home, Shop all, Product detail, Shopping bag, Demo checkout, Routine · morning, Skin journal, Account & skin profile.

Total: 27 mobile screens and states, 8 desktop screens.
