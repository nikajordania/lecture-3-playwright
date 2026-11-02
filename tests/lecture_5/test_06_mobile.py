"""Lecture 5 · 06 — Mobile: the same page on a phone screen.

Slides "06 · Mobile · picture / code".
playwright.devices["iPhone 13"] is a dict: screen size, pixel ratio,
touch, user agent. ** unpacks it into new_context().
This is emulation, the browser is still desktop Chromium.

Whole suite as a phone, without changing the code:
    uv run pytest tests/lecture_5 --device "iPhone 13"
"""
import pytest
from playwright.sync_api import Browser, Page, Playwright, expect

URL = "https://practice.expandtesting.com/"
MENU = "Toggle navigation"


def test_iphone_menu(playwright: Playwright, browser: Browser):
    # 1 — make the browser an iPhone
    iphone = playwright.devices["iPhone 13"]
    context = browser.new_context(**iphone)
    page = context.new_page()
    page.goto(URL)
    # 2 — only small screens show the menu button
    toggle = page.get_by_role("button", name=MENU)
    expect(toggle).to_be_visible()
    # 3 — the menu is closed; after a click it opens
    menu = page.locator("#main-navbar")
    expect(menu).to_be_hidden()
    toggle.click()
    expect(menu).to_be_visible()
    context.close()


def test_desktop(page: Page):
    # 4 — the normal page fixture is a desktop window: no menu button
    page.goto(URL)
    expect(page.get_by_role("button", name=MENU)).to_be_hidden()


@pytest.mark.parametrize("device", ["iPhone 13", "Pixel 7", "Galaxy S9+"])
def test_menu_button_on_phones(playwright: Playwright, browser: Browser, device):
    """One test, three phones: parametrize from lecture 3."""
    context = browser.new_context(**playwright.devices[device])
    page = context.new_page()
    page.goto(URL)
    expect(page.get_by_role("button", name=MENU)).to_be_visible()
    context.close()
