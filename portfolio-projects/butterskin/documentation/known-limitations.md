# Known Limitations

## Concept
- ButterSkin is a fictional brand. Products, formulations, prices, people and journal entries are illustrative.
- Ingredient notes describe what an ingredient is commonly used for, not what a product does. Nothing here is medical or cosmetic advice.
- No user research, interviews or usability testing were done. The "representative needs" are assumptions.
- No dermatological, legal or regulatory review.

## Prototype
- Session-only: ticks, saved products, notes and preferences live in memory and reset on reload. Nothing is stored or sent.
- No accounts, shop, checkout or backend.
- English only; no right-to-left or Indic-script layouts.
- Light theme only.
- `?demo=empty` and `?demo=error` routes exist to show states for review and export.

## Testing
- Automated checks ran in headless Chromium only. Firefox and Safari were not available in the build environment.
- axe-core finds many, but not all, accessibility issues. No manual screen-reader testing (VoiceOver, TalkBack, NVDA) was done.
- Visual quality is judged by eye.

## Presentation
- Phone screenshots inside boards are illustrative; full-resolution screens are in `exports/screens/`.
- The Behance cover crop (808 × 632) is not a separate file.
- Packaging is flat vector illustration, not photorealistic renders.
