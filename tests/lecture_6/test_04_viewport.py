"""Lecture 6 · 04 — Window size and breakpoints.

Slides "Breakpoints", "Window size · picture / code".
playwright.dev shows the menu button ("Toggle navigation bar") below 997 px.
"""
import pytest
from playwright.sync_api import Browser, Page, expect

URL = "https://playwright.dev/python/"
MENU = "Toggle navigation bar"
# 1 — phone, tablet, desktop
SIZES = [(375, 812), (768, 1024), (1280, 720)]


def test_default_viewport(page: Page):
    """Without settings every Playwright page is 1280 × 720.

    (This test fails on purpose if you run it with --device.)
    """
    assert page.viewport_size == {"width": 1280, "height": 720}


# 4 — three sizes → three runs
@pytest.mark.parametrize("width, height", SIZES)
def test_menu_button(page: Page, width, height):
    # 2 — resize the page we already have
    page.set_viewport_size({"width": width, "height": height})
    page.goto(URL)
    toggle = page.get_by_role("button", name=MENU)
    # 3 — the expected result depends on the size
    if width < 997:
        expect(toggle).to_be_visible()
    else:
        expect(toggle).to_be_hidden()


def test_new_context_with_viewport(browser: Browser):
    """The other way: a new context that is small from the start."""
    context = browser.new_context(viewport={"width": 375, "height": 812})
    page = context.new_page()
    page.goto(URL)
    expect(page.get_by_role("button", name=MENU)).to_be_visible()
    context.close()
