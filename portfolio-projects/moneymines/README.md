# MoneyMines: Rewards-Based Transaction App (Concept)

> **Self-initiated concept project.** MoneyMines is a fictional product created for a graphic and product design portfolio. It is not an operating financial service. There are no real payments, bank connections, UPI, financial APIs, offers or rewards. All people, merchants, rates and amounts are fictional demonstration data.

**Product promise:** Make eligible transactions. Discover rewards. Track your progress.

## Status

| Stage | Scope | Status |
|-------|-------|--------|
| 1 | Repository inspection & folder structure | ✅ Done |
| 2 | Brand identity, design tokens, screen map, reward rules | ✅ Done and approved (Strike mark, field-survey direction) |
| 3 | Core screens: dashboard, transactions, rewards, redemption | ✅ Done and approved |
| 4 | Remaining screens, mockups, prototype, Behance case study | ✅ Done: 51 screens and states, 24/24 automated checks passing, awaiting review |
| 5 | Quality checks & final report | Not started |

## Product brief

MoneyMines lets people make everyday payments (bills and recharges, merchant payments, transfers to people, and partner shopping) and see, transparently, which of those payments earn something. There are four mechanisms: **cashback**, **fixed bonuses**, **points** and **referral rewards**. Rewards move from **pending** to **confirmed** and can be redeemed (simulated) as a bank transfer, an in-app benefit, or a voucher.

## Design rationale

Rewards apps often borrow casino language: confetti, countdowns, "you won!", and one swollen balance that mixes real money with maybes. MoneyMines takes the opposite stance. Its visual world is a **field survey**: strata, seams and contour lines, which are patient and exact.

1. **Dashed means not yet yours.** Pending rewards are drawn as outlines, never solid fills.
2. **Every reward explains itself.** The calculation, cap and rule ID sit next to every amount.
3. **Balances never merge.** Wallet funds, confirmed rewards, pending rewards and points are always shown separately.
4. **Calm over urgent.** Expiry is a dated fact, not a timer.
5. **Simulated, and says so.** Every confirmation carries a demo notice.

## Open the prototype

1. On GitHub, switch to the `moneymines-concept` branch and choose **Code → Download ZIP**, then unzip it.
2. Open `portfolio-projects/moneymines/prototype/index.html` in Chrome, Edge or Firefox.

Full instructions are in [`prototype/README.md`](prototype/README.md). The prototype runs offline and only shows simulated data.

## Asset guide

```
portfolio-projects/moneymines/
├── README.md                       this file
├── design/
│   ├── brand/                      logo SVGs, app icon, fonts (SIL OFL), patterns, boards/, brand-guidelines.md
│   ├── components/                 tokens.json, tokens.css, component-specs.md, icons/ (30 SVG)
│   ├── screens/                    51 editable HTML screens (390 × 844) + assets/ (screens.css, embedded fonts)
│   └── mockups/                    device-mockup and all-screens overview sources (HTML)
├── behance/
│   ├── case-study.md               full case-study narrative
│   ├── captions.md                 upload order + caption for each image
│   ├── project-description.md      Behance title, description, tags (draft)
│   └── slides/                     editable HTML sources of the case-study slides
├── exports/                        flattened PNGs, independent of the prototype
│   ├── behance/                    01–19 · upload in this order · 3200 px wide
│   ├── brand/                      brand boards · 3200 × 2000
│   ├── mockups/                    4 device-mockup compositions · 3200 px wide
│   └── screens/                    51 screens at 1170 × 2532, full-length/ variants, 00-all-screens-overview
├── prototype/                      index.html viewer + README
└── documentation/
    ├── sample-data.json            single source of truth (28 Oct 2026 snapshot + labelled hypotheticals)
    ├── reward-rules.md             rules, worked examples, reconciliation
    ├── screen-inventory.md         screen map and IA
    ├── user-flows.md               journeys mapped to screens
    ├── validation-report.md        automated check results
    └── known-limitations.md
```

**Source vs export:** files under `design/` and `behance/slides/` are editable sources. PNGs under `exports/` are flattened and can be used on Behance without the prototype.

## Viewing and editing

- **SVG logos:** open in any browser, Figma or Illustrator. The type is outlined, so no fonts are needed.
- **Screens, boards and slides:** open the HTML files in Chrome or Edge from a downloaded copy. Fonts are embedded or loaded from `design/brand/fonts/`. To use them in Figma, import with an HTML-to-Figma plugin, or place the PNG exports.
- **Tokens:** link `design/components/tokens.css` from any page, or import `tokens.json` into Tokens Studio or Style Dictionary.

## Credits & licences

- **Concept & art direction: Purnananda Mishra · AI-assisted design and production.**
- Typefaces: Space Grotesk by Florian Karsten; Inter by Rasmus Andersson. Both SIL Open Font License 1.1.
- All other artwork is original to this project.
