# MoneyMines: Reward Rules (Demonstration Values)

> **Concept notice.** MoneyMines is a self-initiated design concept. Every rate, cap, merchant, person and amount on this page is fictional and exists only to make the interface realistic and internally consistent. **These are not commercial offers.** No money is moved, and no reward is ever paid.

The single source of truth for all numbers shown in screens, exports and the prototype is [`sample-data.json`](sample-data.json). Amounts are stored in paise (integers) and formatted with Indian digit grouping (₹27,742.50).

---

## 1. The four ways to earn

Not every transaction earns a reward. The app always says *which* rule applies, or *why* none does.

| ID | Mechanism | How it works (demo) | Limits | Becomes confirmed |
|----|-----------|---------------------|--------|-------------------|
| **R1** | **Cashback** at partner merchants | 2% of the order value | Minimum order ₹500 · cap ₹100 per order · cap ₹300 per calendar month | After the 14-day return window |
| **R2** | **Fixed bonus** on bills and recharges | ₹10 per successful bill or recharge | Bill must be ₹199 or more · max 3 bonuses per calendar month | When the biller confirms (2 days in demo) |
| **R3** | **Points** on merchant (scan & pay) payments | 1 point per full ₹50 paid | Max 200 points per payment · points expire 12 months after they're earned | When the payment is confirmed |
| **R4** | **Referral** reward | You get ₹50 and your friend gets ₹25 | Friend's first eligible transaction must be ₹500 or more, within 30 days of joining · max 10 rewarded referrals per year | 7 days after the friend's qualifying transaction is confirmed |

### Never eligible
- Transfers between people.
- Failed or cancelled transactions.
- Reversed or refunded transactions. Any pending or confirmed reward from them is reversed.
- Adding money to the wallet.

### Rounding
- Cashback is calculated in paise and rounded **down**.
- Points count only **whole ₹50 steps**, so ₹2,315 earns 46 points, not 46.3.

---

## 2. Reward states

The interface uses a label, an icon and a fill style for every state. Colour is never the only signal.

| State | Meaning | Visual treatment |
|-------|---------|------------------|
| **Pending** | Earned on paper but not yet usable. It can still be reversed. | Dashed outline, clock icon, expected date shown |
| **Confirmed** | Usable for redemption until it expires | Solid fill, lime facet marker, check icon |
| **Reversed** | Taken back because the transaction was refunded or reversed | Struck amount, return-arrow icon, reason shown |
| **Not eligible** | No rule applied | Info icon and a plain-language reason |
| **Expired** | Not used before the expiry date | Muted, "Expired on…" label |

**Design principle: *dashed means not yet yours.*** Pending money is never shown in the same solid style as money the user can actually use.

---

## 3. Keeping balances separate

These five balances are never added together into one "total":

| Balance | Unit | Example (as of 28 Oct 2026, demo) |
|---------|------|-----------------------------------|
| Wallet / account funds | ₹ | ₹12,480.50 |
| Confirmed rewards | ₹ | ₹222.00 |
| Pending rewards | ₹ | ₹120.00 |
| Points | pts (no ₹ sign) | 1,240 pts, plus 3 pending |
| Reversed this month | ₹ (shown in history only) | ₹17.00 |

---

## 4. Converting points (demo)

- **10 points = ₹1** of confirmed rewards.
- Points convert in blocks of **500 points (₹50)**.
- In the demo, a conversion can't be undone, and the review screen says so before confirming.

**Worked example:** 1,240 pts ÷ 500 = 2 whole blocks, so **1,000 pts → ₹100.00**, with 240 pts left over.

---

## 5. Redeeming (simulated)

Only **confirmed rupee rewards** can be redeemed. Points must be converted first.

| Method | Minimum | Rules (demo) | What the demo shows |
|--------|---------|--------------|---------------------|
| Transfer to bank account | ₹250 | Whole rupees only | "Simulated: no bank is connected. In a real product this might take 1–3 working days." |
| In-app benefit | ₹100 | Apply up to ₹100, and no more than 50% of a bill | Bill total before and after, with the reward line itemised |
| Vouchers & gift cards | ₹100 | Fixed values of ₹100, ₹250 or ₹500 from fictional brands | Voucher card marked "Sample voucher, not redeemable" |

All redemptions need at least ₹100 of confirmed rewards. The app shows the gap as a **depth gauge**, never as a countdown.

---

## 6. Worked examples from the sample data

Each of these appears identically on the receipt, the rewards dashboard and reward history.

| Txn | Situation | Calculation | Result |
|-----|-----------|-------------|--------|
| MM-DEMO-06 | Loomhouse order, ₹1,000.00 | ₹1,000.00 × 2% = ₹20.00 | **₹20.00 pending** until 30 Oct |
| MM-DEMO-09 | Ampere Electronics order, ₹6,499.00 | ₹6,499.00 × 2% = ₹129.98 → capped at ₹100.00 (per-order cap) | **₹100.00 pending** until 5 Nov |
| MM-DEMO-05 | Pagewise Books order ₹850.00, later returned | ₹850.00 × 2% = ₹17.00 | **₹17.00 reversed** |
| MM-DEMO-01, 03, 10 | Three bills ≥ ₹199 in October | Fixed ₹10.00 each | **₹30.00 confirmed** |
| MM-DEMO-11 | Fourth bill in October, ₹799.00 | Monthly limit of 3 reached | **Not eligible** (explained) |
| MM-DEMO-02 | Kesar Grocers, ₹2,315.00 | ₹2,315 ÷ ₹50 = 46.30 → 46 pts | **46 pts** |
| MM-DEMO-08 | Tamarind Café, ₹420.00 | ₹420 ÷ ₹50 = 8.40 → 8 pts | **8 pts** |
| MM-DEMO-13 | Kettle & Co., ₹180.00, payment pending | ₹180 ÷ ₹50 = 3.60 → 3 pts | **3 pts pending** |
| MM-DEMO-04 | Transfer to Rohan S., ₹1,500.00 | Transfers aren't eligible | **No reward** (explained) |
| MM-DEMO-07 | Recharge ₹199.00, failed | Payment didn't complete | **No reward**, no money deducted |
| MM-DEMO-12 | Transfer ₹600.00, cancelled | Cancelled by user | **No reward** |
| Referral | Meera K. joined 2 Oct, first transaction ₹640 on 8 Oct | Fixed ₹50.00 | **₹50.00 confirmed** on 15 Oct |

### Balance reconciliation

| | Amount |
|---|---|
| Confirmed rewards brought forward (before October) | ₹142.00 |
| + Bill bonuses (3 × ₹10.00) | ₹30.00 |
| + Referral (Meera K.) | ₹50.00 |
| **= Confirmed rewards** | **₹222.00** |
| Pending: ₹20.00 (Loomhouse) + ₹100.00 (Ampere) | **₹120.00** |
| Bank-transfer minimum ₹250 − ₹222 | **₹28.00 short** |
| After converting 1,000 pts (₹100.00): ₹222 + ₹100 | ₹322.00 |
| After converting the minimum 500 pts (₹50.00): ₹222 + ₹50 | ₹272.00, enough for a bank transfer |

**Expiry notice (calm, not urgent):** ₹40.00 of the brought-forward balance expires on 12 Nov 2026. It's shown as a dated fact with no timer.

Wallet: opening balance on 1 Oct was ₹27,742.50. Successful and pending debits came to ₹15,262.00, giving a closing balance of **₹12,480.50**. Failed, cancelled and reversed transactions are not debited.

---

## 7. Hypothetical scenarios (not part of the snapshot)

| ID | Scenario | Effect shown on screen | Screens |
|----|----------|------------------------|---------|
| HYP-01 | Redeem a ₹100 Loomhouse voucher | Confirmed ₹222.00 → ₹122.00 | S19-redeem-review, S19-redeem-confirmation |
| HYP-02 | Convert 500 pts | Points 1,240 → 740 · confirmed ₹222.00 → ₹272.00 | S15-points-convert-hypothetical |

Both are stored under `hypothetical_scenarios` in `sample-data.json` with `in_snapshot: false`. They are previews of what *would* happen. Redemption history and every other screen still show the 28 Oct snapshot.

**S18 bill preview:** the in-app benefit preview uses an illustrative next bill of ₹1,840.00 (the same amount as October's Metro Power bill) with ₹100.00 of rewards applied, giving ₹1,740.00. It is labelled "Preview only".
