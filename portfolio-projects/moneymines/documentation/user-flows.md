# MoneyMines: Primary User Flows

All flows use the fictional dataset in [`sample-data.json`](sample-data.json) as of **28 Oct 2026**. The same flows appear as **Guided flows** in the prototype (`prototype/index.html`).

## Flow 1: Partner purchase → capped cashback → pending

```
S09 Partners ──► S10 Review ──► S11 Receipt (MM-DEMO-09) ──► S17 Pending ──► S13 Rewards
  "R1 · 2% up to ₹100"   ₹6,499 × 2% = ₹129.98     pending ₹100.00            ₹100 until 5 Nov
                         − ₹29.98 cap = ₹100.00    progress: return window
```
**Design intent:** the cap is shown *before* confirming, not discovered later. The expected reward sits in a dashed box because it isn't usable yet.

## Flow 2: Bill payment after the monthly limit

```
S05 Pay ──► S06 Broadband bill ──► S10 Review ──► S11 Receipt ──► S17 "Not eligible"
  warning on the       "No bonus on this bill: 3 of 3 used.
  Bills option         Next bonus from 1 Nov"
```
**Design intent:** an ineligible payment is explained at the point of choice (S05) and again before paying (S06). The user is never surprised on the receipt.

## Flow 3: Points → conversion → redemption

```
S13 Rewards ──► S15 Points ──► S18 Use rewards ──► S19 Review ──► S19 Simulated confirmation
 ₹222.00          500 pts → ₹50     bank: ₹28 short     voucher ₹100     "Simulated redemption recorded"
 1,240 pts        rewards ₹272      depth gauge          ₹222 → ₹122      sample code DEMO-NOT-VALID
```
**Design intent:** the depth gauge shows the gap to the bank-transfer minimum (₹250) and points to a fix (convert 500 pts). It never uses a countdown. The confirmation says "recorded (simulated)", never "paid".

**Hypothetical scenarios.** S15-points-convert-hypothetical (**HYP-02**) and both S19 screens (**HYP-01**) carry an amber "Hypothetical scenario" banner and a *scenario vs snapshot* table. They are stored under `hypothetical_scenarios` in the dataset with `in_snapshot: false`. Every other screen, including redemption history, keeps the 28 Oct figures (₹222.00 confirmed, 1,240 pts).

## Flow 4: Reversal

```
S12 Activity ──► S11 Receipt (MM-DEMO-05) ──► S17 Reversed
  ₹850.00 struck     paid → returned → refunded      ₹17.00 reversed
```
**Design intent:** a timeline explains the sequence, the refund confirms that money came back, and the reversed reward is struck through rather than hidden.

## Flow 5: Transaction outcomes (receipts)

| State | Screen | What the user learns first |
|-------|--------|----------------------------|
| Successful | `S11-receipt-09`, `S11-receipt-06` | Demo payment complete, how the reward was calculated, and when it confirms |
| Pending | `S11-receipt-13` | Waiting for the merchant; nothing is deducted if it doesn't go through |
| Failed | `S11-receipt-07` | **No money was deducted**, with try again or get help |
| Cancelled | `S11-receipt-12` | **Nothing was sent**; the wallet is unchanged |
| Reversed | `S11-receipt-05` | Refunded to the wallet, and the cashback reversed |

Every receipt carries a "Simulated" chip next to the status chip.

## Flow 6: First run
S01 (3 cards: pay as usual · dashed means not yet yours · every reward shows its working) → S02 phone → S02 code (demo code 246810; S02-otp-error is the mismatch state) → S03 loading (auto-advances) → S03 Home.

## Flow 7: Referrals & profile
S22 Profile → S16 Referrals (Meera K. rewarded ₹50.00 · Kabir D. joined, needs ₹500+ by 20 Nov · Isha R. invited) → S14 Reward terms.

## No dead ends
Every button and tab leads to a screen. Actions outside the concept's scope (share, add money, settings toggles, request a new code, change contact) show a short in-phone note explaining that they aren't part of the demo. Each receipt has **Done** (→ Home), and any receipt with a pending, reversed or ineligible outcome links to S17.
