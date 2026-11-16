# ButterSkin Brand Guidelines (fictional concept)

## Idea
ButterSkin should feel like **a botanical garden presented like a fine boutique**: natural, warm, premium and calm. It never sells perfection or promises results. The approved direction is "Botanical Luxury" (Option 1).

## Logo
| File | Use |
|---|---|
| `logo/butterskin-lockup-stacked.svg` | Primary lockup on ivory or white |
| `logo/butterskin-lockup-stacked-dark.svg` | On Deep Emerald (background plate included) |
| `logo/butterskin-lockup-stacked-reverse.svg` | Over dark photography, no plate |
| `logo/butterskin-lockup-horizontal.svg`, `-horizontal-dark.svg` | Website and wide spaces |
| `logo/butterskin-lockup-compact.svg` | App header and small sizes, without the tagline |
| `logo/butterskin-wordmark.svg` | Wordmark alone |
| `logo/butterskin-emblem.svg`, `-champagne.svg`, `-ivory.svg` | The lotus on its own: favicon, caps, stickers |
| `app-icon/app-icon-1024.svg` | App icon master, full-bleed (the platform applies the mask). `app-icon-rounded-preview.svg` is for presentation only. |

- **Emblem:** an original line-drawn lotus. It has a tall centre petal, two side petals, two low leaves and a water line, drawn with round joins.
- **Wordmark:** BUTTERSKIN in Playfair Display capitals, tracked +0.2 em, over BOTANICAL SKINCARE in Inter, tracked +0.34 em. All type is outlined to paths.
- **Clear space:** at least half the emblem's height on every side.
- **Minimum size:** emblem 16 px; stacked lockup 140 px wide (use the compact lockup below that).
- **Don't:** add the ® symbol (it's a fictional brand), fill the emblem's petals solid, recolour it outside the palette, or set the wordmark in lowercase.

## Colour
The source of truth is [`../tokens/tokens.json`](../tokens/tokens.json), which also holds the full contrast table. 20 of 20 text and control pairs pass WCAG AA; the lowest text pair is 4.96:1.

| Core colour | HEX | Role |
|---|---|---|
| Deep Emerald | `#0E4A38` | Primary · actions, headlines, glass |
| Sage Green | `#7F9F86` | Secondary · surfaces and illustration |
| Ivory | `#FAF8F4` | Background |
| Champagne | `#C9AA6B` | Accent · caps, rules, emblem |
| Charcoal | `#1F2A24` | Text |

| Support tone | HEX |
|---|---|
| Emerald 900 | `#0A3729` |
| Emerald 800 | `#0E4A38` |
| Emerald 700 | `#155C46` |
| Emerald 100 | `#E2ECE6` |
| Sage 100 | `#EDF2EC` |
| Sage 200 | `#D9E3D9` |
| Sage 300 | `#B7CBBB` |
| Sage 500 | `#7F9F86` |
| Ivory 0 | `#FFFFFF` |
| Ivory 50 | `#FAF8F4` |
| Ivory 100 | `#F3EFE7` |
| Ivory 200 | `#E6DFD2` |
| Champagne 200 | `#EFE3C8` |
| Champagne 400 | `#C9AA6B` |
| Champagne 700 | `#7A5E28` |
| Charcoal 900 | `#1F2A24` |
| Charcoal 700 | `#38433D` |
| Charcoal 600 | `#56605A` |
| Charcoal 400 | `#8A928D` |
| Stone 200 | `#ECE6DB` |
| Stone 300 | `#D8CFC0` |

- Sage 500 and Champagne 400 are **decorative only**: surfaces, rules, caps and the emblem. They are too light for text on ivory.
- For small champagne-coloured text, use Champagne 700.
- Buttons and links use Deep Emerald 800, with Emerald 700 on hover and Emerald 900 when pressed.

## Typography
- **Playfair Display** (400, 500, 600, plus 400 italic): the logo, headlines, product names and prices.
- **Inter** (400–600): interface text and body copy, including the ₹ sign. Buttons and eyebrows are set in capitals with +0.10 to +0.16 em tracking.
- Both are licensed under the SIL OFL 1.1. The font files and licences are in `prototype/assets/fonts/`.
- Body text is 16 px, and nothing visible is smaller than 12 px.

## Shape and controls
- Radius: controls 2 px, cards 4 px, media 4 px, sheets 12 px. Buttons are rectangular, not pills.
- **Primary button:** an Emerald 800 fill with a white label. On photographs, use an ivory fill with an emerald label.
- **Secondary button:** an emerald outline. **Text button:** an underlined emerald label.
- **Focus:** a 2 px Champagne 700 ring with a 2 px offset on every control.
- **Touch targets:** at least 44 × 44 px. Quantity steppers run from 1 to 5, and the end buttons are disabled at each limit.
- **Icons:** line icons at a 1.5 px stroke with round joins, matching the emblem.

## Packaging (fictional)
- **Materials:**
  - Deep emerald glass for the serum.
  - Frosted glass for the gel cleanser, essence and night oil.
  - Porcelain-white glass for the cream jar and moisturiser pump.
  - Soft-touch white tubes for the milk cleanser and SPF.
- **Metal:** every cap, collar and pump is brushed champagne metal.
- **Label:** the lotus, BUTTERSKIN, the product name in Playfair, a key-ingredient line in Inter, and "SIZE · CONCEPT". The flat artwork is in `packaging/labels/`.
- **No claims on the pack:** no "anti-ageing", "clinically proven", "dermatologist tested", "vegan" or results promises.

## Photography (3D)
- There's no product photography. All product images are photorealistic 3D renders, made by `tools/render/`.
- **Brand scenes:** warm side sunlight, travertine stone, moss, small white flowers and leaves, and a soft golden background.
- **Shop packshots:** a single product on a quiet ivory background with soft shadows.
- **Textures:** a swatch of each formula on stone with one leaf.
- **Never:** people or faces, before-and-after images, or stock photography.

## Voice
- Calm, warm and precise: "Real care for real skin." "Skipping a step is fine."
- Product copy describes where a product fits and what its ingredients are commonly used for, never what it fixes.
- Shopping copy is clear about money: prices are always visible, delivery rules are stated, and the demo checkout says that nothing is charged.
- Never: shame, urgency, countdowns, fake scarcity, fake reviews, ratings, diagnosis or miracle claims.
