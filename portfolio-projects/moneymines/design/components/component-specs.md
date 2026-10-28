# MoneyMines: Components & Tokens (Stage 2 foundation)

Token sources: [`tokens.json`](tokens.json) (canonical) and [`tokens.css`](tokens.css) (CSS custom properties `--mm-*` plus type classes `.mm-*`). Icons: [`icons/`](icons/), 24 × 24 grid, 1.75 stroke.

Screens are designed at **390 × 844** with 20 px side margins, a 4-column grid and 12 px gutters. Touch targets are at least 48 × 48.

## Foundations

| Group | Values |
|-------|--------|
| Spacing (4-pt) | 2 · 4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 48 · 64 · 80 |
| Radius | xs 4 · sm 8 · md 12 · lg 20 · xl 28 · pill 999 |
| Borders | hairline 1 px Paper 200 · strong 1.5 px · **pending dash 1.5 px, 4/3** |
| Elevation | e0 none · e1 hairline + soft 3 px shadow (cards) · e2 32 px soft shadow (sheets) |
| Motion | 120 ms fast · 180 ms standard · 260 ms sheets · `cubic-bezier(0.2,0,0,1)` · all 0 ms under *reduce motion* |

### Type scale

| Role | Font | Size / line | Notes |
|------|------|-------------|-------|
| display | Space Grotesk 500 | 40/44 | Onboarding only |
| h1 | Space Grotesk 500 | 28/34 | Screen titles |
| h2 | Space Grotesk 500 | 22/28 | Section titles |
| h3 | Space Grotesk 500 | 18/24 | Card titles |
| title | Inter 600 | 16/22 | List item titles |
| body | Inter 400 | 16/24 | Minimum for reading text |
| body-sm | Inter 400 | 14/20 | Supporting text |
| label | Inter 500 | 13/16 | Chips, small buttons |
| caption | Inter 400 | 12/16 | Demo notices, timestamps |
| overline | Space Grotesk 500 | 11/16, +8% caps | Section labels |
| amount-hero | Space Grotesk 500 | 44/48 tabular | Main balance |
| amount-lg | Space Grotesk 500 | 24/28 tabular | Reward balances |
| amount-md | Space Grotesk 500 | 16/20 tabular | List amounts, right-aligned |

## Core components

| Component | Anatomy | Variants and states | Rules |
|-----------|---------|---------------------|-------|
| **Button** | 52 px high, radius 14, Inter 600 16 | Primary (Forest 800), Secondary (1.5 px Charcoal 400 outline), Tertiary (text), Destructive (Failed fg). States: default, pressed (Forest 900), focus (2 px Forest 600 ring with 2 px offset), disabled (Paper 100 fill, Charcoal 500 text, *plus* a reason line underneath) | Confirm buttons in demo flows always read "Confirm demo payment" or "Confirm simulated redemption" |
| **Balance tile** | Overline, amount, caption | Wallet (solid, ₹) · Confirmed rewards (facet + ₹, lime on dark or Forest 700 on light) · Pending (dashed box, Charcoal 600) · Points ("pts", no ₹) | Never summed into one total |
| **Status chip** | Pill, 24–28 px, icon 14–16 + label | Successful · Pending · Failed · Reversed · Cancelled · Not eligible · Expired | Label and icon are required. Colour is supporting only |
| **Reward row** | Title, calculation line, amount, chip | Confirmed (solid card + facet) · Pending (dashed card) · Reversed (struck amount) · Not eligible (sunken card, "—") | Calculation line is required: "₹1,000.00 × 2% · until 30 Oct" |
| **Calculation block** | Ledger lines, divider, result | Cashback · Capped cashback · Bonus · Points (with rounding note) | Shows the rule ID and transaction ID |
| **Depth gauge** | Overline, current / target, 14 px segmented bar, gap sentence | Below threshold · Reached | Never animated as a countdown. The sentence states the gap in ₹ |
| **Core sample** | Stacked layers to scale + labels | Pending (dashed) on top of confirmed layers | Every layer has a text label and amount |
| **Transaction list item** | Icon tile 40 px, title, sub-line (date · type), amount right-aligned, chip | All five transaction states | Failed and cancelled items say whether money moved |
| **Info row** | Info icon, sentence, optional link | Eligibility · Fees · Limits · Demo notice | Used *before* the user commits, not only after |
| **Demo notice** | Caption with Charcoal 600 text on Paper 100, lock icon | Inline · Banner · Receipt footer | Wording: "Simulated: no money will move." |
| **Bottom navigation** | 5 slots, 64 px + safe area | Home · Activity · **Pay** (raised Forest 800 tile with the facet) · Rewards · Profile | Active item: Forest 800 icon + label + 2 px top bar |
| **Input** | 52 px, Paper 100 fill, 1.5 px Charcoal 400 border, label above | Default · Focus (Forest 600 border) · Error (Failed fg border + message + icon) · Disabled | Amount inputs use amount-lg with tabular figures |
| **Skeleton** | Paper 100 blocks matching final layout | — | Shimmer disabled under reduce motion |
| **Empty state** | Survey-line mini illustration, one sentence, one action | — | No mascots |

## Contrast verification (WCAG 2.2)

| Pair | Colours | Ratio | Required | Result |
|------|---------|-------|----------|--------|
| Primary text on canvas | `#1A1D1F` on `#F7F4EC` | 15.42:1 | 4.5:1 | Pass |
| Secondary text on canvas | `#4A5055` on `#F7F4EC` | 7.43:1 | 4.5:1 | Pass |
| Tertiary text on surface | `#5F666B` on `#FFFDF8` | 5.74:1 | 4.5:1 | Pass |
| Tertiary text on sunken | `#5F666B` on `#EFEBE0` | 4.90:1 | 4.5:1 | Pass |
| Primary button label | `#F7F4EC` on `#164029` | 10.62:1 | 4.5:1 | Pass |
| Text on dark hero | `#F7F4EC` on `#0B2219` | 15.20:1 | 4.5:1 | Pass |
| Muted text on dark hero | `#BFD9C7` on `#0B2219` | 11.11:1 | 4.5:1 | Pass |
| Lime reward figure on dark | `#C5EE4A` on `#0B2219` | 12.49:1 | 4.5:1 | Pass |
| Charcoal text on lime fill | `#1A1D1F` on `#C5EE4A` | 12.67:1 | 4.5:1 | Pass |
| Lime-ink text on canvas | `#4E6A00` on `#F7F4EC` | 5.64:1 | 4.5:1 | Pass |
| Forest link on canvas | `#1D5235` on `#F7F4EC` | 8.27:1 | 4.5:1 | Pass |
| Success chip | `#1D5235` on `#DDEBE0` | 7.37:1 | 4.5:1 | Pass |
| Pending chip | `#7A4F00` on `#FAEBC6` | 6.03:1 | 4.5:1 | Pass |
| Failed chip | `#A3261C` on `#FBE3DF` | 6.02:1 | 4.5:1 | Pass |
| Reversed chip | `#2B5170` on `#DCE7EF` | 6.65:1 | 4.5:1 | Pass |
| Cancelled chip | `#4A5055` on `#E9E7E0` | 6.60:1 | 4.5:1 | Pass |
| Input border (non-text) | `#858B8F` on `#F7F4EC` | 3.14:1 | 3:1 | Pass |
| Focus ring on light (non-text) | `#2A6B47` on `#F7F4EC` | 5.80:1 | 3:1 | Pass |
| Focus ring on dark (non-text) | `#C5EE4A` on `#0B2219` | 12.49:1 | 3:1 | Pass |

Lime 400 on Paper fails text contrast, so **lime is never used for text on light surfaces.**
