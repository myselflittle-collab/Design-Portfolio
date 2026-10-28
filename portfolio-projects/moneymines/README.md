# MoneyMines: Rewards-Based Transaction App (Concept)

> **Self-initiated concept project.** MoneyMines is a fictional product created for a graphic and product design portfolio. It is not an operating financial service. There are no real payments, bank connections, UPI, financial APIs, offers or rewards. All people, merchants, rates and amounts are fictional demonstration data.

**Product promise:** Make eligible transactions. Discover rewards. Track your progress.

## Status

| Stage | Scope | Status |
|-------|-------|--------|
| 1 | Repository inspection & folder structure | ✅ Done |
| 2 | Brand identity, design tokens, screen map, reward rules | ✅ Done, **awaiting approval of the Strike mark and the direction** |
| 3 | Core screens: dashboard, transactions, rewards, redemption | Not started |
| 4 | Remaining screens, mockups, exports, Behance case study | Not started |
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

## Asset guide

```
portfolio-projects/moneymines/
├── README.md                     this file
├── design/
│   ├── brand/
│   │   ├── logo/                 lockups, wordmarks, symbols (SVG, outlined) + concepts/
│   │   ├── app-icon/             1024 px masters + rounded previews
│   │   ├── fonts/                Space Grotesk & Inter (SIL OFL 1.1) with licences
│   │   ├── boards/               editable HTML sources of the brand boards
│   │   ├── pattern-survey-lines-*.svg
│   │   └── brand-guidelines.md
│   ├── components/               tokens.json, tokens.css, component-specs.md, icons/
│   ├── screens/                  Stage 3–4: editable screen sources
│   └── mockups/                  Stage 4: device mockups
├── behance/                      Stage 4: case-study text, captions, ordered slides
├── exports/
│   └── brand/                    01–05 brand boards, PNG at 3200 × 2000
├── prototype/                    Stage 4: local interactive demo (simulated data only)
└── documentation/
    ├── reward-rules.md           fictional rules, worked examples, reconciliation
    ├── sample-data.json          the single dataset used by every screen
    └── screen-inventory.md       screen map, IA, journeys
```

Empty folders appear in GitHub once they contain files in later stages.

**Source vs export:** SVG and HTML files under `design/` are editable sources. PNGs under `exports/` are flattened copies for Behance and can be used without the prototype.

## Viewing and editing

- **SVG logos:** open in any browser, Figma (drag in) or Illustrator. Text is outlined, so no fonts are needed.
- **Brand boards:** open `design/brand/boards/*.html` in Chrome or Edge from a downloaded copy of the repository. Fonts load from `design/brand/fonts/`. Exported PNGs are in `exports/brand/`.
- **Tokens:** `design/components/tokens.css` can be linked by any HTML page. `tokens.json` can be imported into Figma Tokens or Style Dictionary.
- **Fonts:** install the `.otf` files from `design/brand/fonts/` to use them in design tools.

## Credits & licences

- Concept, brand and product design: Purnananda Mishra (self-initiated). Prepared with AI-assisted production.
- Typefaces: Space Grotesk by Florian Karsten; Inter by Rasmus Andersson. Both SIL Open Font License 1.1.
- All other artwork is original to this project.
