"""Lecture 6 · 08 — storage_state: log in once, reuse the session.

Slide "Log in once, save it, reuse it".
state.json is a key to the account: never commit it (.gitignore).
Here it goes to a temporary folder that pytest cleans up.
"""
import json

import pytest
from playwright.sync_api import Browser, expect

URL = "https://www.saucedemo.com"


@pytest.fixture(scope="module")
def state_file(browser: Browser, tmp_path_factory):
    """Logs in ONCE for the whole file and saves cookies + local storage."""
    context = browser.new_context()
    page = context.new_page()
    page.goto(URL)
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    page.get_by_role("button", name="Add to cart").first.click()
    path = tmp_path_factory.mktemp("auth") / "state.json"
    context.storage_state(path=path)   # 1 — save
    context.close()
    return path


def test_state_file_has_cookie_and_cart(state_file):
    state = json.loads(state_file.read_text())
    names = [c["name"] for c in state["cookies"]]
    assert "session-username" in names
    storage = state["origins"][0]["localStorage"]
    assert {"name": "cart-contents", "value": "[4]"} in storage


def test_starts_logged_in(browser: Browser, state_file):
    # 2 — load: the new context starts with the saved cookies and storage
    context = browser.new_context(storage_state=state_file)
    page = context.new_page()
    page.goto(URL + "/inventory.html")
    expect(page.locator("[data-test='title']")).to_have_text("Products")
    expect(page.locator("[data-test='shopping-cart-badge']")).to_have_text("1")
    context.close()
