# MoneyMines prototype: how to open it

The prototype is a browser viewer around the real screen files in `../design/screens/`. It needs no install, no internet and no server.

## Open it
1. On GitHub, open the `moneymines-concept` branch and choose **Code → Download ZIP**.
2. Unzip the file. Keep the folder structure exactly as it is: the prototype loads screens from `design/screens/`.
3. Open `portfolio-projects/moneymines/prototype/index.html` in **Chrome, Edge or Firefox**. Double-clicking it is enough.

> Opening `index.html` straight from the GitHub website won't work, because GitHub shows the code rather than running it. Use the downloaded copy.

## Use it
- **Tap inside the phone** to use the app. Every button and tab leads to a screen.
- **Guided flows** (left panel) jump to the start of each journey. The step chips under the phone show where you are in that flow and let you jump between steps.
- **States** (left panel) open loading, empty, error and receipt-state variants that a normal tap path wouldn't reach.
- **Back** steps back one screen. **Restart** returns to the first onboarding card.
- Actions outside the concept's scope (share, add money, change settings, request a new code) show a short note at the bottom of the phone instead of a dead link.

## What it is not
- No data is entered, stored or sent. All screens are pre-designed from `documentation/sample-data.json` (28 Oct 2026 snapshot).
- The ₹100 voucher (HYP-01) and the 500-point conversion (HYP-02) are **hypothetical** previews. They are labelled on screen and never change the snapshot.
- It is a design prototype, not production code.

## Single screens
Any file in `design/screens/` also opens on its own in a browser, and links between screens still work.
