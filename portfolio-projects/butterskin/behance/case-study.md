# ButterSkin: Botanical Skincare, Beautifully Simple

**Self-initiated concept · Brand identity, packaging design, e-commerce UX/UI and prototype · 2026**
**Concept & art direction: Purnananda Mishra · AI-assisted design and production**

> ButterSkin is fictional. It is not a real brand, shop or medical tool. Products, formulations, prices and journal entries are illustrative. Product images are rendered packaging, not photographs. The checkout is a demo: no order is placed and nothing is charged. Nothing here is medical advice. No user research or usability testing was carried out, and the principles below are design assumptions.

---

## 1. Overview

ButterSkin is a concept for a premium botanical skincare label and its own shopping app. In the app you can:
- discover eight essentials by routine step or skin focus
- read what is inside, in plain words
- build a morning and evening routine
- keep a private skin journal
- add to bag and go through a short demo checkout.

**Deliverables:**
- brand identity, guidelines and design tokens
- a packaging family for eight fictional products
- a responsive shopping prototype with 27 exported mobile screens and states, plus 8 desktop screens
- this case study and 16 presentation boards.

## 2. Design approach (assumptions)

1. **Commercially credible.** Prices are always visible, every card has Add to bag and a wishlist button, the bag has real quantity controls, and the checkout takes three steps.
2. **Where it fits, not what it fixes.** Each product sits in a routine step, and ingredients are described by what they are commonly used for. There are no miracle claims, ratings or before-and-after images.
3. **Personal, not prescriptive.** An optional skin profile reorders picks. It never diagnoses, and there are no scores or streaks.
4. **Honest content.** "Concept" labels sit where claims usually would, and the demo checkout says plainly that nothing is charged.

## 3. Brand identity

- **The seal:** an emerald disc with a fine champagne ring and a Bodoni Moda *B*, like the stamp on an apothecary jar.
- **Wordmark:** BUTTERSKIN in widely tracked Jost capitals, with an optional BOTANICAL SKINCARE tagline.
- **Colour:** porcelain backgrounds, deep emerald for actions, muted sage for secondary surfaces, champagne for fine details, and charcoal text.
- **Type:** Bodoni Moda for names and headlines, Jost for the interface. Both are SIL OFL 1.1 and served locally.

Full rules are in [`../design/brand/brand-guidelines.md`](../design/brand/brand-guidelines.md).

## 4. Packaging design (fictional)

Five formats (tube, pump, dropper, jar and bottle) with brushed champagne caps. Body colour follows the routine: frosted glass to cleanse, emerald to treat, porcelain to moisturise and protect. One label system carries the brand, the product name, the routine step and "size · concept".

There is no product photography. Real-looking photos of products that don't exist would mislead, so products are shown as studio-lit vector renders and illustrated texture swatches.

## 5. Home & discovery

- **Home:** a featured edit, shop by step, picks for your skin focus, and today's routine.
- **Shop:** search, underline category tabs, a "Suits my focus" switch and sort by price. Each card shows the image, name, short description, size, price, a wishlist button and Add to bag.
- **No results:** says what happened and offers Clear filters.

## 6. Product details & ingredients

A gallery with pack, in-scene and texture views; size and price; a quantity stepper with a full-width Add to bag; accordions for how to use, key ingredients and where it fits; a patch-test note; and "Pairs well with".

## 7. Routines & personalisation

- **Skin profile:** two optional questions, and "Not sure" is allowed.
- **Morning and evening:** real checkboxes, progress for today only, and Clear. **Shop this routine** adds only the missing products to the bag.
- **Journal:** short private notes with a mood, never scored. Home has a one-tap check-in.

## 8. Shopping experience

1. **Add to bag** opens a confirmation dialog with View bag and Continue shopping.
2. **Bag:** quantity steppers (1–5), Remove, and an order summary. Delivery is free over ₹999, otherwise ₹79.
3. **Delivery details:** five fields, standard or express delivery, and a linked error summary with a message on each field.
4. **Confirmation:** a demo order reference, and a plain statement that no order was sent and nothing was charged.

Empty states for the bag and wishlist each offer one clear way forward.

## 9. Mobile & desktop

Below 900 px, a bottom tab bar is used. Above it, a top navigation with wider grids and a side-by-side bag summary takes over. The same code and data power both.

## 10. Accessibility (documentation only)

The app was built against WCAG 2.2 AA. Actual results are in [`../documentation/validation-report.md`](../documentation/validation-report.md) and are not shown on the presentation boards.
- Real buttons, checkboxes, radio groups and labels; errors linked to fields; a skip link; visible focus; 44 px targets; no text below 12 px.
- The Add to bag dialog moves focus inside, traps Tab, closes on Escape or a backdrop click, returns focus to the button you used, and makes the page behind inert.
- **Not yet done:** testing with screen-reader users or with people in general. Automated tests ran in Chromium only.

## 11. Tools, contribution & limitations

**Contribution:**
- **Purnananda Mishra:** concept, art direction, choice of visual direction, and review at each stage.
- **AI-assisted:** design production, prototype code, packaging illustration, checks and writing, under that direction.

**Tools:** HTML, CSS and JavaScript; Python (tokens, logo and packaging generation); Playwright with Chromium (screen exports and tests); axe-core 4.10.2.

**Limitations:** fictional brand, products and prices; rendered packaging with no photography; a demo checkout with no backend; no user research or usability testing; no dermatological or regulatory review; English only; tested in Chromium only. See [`../documentation/known-limitations.md`](../documentation/known-limitations.md).
