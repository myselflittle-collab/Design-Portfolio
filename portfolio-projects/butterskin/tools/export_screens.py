"""Exports screens straight from the prototype (single source of truth).
Run from the butterskin folder:  python3 tools/export_screens.py
Needs Python Playwright with Chromium."""
import json, os
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = f"file://{ROOT}/prototype/index.html"

# id, route, title, (optional) action to perform before capture
SCREENS = [
    ("01-welcome-1", "#/welcome/1", "Welcome · 1 of 3"),
    ("02-welcome-2", "#/welcome/2", "Welcome · 2 of 3"),
    ("03-welcome-3", "#/welcome/3", "Welcome · 3 of 3"),
    ("04-personalise", "#/setup", "Personalise (optional)"),
    ("05-home", "#/home", "Home"),
    ("06-shop", "#/shop", "Shop all"),
    ("07-shop-treat", "#/shop?cat=treat", "Shop · category"),
    ("08-shop-focus", "#/shop?focus=1&sort=price-asc", "Shop · focus filter, sorted"),
    ("09-shop-no-results", "#/shop?q=retinol", "Shop · no results"),
    ("10-product", "#/product/dewdrop-hydration-serum", "Product detail"),
    ("11-product-ingredients", "#/product/butter-balm-cream", "Product detail · ingredients", "scroll-ingredients"),
    ("12-added-to-bag", "#/product/butter-balm-cream", "Added to bag dialog", "add"),
    ("13-bag", "#/bag", "Shopping bag"),
    ("14-bag-empty", "#/bag?demo=empty", "Shopping bag · empty"),
    ("15-checkout", "#/checkout", "Demo checkout"),
    ("16-checkout-error", "#/checkout?demo=error", "Demo checkout · validation"),
    ("17-order", "#/order", "Demo order confirmation"),
    ("18-wishlist", "#/wishlist", "Wishlist"),
    ("19-wishlist-empty", "#/wishlist?demo=empty", "Wishlist · empty"),
    ("20-routine-am", "#/routine", "Routine · morning"),
    ("21-routine-pm", "#/routine?time=PM", "Routine · evening"),
    ("22-journal", "#/journal", "Skin journal"),
    ("23-journal-new", "#/journal/new", "New note"),
    ("24-journal-error", "#/journal/new?demo=error", "New note · validation"),
    ("25-account", "#/account", "Account & skin profile"),
    ("26-about", "#/about", "About this concept"),
    ("27-home-checkin", "#/home", "Home · check-in confirmation", "checkin"),
]
DESKTOP = ["05-home", "06-shop", "10-product", "13-bag", "15-checkout", "20-routine-am", "22-journal", "25-account"]


def capture(page, sid, route, action=None):
    page.goto("about:blank"); page.goto(URL + route); page.wait_for_timeout(250)
    page.evaluate("document.fonts.ready")
    if action == "checkin":
        page.click('[data-checkin="A little dry"]'); page.wait_for_timeout(300)
        page.evaluate("document.querySelector('.checkin').scrollIntoView({block:'center'})")
    if action == "add":
        page.click("#pdpAdd"); page.wait_for_timeout(300)
    if action == "scroll-ingredients":
        page.evaluate("document.querySelectorAll('details.acc')[2].scrollIntoView({block:'start'});window.scrollBy(0,-120)")
    page.mouse.move(0, 0)
    if action != "add":
        page.evaluate("document.activeElement && document.activeElement.blur && document.activeElement.blur()")
    page.wait_for_timeout(120)


def run():
    out_m, out_f, out_d = (f"{ROOT}/exports/screens/mobile", f"{ROOT}/exports/screens/mobile-full", f"{ROOT}/exports/screens/desktop")
    for d in (out_m, out_f, out_d):
        os.makedirs(d, exist_ok=True)
    manifest = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        m = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=3)
        for s in SCREENS:
            sid, route, title = s[:3]; act = s[3] if len(s) > 3 else None
            capture(m, sid, route, act)
            m.screenshot(path=f"{out_m}/{sid}.png")
            if act not in ("add", "scroll-ingredients", "checkin"):
                m.screenshot(path=f"{out_f}/{sid}-full.png", full_page=True)
            manifest.append({"id": sid, "route": route, "title": title})
        dk = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        for s in SCREENS:
            if s[0] in DESKTOP:
                capture(dk, s[0], s[1]); dk.screenshot(path=f"{out_d}/{s[0]}-desktop.png")
        b.close()
    json.dump(manifest, open(f"{ROOT}/exports/screens/manifest.json", "w"), indent=1)
    print("exported", len(SCREENS), "mobile,", len(DESKTOP), "desktop")


if __name__ == "__main__":
    run()
