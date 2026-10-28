# MoneyMines: Screen Map & Information Architecture

Frame: 390 × 844 (mobile). Each screen has an ID that is reused in file names (`design/screens/S07-merchant-payment.svg`), exports and the prototype.

## Navigation model

A bottom bar with five slots. **Pay** sits in the centre because it is the most common action, and every reward starts with a transaction.

```
┌──────────┬──────────┬──────────┬──────────┬──────────┐
│   Home   │ Activity │  ◆ Pay   │ Rewards  │ Profile  │
└──────────┴──────────┴──────────┴──────────┴──────────┘
```

```
Onboarding ─ Sign up / Log in
     │
   Home ──────────────┬─────────────────┬────────────────┬──────────────┐
     │                │                 │                │              │
  Wallet (S04)    Activity (S12)     Pay (S05)       Rewards (S13)   Profile (S22)
                      │                 │                │              │
                 Receipt (S11)   ┌──────┼──────┬──────┐  ├ Offers (S14) ├ Notifications (S21)
                                 S06    S07    S08    S09├ Points (S15)  └ Help & rules
                               Bills Merchant Transfer Shop├ Referrals (S16)
                                 └──────┴──────┴──────┘  ├ Pending & eligibility (S17)
                                    Review (S10)         └ Redeem (S18) → Review (S19)
                                         │                               └ History (S20)
                                    Receipt (S11)
```

## Screen inventory

Stage key: **3** means built in Stage 3 (core), **4** means built in Stage 4 (remaining).

| ID | Screen | Purpose | Key content (from `sample-data.json`) | States to design | Stage |
|----|--------|---------|----------------------------------------|------------------|-------|
| S01 | Welcome & onboarding | Set honest expectations | 3 cards: *Pay as usual · See which payments earn · Track pending to confirmed*. Concept notice on the first card | — | 4 |
| S02 | Sign up / log in | Concept of phone and OTP entry | Phone field, demo OTP, "Demo: no SMS is sent" | Error: wrong OTP | 4 |
| S03 | Home dashboard | One glance: money vs rewards | Wallet ₹12,480.50 · Confirmed ₹222.00 · Pending ₹120.00 (dashed) · 1,240 pts · quick actions · recent activity | Loading (skeleton), first-use empty | 3 |
| S04 | Account & wallet | Account funds only | Balance, demo top-up, monthly debits ₹15,262.00 | — | 4 |
| S05 | Pay: action selector | Choose transaction type | Bills & recharge · Scan & pay merchant · Send to a person · Shop partners. Each shows which reward rule applies, or "No rewards on transfers" | — | 3 |
| S06 | Bill payment & recharge | Pay a bill | Biller, amount, *"Bonus ₹10: 3rd of 3 this month"* or the limit-reached explanation | Validation error | 3 |
| S07 | Merchant payment | Scan & pay | Merchant, amount ₹420.00, live points preview "8 pts (whole ₹50 steps)" | — | 3 |
| S08 | Transfer to a person | Send money | Contact, amount, clear "Transfers don't earn rewards" | Cancelled state | 3 |
| S09 | Partner shopping | Browse partner offers | Loomhouse, Ampere, Pagewise: 2% up to ₹100, min ₹500 | Offer unavailable | 4 |
| S10 | Review & demo confirmation | Last check before acting | Amount, fee ₹0.00 (demo), reward line, "Simulated: no money will move" | Processing | 3 |
| S11 | Receipt & details | Proof plus reward calculation | Status chip, ID MM-DEMO-09, calc "₹6,499.00 × 2% = ₹129.98 → capped at ₹100.00", expected 5 Nov | Success · Pending · Failed · Cancelled · Reversed | 3 |
| S12 | Transaction history & filters | Find anything | 13 October transactions, filters by type, status and reward | Empty filter result, loading | 3 |
| S13 | Rewards dashboard | The "mine" | Confirmed ₹222.00, pending ₹120.00, points 1,240, core-sample chart of earnings by rule | First-use empty | 3 |
| S14 | Cashback & bonus offer details | Read the terms | Rate, caps, minimums, expiry, the rules that exclude a transaction | — | 4 |
| S15 | Points & conversion | Convert transparently | 1,240 pts, 10 pts = ₹1, blocks of 500, "1,000 pts → ₹100.00, 240 left" | Below 500 pts | 3 |
| S16 | Referrals | Invite and track | Meera rewarded ₹50 · Kabir joined (needs ₹500 by 20 Nov) · Isha invited | No referrals yet | 4 |
| S17 | Pending & eligibility | Explain *why* | Pending ₹120.00 with dates; not-eligible list with reasons | — | 3 |
| S18 | Redemption method selector | Choose how to use rewards | Bank (needs ₹28 more: depth gauge) · In-app · Vouchers | Below minimum | 3 |
| S19 | Redemption review & simulated confirmation | Confirm without implying payout | Amount, method, "Simulated: nothing will be paid" | Processing (simulated) | 3 |
| S20 | Redemption history | Past uses | Voucher ₹100.00 (Issued, simulated), in-app ₹50.00 (Applied, simulated) | Empty | 4 |
| S21 | Notifications | Reward updates, no hype | "₹10.00 bonus confirmed", "₹17.00 cashback reversed: order returned", expiry notice for 12 Nov | Empty | 4 |
| S22 | Profile, preferences, security, help | Control and trust | Demo persona, notification toggles, app lock, reward rules link, concept notice | — | 4 |

### System states (designed as reusable patterns)
- **Loading:** skeletons shaped like the final content. No spinners on the home screen.
- **Empty:** a short sentence, one action, and the survey-line illustration.
- **Error:** what happened, whether money moved ("No money was deducted"), and what to do next.
- **Ineligible and pending explanations:** inline info rows that link to S17.

## Key journeys (detailed flows come in Stage 3)

1. **Partner purchase to cashback:** S05 → S09 → S10 → S11 (pending ₹100.00, capped) → S13 → S17
2. **Bill payment at the monthly limit:** S05 → S06 (limit explained *before* paying) → S10 → S11 (not eligible)
3. **Points to redemption:** S13 → S15 (convert 500 pts → ₹50) → S18 (bank now available: ₹272.00) → S19 → S20
4. **Reversal:** S21 notification → S11 (reversed, ₹17.00) → S17
5. **Referral:** S13 → S16 → share sheet (demo)
