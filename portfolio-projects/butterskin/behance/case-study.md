# ButterSkin: A Skincare App That Lets Skin Be Skin

**Self-initiated concept · Brand identity, packaging direction, UX/UI and prototype · 2026**
**Concept & art direction: Purnananda Mishra · AI-assisted design and production**

> ButterSkin is fictional. It is not a real brand, shop or medical tool. Products, formulations, prices, people and journal entries are illustrative. Nothing is sold, stored or sent, and nothing here is medical advice. No user research or usability testing was carried out. The users and problems below are design assumptions, stated as such.

---

## 1. Overview

ButterSkin is a concept for a skincare companion app. It helps you:
- keep a simple morning and evening routine
- find everyday essentials
- note how your skin feels.

It does this without scores, streaks or promises.

**Deliverables:**
- brand identity and design tokens
- a packaging direction for eight fictional products
- a responsive prototype with 22 exported screens and states
- automated accessibility and behaviour checks
- this case study.

## 2. The design problem (assumptions)

Many skincare and wellness apps lean on patterns that make care feel like performance. This project treats them as **assumptions to design against**, not research findings:

- streaks, scores and badges that punish a missed night
- "before and after" promises and miracle-style claims
- long ingredient lists with no plain-language context
- quizzes that feel like a diagnosis.

**Principles:**
1. **Skipping is fine.** Routines are checklists, never scores.
2. **Where it fits, not what it fixes.** Products are described by their place in a routine.
3. **Personal, not prescriptive.** Preferences reorder content and never diagnose.
4. **Calm by default.** Soft colour, plain words, generous space.
5. **Honest content.** "Fictional" and "concept" labels sit where claims usually would.

## 3. Representative needs (assumption-based, not research personas)

| Profile | Context | Representative question |
|---|---|---|
| The routine starter | Wants three or four steps that are easy to remember | "What do I actually need in the morning?" |
| The ingredient-curious | Reads labels but feels lost in the jargon | "What is niacinamide, in plain words?" |
| The gentle tracker | Notices flare-ups and wants a light way to keep notes | "Was my skin drier after that windy weekend?" |

## 4. Key decisions

| Decision | Why |
|---|---|
| **Removed the routine streak.** An early draft showed "Routine streak: 4 days". It became a "Saved on your shelf" count, and the final app shows today's progress only. | Streaks reward perfection and punish a missed night, which contradicts the brand idea. |
| **"Skipping a step is fine."** Optional steps are labelled, the completion message is neutral, and "Clear today's ticks" is always available. | Progress stays informational, not moral. |
| **Where it fits, not what it fixes.** The product dialog shows the routine step, how to use it, and ingredients described as what they are *commonly used for*. | Avoids implying results a fictional product can't support. |
| **Concept labels in place.** "Concept product", "concept formulation", and "concept" on every pack label; a patch-test note on every product. | Fiction stays obvious even when one screen is seen alone. |
| **Preferences, never diagnosis.** Setup is optional, has a "Not sure" option, and only reorders or filters products. | Personal without pretending to be clinical. |
| **Notice, don't judge.** One-tap check-in on Home and a private journal, never scored; a note points to a doctor or dermatologist if something worries you. | Reflection without self-surveillance. |
| **Identity: the pat.** A soft square with three rounded corners and one tucked corner, tilted 8°, holding a serif *b*. | Butter, softness and handmade warmth, without a literal butter illustration. |

## 5. Information architecture & flows

Tabs: **Home · Routine · Discover · Journal · Profile**. The shelf sits behind a heart in the header. Onboarding (three cards) and an optional setup come first.

1. **First run:** Welcome 1 → 2 → 3 → optional setup → Home. Every step can be skipped.
2. **Morning routine:** Home → Routine (tick steps; focus stays on the checkbox) → product dialog → Evening tab.
3. **Discover:** search, category filters, a "Suits my focus" switch → product dialog → save to shelf.
4. **Notice, don't judge:** Home check-in → Journal → New note, with gentle validation if the note is empty.

## 6. Visual identity & packaging

- **Mark and wordmark:** the pat with a Playfair Display *b*; the wordmark is DM Sans Bold, lowercase. Light, dark and one-colour versions, plus an app icon.
- **Colour:** butter paper canvas, botanical olive for actions, and four category colours (sage = Cleanse, clay = Treat, butter = Moisturise, sky = Protect). Colour always comes with a text label.
- **Type:** Playfair Display for editorial headlines, DM Sans for interface text. Both SIL OFL 1.1, served locally.
- **Packaging (fictional):** five formats (tube, pump, dropper, jar, bottle) with olive caps, category-coloured bodies and a cream label carrying the pat, the product name and "size · concept".

## 7. Accessibility

Built and checked against WCAG 2.2 AA. Actual results are in [`../documentation/validation-report.md`](../documentation/validation-report.md).
- All 18 token colour pairs pass AA (text 4.5:1, borders and focus 3:1).
- axe-core 4.10.2 with WCAG 2.2 A/AA rules runs on 20 screens and states at mobile and desktop widths.
- Real checkboxes, radio groups, labels and `aria-describedby` errors; a skip link; visible focus; 44 px touch targets; no text below 12 px; reduced motion respected.
- The product dialog moves focus inside, traps Tab, closes on Escape or a backdrop click, returns focus to the product, and makes the page behind inert.
- **Not yet done:** testing with screen-reader users or with people in general. Automated tests ran in Chromium only.

## 8. Tools, contribution & limitations

**Contribution:**
- **Purnananda Mishra:** concept, art direction and review at each stage.
- **AI-assisted:** design production, prototype code, packaging illustration, automated checks and writing, under that direction.

**Tools:** HTML, CSS and JavaScript; Python (tokens, logo and packaging generation); Playwright with Chromium (screen exports and tests); axe-core 4.10.2.

**Limitations:**
- Fictional brand, products and data.
- No user research or usability testing.
- No dermatological, legal or regulatory review.
- Session-only prototype with no backend.
- English only; tested in Chromium only.
