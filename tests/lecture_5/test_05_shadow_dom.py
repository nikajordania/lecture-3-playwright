"""Lecture 5 · 05 — Shadow DOM: HTML hidden behind a wall.

Slides "05 · Shadow DOM · picture / code".
The page has two buttons with the same id="my-btn": one in the normal
page, one inside the shadow root of #shadow-host.
CSS and get_by_* locators go through open shadow roots by themselves.
XPath does not.
"""
import pytest
from playwright.sync_api import Error, Page, expect

URL = "https://practice.expandtesting.com/shadowdom"
TEXT = "inside a Shadow DOM"


def test_shadow_dom(page: Page):
    page.goto(URL)
    # 1 — CSS sees both buttons: the page one and the shadow one
    expect(page.locator("#my-btn")).to_have_count(2)
    # 2 — start from the host to pick the inside one
    inside = page.locator("#shadow-host #my-btn")
    expect(inside).to_contain_text(TEXT)
    # 3 — the best choice: role + name, no ids at all
    by_role = page.get_by_role("button", name=TEXT)
    expect(by_role).to_be_visible()
    # 4 — XPath stops at the shadow root: only the light-DOM button
    xpath = page.locator("//button[@id='my-btn']")
    expect(xpath).to_have_count(1)
    expect(xpath).not_to_contain_text(TEXT)


def test_strict_mode_with_duplicate_id(page: Page):
    """Two elements match "#my-btn", so an action on it fails.

    Playwright never guesses which one you meant (strict mode).
    """
    page.goto(URL)
    with pytest.raises(Error, match="strict mode violation"):
        page.locator("#my-btn").click(timeout=3000)
