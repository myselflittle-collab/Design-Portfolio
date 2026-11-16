# Known Limitations

## Concept
- ButterSkin is a fictional brand. Products, formulations, prices and journal entries are illustrative.
- Ingredient notes describe what an ingredient is commonly used for, not what a product does. Nothing here is medical or cosmetic advice.
- No user research, interviews or usability testing were done. The design principles are assumptions.
- No dermatological, legal or regulatory review.

## Product imagery
- **No product photography.** The products don't exist, so real-looking photographs of them would mislead. Every product image is a photorealistic 3D render of modelled packaging (Blender Cycles), and every label carries "CONCEPT".
- The plants, stones, moss and flowers in the botanical scenes are also 3D. They match the approved direction in mood and materials, but up close the leaves look smoother and more stylised than real foliage.
- The 3D models are presentation models, not manufacturing artwork. Pack sizes are illustrative.

## Prototype
- Session-only: the bag, wishlist, ticks, notes and preferences live in memory and reset on reload. Nothing is stored or sent.
- **Demo checkout.** No payment step, no account and no backend. "Place demo order" only shows a confirmation, and every screen says that nothing is charged.
- Prices are illustrative, in rupees. Delivery rules (free over ₹999, otherwise ₹79, or ₹149 for express) are made up for the demo.
- No ratings, reviews or certification badges are shown, because none exist.
- English only; no right-to-left or Indic-script layouts. Light theme only.
- `?demo=empty` and `?demo=error` routes exist to show states for review and export.

## Testing
- Automated checks ran in headless Chromium only. Firefox and Safari were not available in the build environment.
- axe-core finds many, but not all, accessibility issues. No manual screen-reader testing (VoiceOver, TalkBack, NVDA) was done.
- Text placed over photographs (the Home hero) cannot be measured automatically; it sits on a dark emerald overlay and was checked by eye.
- Visual quality is judged by eye.

## Presentation
- Phone screenshots inside boards are illustrative; full-resolution screens are in `exports/screens/`.
- The Behance cover crop (808 × 632) is not a separate file.
