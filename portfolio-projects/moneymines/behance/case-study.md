# MoneyMines: A Rewards App That Shows Its Working

**Self-initiated concept · Brand identity, UX and UI design · 2026**
**Concept & art direction: Purnananda Mishra**

> MoneyMines is fictional. No bank, UPI, payment gateway or financial API is connected. Every rate, merchant, person and amount is demonstration data, and no money moves. No user research or usability testing was carried out. The users and problems below are design assumptions, stated as such.

---

## 1. Overview

MoneyMines is an everyday payments app concept in which *some* transactions earn rewards through four mechanisms: partner cashback, fixed bill bonuses, scan-and-pay points and referrals. The deliverables are:
- a brand identity
- a token-based design system
- 51 connected mobile screens and states
- a clickable browser prototype
- documented reward rules that produce every number shown.

## 2. The design problem

Reward features in payment apps often rely on patterns that make money harder to understand. This project treats them as **assumptions to design against**, not research findings:

- one headline balance that mixes real funds, pending cashback and points
- rules that surface only after paying, or never
- urgency mechanics (countdowns, streaks, celebratory language) that encourage extra spending
- pending rewards that look the same as money the user can use.

**Objectives**
1. Show eligibility *before* a payment is made.
2. Keep wallet funds, confirmed rewards, pending rewards and points visibly separate.
3. Place the calculation next to every reward amount.
4. Represent pending, reversed and ineligible outcomes truthfully.
5. Make redemption thresholds and rules obvious.
6. Meet WCAG 2.2 AA and never use colour alone to carry meaning.

## 3. Research assumptions & representative users

No interviews were conducted. These three profiles are illustrative and were used to keep decisions concrete:

| Profile | Context | Representative question |
|---|---|---|
| Bill payer | Monthly household bills and recharges | "Will this bill get the bonus, or did I use them up?" |
| Everyday shopper | Scan & pay at local shops and cafés | "How many points did that coffee earn, and why not more?" |
| Occasional online buyer | Partner orders (electronics, clothing) | "When does this cashback actually become mine? What if I return it?" |

**Validation that a real project would need:** comprehension testing of the dashed-pending pattern, screen-reader testing of amounts and statuses, and compliance review of the reward terms.

## 4. Key decisions

| Decision | Why |
|---|---|
| **Dashed means not yet yours.** Pending rewards are outlined, never filled. | Separates "might become money" from "is money" without relying on colour. |
| **Balances never merge.** Wallet, confirmed, pending and points sit side by side, with no grand total. | A single total would overstate what the user can actually spend. |
| **Every reward explains itself.** Rate, cap, rule ID and result appear wherever an amount appears. | E.g. ₹6,499.00 × 2% = ₹129.98 → capped at ₹100.00. The cap is visible before paying. |
| **Eligibility up front.** The Pay chooser and bill screen say when no reward applies. | The 4th October bill shows "No bonus on this bill" *before* Review, not after. |
| **Calm over urgent.** Expiry is a date ("₹40.00 expires on 12 Nov"), never a timer. No streaks, no confetti. | Avoids pressure to spend or redeem. |
| **Thresholds as depth gauges.** Bank transfer shows "₹28.00 more needed" plus one way to close the gap. | Shows the gap as information, not urgency. |
| **Simulated, and says so.** "Confirm demo payment", a Simulated chip on every receipt, and sample voucher code "DEMO-NOT-VALID". | Nothing in the concept can be mistaken for a real payout. |
| **Identity: Strike.** Two shafts lead down to a lime facet. The facet doubles as the reward marker in the UI. | The brand mark and the interface share one symbol for "a confirmed reward". |

## 5. Information architecture & primary flows

Five tabs: Home · Activity · **Pay** (centre) · Rewards · Profile. Onboarding and sign-in come first.

1. **Partner purchase → capped cashback:** Partners → Review (expected ₹100.00 after cap) → Receipt (pending until 5 Nov) → Pending & eligibility → Rewards.
2. **Bill after the monthly limit:** Pay (limit flagged) → Bill (no-bonus explained) → Review → Receipt (not eligible, with a link to "Why no reward?").
3. **Points → redemption:** Points (1,240 pts) → conversion preview (HYP-02) → Use rewards → voucher review (HYP-01) → simulated confirmation → history.
4. **Reversal:** Notification → Receipt (paid → returned → refunded; ₹17.00 cashback reversed).
5. **Transfer:** Send → Review → Receipt, labelled as not earning rewards at every step.

## 6. Reward transparency: the 28 October snapshot

All screens read from one dataset (`documentation/sample-data.json`).

| Balance | Amount |
|---|---|
| Wallet · account funds | ₹12,480.50 |
| Confirmed rewards | ₹222.00 (₹142.00 brought forward + ₹30.00 bill bonuses + ₹50.00 referral) |
| Pending rewards | ₹120.00 (Loomhouse ₹20.00 + Ampere ₹100.00) |
| Points | 1,240 pts (+3 pending) |
| Reversed in October | ₹17.00 (Pagewise Books return) |

**Hypothetical scenarios.** Two demo flows show what *would* happen and are labelled on screen as hypothetical:
- **HYP-01:** a ₹100 voucher redemption (₹222.00 → ₹122.00)
- **HYP-02:** converting 500 pts (₹222.00 → ₹272.00)

They are stored separately in the dataset with `in_snapshot: false` and never change the 28 October figures. Redemption history notes HYP-01 but does not list it.

## 7. Edge cases & states

Every transaction outcome leads with *what happened*, *whether money moved*, and *what to do next*:

| State | First message |
|---|---|
| Successful | "Demo payment successful", plus the calculation and when the reward confirms |
| Pending | "Waiting for the merchant", and nothing is deducted if it doesn't complete |
| Failed | "No money was deducted", with try again or get help |
| Cancelled | "Nothing was sent", and the wallet is unchanged |
| Reversed | A timeline: paid → returned → refunded, with the cashback reversed |

Also designed: skeleton loading, empty states (activity filter, first-use rewards, referrals, redemption history, notifications), a field validation error and an OTP error.

## 8. Accessibility

- 19 colour pairs checked programmatically. All text pairs pass AA (lowest used: 4.9:1). Borders and focus rings pass the 3:1 non-text rule.
- Status always appears as a label, an icon and colour. Pending also gets a dashed outline.
- 16 px minimum body text, 48 px minimum touch targets, and tabular figures with right-aligned amounts.
- Lime is never used for text on light surfaces.
- Reduced-motion tokens set all transitions to 0 ms.
- Landmarks, labelled icon buttons and switch roles are used in the screen markup.
- Not yet tested with assistive-technology users.

## 9. Visual identity & design system

- **Mark:** Strike, with light, dark and one-colour versions and a 1024 px app icon.
- **Wordmark:** Space Grotesk, with the facet replacing the dot of the *i*.
- **Colour:** Forest, Charcoal and Paper, with Lime rationed to rewards only.
- **Type:** Space Grotesk for headings and amounts (tabular figures); Inter for reading. Both are SIL OFL.
- **System:** 4-pt spacing, radius, elevation and motion tokens (JSON + CSS), 30 icons on a 24 px grid, and component specs.
- **Graphic language:** survey-line contours, a core-sample strata chart and a depth gauge.

## 10. Tools, contribution & limitations

**Contribution:**
- **Purnananda Mishra:** concept, brief, art direction, and review and approval at every stage.

**Tools:** HTML/CSS (screens, boards, slides); Python (data generation, logo geometry, rendering); Chromium via Playwright (exports and automated checks); fontTools (outlined logo type).

**Limitations:**
- Fictional data; no real integrations.
- No user research or usability testing.
- No legal or compliance review.
- Light theme only; Latin script only.
- The prototype is a click-through of static screens, not production code.
- Screens are HTML/CSS, not native Figma files.
