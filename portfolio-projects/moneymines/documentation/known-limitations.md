# Known Limitations & Open Decisions

This file is kept up to date at every stage.

## Concept limitations (permanent)
- MoneyMines is a fictional concept. There are no payment gateway, bank, UPI, KYC or financial API integrations, and none are implied.
- Reward rates, caps, merchants, billers, people and amounts are demonstration values only.
- No user research, interviews or usability testing were carried out. Design decisions are reasoned from principles and accessibility standards, not from measured outcomes.
- No regulatory or legal review. A real product would need compliance review of reward terms, disclosures and data handling.

## Stage 2 notes
- The design is light-first. Dark surfaces are used for hero cards and the app icon, and a full dark theme is not specified.
- Lime 400 can't be used as text on light backgrounds (contrast fails), so rewards on light use Forest 700 plus the facet marker.
- The app icon master is a full-bleed square, and the rounded previews are for presentation only.
- Only Latin script is covered. Hindi and other Indian-language typography is not designed.

## Stage 3 notes
- Screens are authored as HTML/CSS, which is editable and exact, rather than native Figma files. PNG exports at 3× are the presentation assets.
- S19 shows a hypothetical voucher redemption. The base dataset is as of 28 Oct, before it (see user-flows.md).
- The status bar time (9:41) and device chrome are illustrative.
- No dark-mode screens.

## Stage 4 notes
- The prototype is a click-through of static screens. Nothing is typed, stored or sent, and toggles don't change state.
- Seven state variants (errors and empty states) are reached through the prototype's **States** panel rather than a natural tap path, because in the 28 Oct snapshot those situations don't occur.
- Out-of-scope actions (share, add money, settings, new OTP, change contact) show an explanatory note instead of a screen.
- The prototype must be opened from a downloaded copy. GitHub's website shows the HTML source rather than running it.
- Screen fonts are embedded as subsets (Latin plus ₹ and common symbols) so they render from disk.
- Phone screenshots inside slides are illustrative. The captions carry the meaning, and full-resolution screens are in `exports/screens/`.

## Decisions
- Approved on 28 Oct 2026: Strike mark and field-survey direction.
- Credit line: "Concept & art direction: Purnananda Mishra."
