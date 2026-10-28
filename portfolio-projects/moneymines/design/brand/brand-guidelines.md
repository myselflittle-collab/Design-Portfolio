# MoneyMines Brand Guidelines

> Self-initiated concept. MoneyMines is a fictional product and not a financial service.

**Status:** Strike is the recommended mark. It is **pending approval** before the app screens are built (Stage 3).

## 1. Idea

Rewards are *found* inside everyday transactions; they are not handed out. The identity borrows from geological survey work: strata, seams, contour lines. That world is patient, measured and exact, which suits a product whose job is to say precisely what you've earned and when it becomes yours.

**Personality:** transparent, steady, precise, quietly optimistic. **Not:** flashy, gamified, urgent or "get rich".

## 2. Logo

### The mark: Strike
Two shafts angle down towards a lime **facet**, the moment a reward is found. The shapes form an M, and the facet becomes a reward marker reused across the interface.

| File | Use |
|------|-----|
| `logo/moneymines-lockup-light.svg` | Primary logo on paper or white |
| `logo/moneymines-lockup-dark.svg` | On Forest 950 (plate included) |
| `logo/moneymines-lockup-reverse-transparent.svg` | On any dark brand surface |
| `logo/moneymines-lockup-mono.svg` | One-colour print or engraving |
| `logo/moneymines-wordmark-*.svg` | Where the symbol already appears nearby |
| `logo/moneymines-symbol*.svg` | Avatars, favicons, tight spaces |
| `app-icon/app-icon-1024.svg` | Store master, full-bleed square (the platform applies its own mask) |
| `app-icon/*-rounded-preview.svg` | Presentation only |
| `logo/concepts/` | Exploration record: Seam, Strike, Bench |

**Wordmark:** "moneymines" in lowercase Space Grotesk Medium, tracked −1.8%, outlined to paths. The dot of the *i* is replaced by the facet.

**Construction (at wordmark size 100):** cap height 70, symbol height 76 sitting on the baseline, gap of 26 between symbol and wordmark.

### Clear space
- **Symbol:** keep clear space of **x** on all sides, where x is the width of one shaft (≈ 18% of symbol width).
- **Lockup:** keep clear space equal to the symbol's height.

### Minimum size
- Symbol: **20 px / 6 mm**
- Lockup: **96 px / 25 mm** wide

### Don't
- Recolour the facet. It is always Lime 400, or the single ink colour in mono versions.
- Rotate, skew, outline, add shadows to or apply gradients to the mark.
- Rebuild the wordmark in another typeface or in title case.
- Place the logo on photography without a solid Paper or Forest plate.
- Use the facet as decoration away from rewards.

## 3. Colour

| Token | HEX | Role |
|-------|-----|------|
| Forest 950 | `#0B2219` | Dark surfaces, app icon background |
| Forest 900 | `#0F2E20` | Raised dark surfaces |
| Forest 800 | `#164029` | Primary action, logo ink on light |
| Forest 700 | `#1D5235` | Reward amounts on light, links, success text |
| Forest 500 | `#3F8560` | Chart layer, dashed border on dark |
| Forest 200 | `#BFD9C7` | Muted text on dark, chart layer |
| Forest 100 | `#DDEBE0` | Success chip background |
| Charcoal 900 | `#1A1D1F` | Primary text, wallet funds |
| Charcoal 600 | `#4A5055` | Secondary text, pending amounts |
| Charcoal 500 | `#5F666B` | Tertiary text (minimum text contrast) |
| Charcoal 400 | `#858B8F` | Input borders, dashed pending outline (3:1) |
| Paper 50 | `#F7F4EC` | App canvas: warm white |
| Paper 0 | `#FFFDF8` | Cards |
| Paper 100 | `#EFEBE0` | Sunken areas, inputs, ineligible rows |
| Paper 200 | `#E2DDCF` | Hairlines |
| Lime 400 | `#C5EE4A` | **Reward accent only:** facet, confirmed figures on dark |
| Lime 700 | `#4E6A00` | Lime-family text on light, if ever required |

**Ratio guide:** roughly 60% paper, 25% forest and charcoal, 10% status tints, and no more than 5% lime.

### Status colours (always paired with a label and an icon)

| Status | Text | Background | Icon | Contrast |
|--------|------|------------|------|----------|
| Successful / Confirmed | `#1D5235` | `#DDEBE0` | check | 7.4:1 |
| Pending | `#7A4F00` | `#FAEBC6` | clock | 6.0:1 |
| Failed | `#A3261C` | `#FBE3DF` | circle-x | 6.0:1 |
| Reversed | `#2B5170` | `#DCE7EF` | return arrow | 6.7:1 |
| Cancelled / Not eligible | `#4A5055` | `#E9E7E0` | slash / info | 6.6:1 |

All text pairs meet WCAG 2.2 AA. The full contrast table is in [`../components/component-specs.md`](../components/component-specs.md).

## 4. Typography

Both families are licensed under the **SIL Open Font License 1.1**. Font files and licences are in `fonts/`.

| Family | Use |
|--------|-----|
| **Space Grotesk** (Florian Karsten) | Headlines, overlines and **every monetary amount**, with tabular figures |
| **Inter** (Rasmus Andersson) | Body, labels, captions |

The full scale is in `../components/tokens.json`. Rules:
- Body text is at least 16 px. Nothing interactive is set below 13 px.
- Amounts always use tabular figures and Indian digit grouping (₹27,742.50), and are right-aligned in lists.
- Points never use the ₹ sign. They're written as "1,240 pts".

## 5. Graphic elements

- **Facet:** the reward marker. It appears beside confirmed reward amounts and in the logo.
- **Survey lines** (`pattern-survey-lines-*.svg`): a contour texture, used only on dark hero surfaces and empty states. Never placed behind numbers or text blocks smaller than 24 px.
- **Strata / core sample:** a charting form. Stacked layers show reward composition, with pending as a dashed top layer.
- **Depth gauge:** progress towards a threshold. A segmented bar with a plain-language gap ("₹28.00 more needed"). Never a timer.
- **Icons** (`../components/icons/`): 24 px grid, 1.75 stroke, round caps and joins.

## 6. Voice

- Say what happened, then what it means for the user's money: "Order returned on 19 Oct. Amount refunded and cashback reversed."
- Name the rule: "Not eligible: monthly limit of 3 bill bonuses already reached."
- Never say "earn money", "guaranteed", "free cash", "hurry" or "last chance".
- Demo notice wording: **"Simulated: no money will move."**
