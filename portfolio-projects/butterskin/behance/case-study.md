# ButterSkin: Botanical Skincare, Real Care for Real Skin

**Self-initiated concept · Brand identity, packaging design, 3D product renders, e-commerce UX/UI and prototype · 2026**
**Concept & art direction: Purnananda Mishra · AI-assisted design and production**

> ButterSkin is fictional. It is not a real brand, shop or medical tool. Products, formulations, prices and journal entries are illustrative. Product images are photorealistic 3D renders, not photographs. The checkout is a demo: no order is placed and nothing is charged. Nothing here is medical advice. No user research or usability testing was carried out, and the principles below are design assumptions.

---

## 1. Overview

ButterSkin is a concept for a premium botanical skincare label and its own shopping app. In the app you can:
- discover eight essentials by routine step or skin focus
- read the key ingredients in plain words
- build a morning and evening routine
- keep a private skin journal
- add to bag and go through a short demo checkout.

**Deliverables:**
- brand identity, design tokens and guidelines
- a packaging family for eight fictional products, rendered in 3D
- a product photography direction: botanical scenes, packshots and texture swatches
- a responsive shopping prototype with 27 exported mobile screens and states, plus 8 desktop screens
- this case study and 17 presentation boards.

## 2. Design approach (assumptions)

1. **Botanical luxury.** Deep emerald glass, champagne metal, sunlit stone and leaves. The brand should feel like a garden, presented like a fine boutique.
2. **Honest information.** Each product shows its key ingredients and where it fits in a routine. There are no ratings, certification badges, "best seller" labels or results claims.
3. **Shopping that works.** Prices are always visible, every card has Add to bag and a wishlist button, the bag has real quantity controls, and the checkout takes three steps.
4. **Personal, not prescriptive.** An optional skin profile reorders picks. It never diagnoses, and there are no scores or streaks.

## 3. Brand identity

- **Emblem:** an original line-drawn lotus with a tall centre petal, two side petals, two low leaves and a water line.
- **Wordmark:** BUTTERSKIN in Playfair Display capitals, widely spaced, over BOTANICAL SKINCARE in Inter.
- **Colour:** Deep Emerald #0E4A38, Sage #7F9F86, Ivory #FAF8F4, Champagne #C9AA6B and Charcoal #1F2A24. Every text and control colour pair meets WCAG AA. Sage and bright champagne are used only for surfaces and decoration.
- **Type:** Playfair Display for names and headlines, Inter for the interface. Both are SIL OFL 1.1 and served locally.

Full rules are in [`../design/brand/brand-guidelines.md`](../design/brand/brand-guidelines.md).

## 4. Packaging design (fictional)

All eight products keep their names:
- **Dewdrop Hydration Serum:** deep emerald glass with a glass pipette.
- **Soft Gel Cleanser** and **Soft Cloud Moisturiser:** frosted and porcelain-white pump bottles.
- **Still Water Essence:** a frosted glass bottle with a screw cap.
- **Quiet Night Oil:** a frosted dropper with golden oil.
- **Butter Balm Cream:** a porcelain-white jar.
- **Cloud Milk Cleanser** and **Daylight SPF 50:** soft-touch tubes.

Every cap, collar and pump is brushed champagne metal. One label system shows the lotus, BUTTERSKIN, the product name, a key-ingredient line, and the size with "CONCEPT".

## 5. Product photography direction (3D)

There is no product photography, because the products don't exist and real-looking photos of them would mislead. Instead the packaging was modelled and rendered in Blender (Cycles), with real glass, liquid, metal and printed labels:
- **Brand scenes:** warm side light, travertine, moss, small white flowers and leaves.
- **Packshots:** quiet ivory backgrounds, used in the shop.
- **A garden scene and a texture swatch** for every product, used in the product gallery.

## 6. Home & discovery

- **Home:** a sunlit hero with an emerald overlay, a strip of three honest brand facts, shop by step, and picks for your skin focus.
- **Shop:** search, category tabs, a "Suits my focus" switch and sort by price. Each card shows the photo, name, short description, key ingredients, size, price, a wishlist button and Add to bag.
- **No results:** says what happened and offers Clear filters.

## 7. Product details & ingredients

A three-view gallery (packshot, garden scene, texture); size and price; a quantity stepper with a full-width Add to bag; accordions for how to use, key ingredients and where it fits; a patch-test note; and "Pairs well with".

## 8. Routines & personalisation

- **Skin profile:** two optional questions, and "Not sure" is allowed.
- **Morning and evening:** real checkboxes, progress for today only, and Clear. **Shop this routine** adds only the missing products to the bag.
- **Journal:** short private notes with a mood, never scored. Home has a one-tap check-in.

## 9. Shopping experience

1. **Add to bag** opens a confirmation dialog with View bag and Continue shopping.
2. **Bag:** quantity steppers (1–5), Remove, and an order summary. Delivery is free over ₹999, otherwise ₹79.
3. **Delivery details:** five fields, standard or express delivery, and a linked error summary with a message on each field.
4. **Confirmation:** a demo order reference, and a plain statement that no order was sent and nothing was charged.

## 10. Mobile & desktop

Below 900 px, a bottom tab bar is used. Above it, a top navigation with wider grids and a side-by-side bag summary takes over. The same code and data power both.

## 11. Accessibility (documentation only)

The app was built against WCAG 2.2 AA. Actual results are in [`../documentation/validation-report.md`](../documentation/validation-report.md) and are not shown on the presentation boards.
- Real buttons, checkboxes, radio groups and labels; errors linked to fields; a skip link; visible focus; 44 px targets; no text below 12 px.
- The Add to bag dialog moves focus inside, traps Tab, closes on Escape or a backdrop click, returns focus to the button you used, and makes the page behind inert.
- **Not yet done:** testing with screen-reader users or with people in general. Automated tests ran in Chromium only.

## 12. Tools, contribution & limitations

**Contribution:**
- **Purnananda Mishra:** concept, art direction, choice of the Botanical Luxury direction, and review at each stage.
- **AI-assisted:** design production, prototype code, 3D packaging and renders, checks and writing, under that direction.

**Tools:** HTML, CSS and JavaScript; Python (tokens and logo generation); Blender Cycles (3D product renders); Playwright with Chromium (screen exports and tests); axe-core 4.10.2.

**Limitations:** fictional brand, products and prices; 3D renders, not photography; a demo checkout with no backend; no user research or usability testing; no dermatological or regulatory review; English only; tested in Chromium only. See [`../documentation/known-limitations.md`](../documentation/known-limitations.md).
