"""Lecture 6 · 07 — Cookies: read them, bring them, delete them.

Slides "Anatomy of a cookie", "Login with a cookie · picture / code".
Real data from saucedemo.com: after login there is ONE cookie,
session-username = standard_user, and it lives about 10 minutes.
"""
from playwright.sync_api import BrowserContext, Page, expect

URL = "https://www.saucedemo.com"


def test_login_creates_a_cookie(page: Page, context: BrowserContext):
    page.goto(URL)
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    expect(page).to_have_url(URL + "/inventory.html")

    cookie = next(c for c in context.cookies() if c["name"] == "session-username")
    assert cookie["value"] == "standard_user"
    assert cookie["httpOnly"] is False   # JavaScript can read it
    assert cookie["sameSite"] == "Lax"


def test_login_with_cookie(page: Page, context: BrowserContext):
    # 2 — put the cookie in the context BEFORE the first goto
    context.add_cookies([{
        # 1 — name and value copied from DevTools → Application
        "name": "session-username", "value": "standard_user",
        "url": URL,
    }])
    # 3 — no login form: the site trusts the cookie
    page.goto(URL + "/inventory.html")
    title = page.locator("[data-test='title']")
    expect(title).to_have_text("Products")
    page.get_by_role("button", name="Add to cart").first.click()
    # 4 — the backpack (id 4) is now in local storage
    cart = page.evaluate("localStorage.getItem('cart-contents')")
    assert cart == "[4]"


def test_no_cookie_no_inventory(logged_in_page: Page, context: BrowserContext):
    """Test idea "the session ended": delete the cookie and reload."""
    context.clear_cookies()
    logged_in_page.goto(URL + "/inventory.html")
    expect(logged_in_page.locator("[data-test='error']")).to_have_text(
        "Epic sadface: You can only access '/inventory.html' when you are logged in."
    )
