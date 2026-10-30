# ButterSkin Brand Guidelines (fictional concept)

## Idea
ButterSkin should feel like **soft butter on warm paper**: calm, tactile and unhurried. The brand supports people and never sells perfection.

## Logo
| File | Use |
|---|---|
| `logo/butterskin-lockup-light.svg` | Primary, on paper or light backgrounds |
| `logo/butterskin-lockup-dark.svg` | On Olive 800 (background plate included) |
| `logo/butterskin-lockup-mono.svg` | One-colour use |
| `logo/butterskin-wordmark.svg` | Wordmark alone |
| `logo/butterskin-mark.svg`, `-butter.svg`, `-mono.svg` | The pat on its own: favicon, avatar, labels |
| `app-icon/app-icon-1024.svg` | App icon master, full-bleed (the platform masks it); `app-icon-rounded-preview.svg` is for presentation only |

- **The pat:** a soft square with three large rounded corners and one tucked bottom-left corner, rotated −8°, containing a lowercase *b* in Playfair Display SemiBold.
- **Wordmark:** "butterskin" in DM Sans Bold, lowercase, tracked −3.5%, outlined to paths.
- **Clear space:** at least half the pat's width on every side.
- **Minimum size:** pat 16 px; lockup 96 px wide.
- **Don't:** add the ® symbol (it's a fictional brand), recolour the pat outside the palette, straighten the tilt, or set the wordmark in capitals.

## Colour
The source of truth is [`../tokens/tokens.json`](../tokens/tokens.json), which also holds the full contrast table. Every pair passes WCAG AA.

| Token | HEX | Role |
|---|---|---|
| Paper 50 | `#F7F2E8` | Canvas |
| Paper 0 | `#FFFCF6` | Cards, labels |
| Ink 900 | `#26291F` | Text |
| Ink 600 | `#55594A` | Muted text (lowest text tone: 5.5:1 or better on every surface it's used on) |
| Olive 800 | `#3F4A2E` | Primary action, packaging caps |
| Olive 600 | `#56623F` | Mark, links, focus ring |
| Butter 300 | `#F2DC8F` | Brand accent, app icon, Moisturise |
| Sage 200 | `#DCE4CF` | Cleanse, hero surfaces |
| Clay 200 | `#EED5C4` | Treat |
| Sky 200 | `#D7E4EA` | Protect |

Category colour is always paired with the category name in text.

## Typography
- **Playfair Display** (500/600): headlines, the *b* in the mark, editorial italics.
- **DM Sans** (400–700): interface text, body copy, the wordmark.
- Both are licensed under the SIL OFL 1.1; the font files and licences are in `prototype/assets/fonts/`.
- Body text is 16 px, and nothing visible is smaller than 12 px.

## Packaging direction (fictional)
- Five formats: tube, pump, dropper, jar, bottle.
- Olive 800 caps and a body in the category colour.
- A cream label with the pat, the wordmark, the product name and "size · concept".
- No claims on the pack: no SPF promises beyond the product name, no "anti-ageing", no "clinically proven".

## Voice
- Warm, plain and supportive: "Skipping a step is fine." "Do what feels right today."
- Products are described by where they fit, never by what they "fix".
- Never: shame, urgency, perfection, diagnosis, or miracle claims.
