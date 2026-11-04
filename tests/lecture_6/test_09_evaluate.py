"""Lecture 6 · 09 — page.evaluate: the Console inside a test.

Slides "evaluate() runs JavaScript in the page" and
"A JavaScript click can hide a real bug" (the red slide).
"""
import re

import pytest
from playwright.sync_api import Page, TimeoutError, expect

URL = "https://www.saucedemo.com/"


def test_read_local_storage(logged_in_page: Page):
    logged_in_page.get_by_role("button", name="Add to cart").first.click()
    cart = logged_in_page.evaluate("localStorage.getItem('cart-contents')")
    assert cart == "[4]"


def test_ask_about_one_element(page: Page):
    page.goto(URL)
    button = page.locator("#login-button")
    color = button.evaluate("e => getComputedStyle(e).backgroundColor")
    assert color.startswith("rgb")   # e.g. "rgb(61, 220, 145)"


def test_scroll_to_the_end(logged_in_page: Page):
    logged_in_page.set_viewport_size({"width": 400, "height": 300})
    logged_in_page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    assert logged_in_page.evaluate("window.scrollY") > 0


def test_init_script_runs_before_the_page(page: Page):
    page.add_init_script("window.TEST_MODE = true")
    page.goto(URL)
    assert page.evaluate("window.TEST_MODE") is True


BANNER = """document.body.insertAdjacentHTML('beforeend',
  '<div id="banner" style="position:fixed; inset:0; z-index:9999;' +
  ' background:rgba(14,23,38,.9); color:white">We use cookies. Accept?</div>')"""


def test_js_click_hides_a_bug(page: Page):
    """A banner covers the page. A user cannot click Login — and neither
    can Playwright. A JavaScript click can, so the bug stays hidden."""
    page.goto(URL)
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.evaluate(BANNER)
    login = page.locator("#login-button")

    # the honest click fails, like a real user
    with pytest.raises(TimeoutError):
        login.click(timeout=2000)

    # the JavaScript click "works" — the test would PASS over a real bug
    login.evaluate("e => e.click()")
    expect(page).to_have_url(re.compile("inventory"))
