"""Lecture 5 · 03 — Basic auth: the browser asks for a password.

Slides "03 · Basic auth · picture / code".
The sign-in window is drawn by the browser, it is not HTML and not a
JavaScript alert. No locator can reach it. Give the login and the
password to the browser context BEFORE the page opens.

In a real project read the password from an environment variable:
    os.environ["STAGING_PASSWORD"]
"""
from playwright.sync_api import Browser, Page, expect

URL = "https://the-internet.herokuapp.com/basic_auth"


def test_basic_auth(browser: Browser):
    # 2 — a fresh browser context with the credentials inside
    context = browser.new_context(
        http_credentials={"username": "admin", "password": "admin"}
    )
    page = context.new_page()
    # 3 — no sign-in window: the page opens at once
    page.goto(URL)
    expect(page.get_by_text("Congratulations!")).to_be_visible()
    context.close()


def test_no_credentials(page: Page):
    # 1 — no locator can reach the sign-in window
    # 4 — goto returns the response: the server says 401 Unauthorized
    response = page.goto(URL)
    assert response is not None
    assert response.status == 401


def test_wrong_password(browser: Browser):
    context = browser.new_context(
        http_credentials={"username": "admin", "password": "wrong"}
    )
    page = context.new_page()
    response = page.goto(URL)
    assert response is not None
    assert response.status == 401
    context.close()
