# ButterSkin Brand Guidelines (fictional concept)

## Idea
ButterSkin should feel like **a botanical apothecary in a porcelain room**. It is premium, quiet and commercially credible, and it never sells perfection. The direction is called "Porcelain Garden".

## Logo
| File | Use |
|---|---|
| `logo/butterskin-lockup.svg` | Primary lockup with the BOTANICAL SKINCARE tagline, on porcelain or white |
| `logo/butterskin-lockup-dark.svg` | On Emerald 800 (the background plate is included) |
| `logo/butterskin-lockup-stacked.svg` | Square spaces, social avatars, packaging sides |
| `logo/butterskin-lockup-compact.svg` | App header and small sizes, without the tagline |
| `logo/butterskin-wordmark.svg` | Wordmark alone |
| `logo/butterskin-monogram.svg`, `-reverse.svg`, `-mono.svg` | The seal on its own: favicon, caps, stickers |
| `app-icon/app-icon-1024.svg` | App icon master, full-bleed (the platform applies the mask). `app-icon-rounded-preview.svg` is for presentation only. |

- **The seal:** an Emerald 800 disc with a fine Champagne 400 ring and a Bodoni Moda capital *B*, like the stamp on an apothecary jar.
- **Wordmark:** BUTTERSKIN in Jost, all capitals, tracked +0.24 em, outlined to paths.
- **Clear space:** at least half the seal's diameter on every side.
- **Minimum size:** seal 16 px; lockup 120 px wide (use the compact lockup below that).
- **Don't:** add the ® symbol (it's a fictional brand), recolour the seal outside the palette, set the wordmark in lowercase, or put the light lockup on emerald.

## Colour
The source of truth is [`../tokens/tokens.json`](../tokens/tokens.json), which also holds the full contrast table. All 18 pairs pass WCAG AA. The lowest text pair is 5.08:1.

| Token | HEX | Role |
|---|---|---|
| Porcelain 50 | `#FCFBF8` | Canvas |
| Porcelain 0 | `#FFFFFF` | Cards, labels |
| Porcelain 100 | `#F4F2EC` | Sunken surfaces, Moisturise |
| Charcoal 900 | `#262A28` | Primary text |
| Charcoal 600 | `#5B605C` | Muted text (5:1 or better on every surface it is used on) |
| Emerald 800 | `#1B5643` | Primary actions, links, the seal |
| Emerald 900 | `#0F3B2D` | Headlines, pressed state |
| Sage 200 | `#E5ECE3` | Secondary surfaces, Cleanse |
| Champagne 400 | `#CDB68A` | Rings, caps, fine rules (decorative only) |
| Champagne 700 | `#7A5E2A` | Eyebrows and the focus ring |
| Champagne 200 | `#EFE4CC` | Treat, highlights |
| Mist 200 | `#E4EBEE` | Protect |

Category colour is always paired with the category name in text. Champagne is an accent: never use it for long text, and never use Champagne 400 for text at all.

## Typography
- **Bodoni Moda** (400/500, with 400 italic): display, headings, product names, prices on cards.
- **Jost** (400–600): interface text and body copy. Buttons, eyebrows and labels are set in capitals with +0.12 to +0.18 em tracking.
- Both are licensed under the SIL OFL 1.1. The font files and licences are in `prototype/assets/fonts/`. A subset of DM Sans (also SIL OFL) supplies the ₹ sign only, because Jost doesn't include it.
- Body text is 16 px, and nothing visible is smaller than 12 px.

## Shape & controls
- Radius: controls 2 px, cards 4 px, media 6 px, sheets 12 px. Buttons are rectangular, not pills.
- **Primary button:** Emerald 800 fill with a white label. Hover is Emerald 700, pressed is Emerald 900, and disabled is a 45% tint with no pointer.
- **Secondary button:** an Emerald 800 outline. **Text button:** an underlined emerald label.
- Every control has a visible focus ring: 2 px of Champagne 700 with a 2 px offset.
- Touch targets are at least 44 × 44 px. Quantity steppers have a 1–5 range, and the end buttons are disabled at each limit.

## Packaging (fictional)
- Five formats: tube, pump, dropper, jar and bottle, with brushed champagne caps.
- Body colour follows the routine: frosted glass to cleanse, emerald to treat, porcelain to moisturise and protect.
- A white label with a fine champagne border shows BUTTERSKIN, the product name in Bodoni Moda, the routine step in emerald, and "SIZE · CONCEPT".
- No claims on the pack: no "anti-ageing", no "clinically proven", and no promises beyond the product name.
- **Imagery:** there is no product photography. Products are shown as studio-lit vector renders and illustrated texture swatches, all labelled "concept".

## Voice
- Calm, precise and supportive: "Skipping a step is fine." "Where it fits, not what it fixes."
- Shopping copy is clear about money: prices are always visible, delivery rules are stated, and the demo checkout says that nothing is charged.
- Never: shame, urgency, countdowns, fake scarcity, fake reviews, diagnosis or miracle claims.
