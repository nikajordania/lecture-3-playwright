"""Lecture 6 · 03 — One test, three browsers.

Slides "Three browsers · picture / code", "Markers and channels".
The test code does not change; the command does:

    uv run pytest tests/lecture_6/test_03_browsers.py --browser chromium --browser firefox --browser webkit
    uv run pytest tests/lecture_6 --browser-channel chrome     (the real Chrome on this computer)

Once, before the first run:  uv run playwright install
"""
import pytest
from playwright.sync_api import Page, expect

SAUCE = "https://www.saucedemo.com/"


def test_title_in_every_browser(page: Page, browser_name: str):
    """browser_name is a pytest-playwright fixture: chromium, firefox or webkit."""
    page.goto(SAUCE)
    expect(page).to_have_title("Swag Labs")


def test_user_agent_names_the_engine(page: Page, browser_name: str):
    expected = {"chromium": "Chrome", "firefox": "Firefox", "webkit": "Safari"}
    user_agent = page.evaluate("navigator.userAgent")
    assert expected[browser_name] in user_agent, user_agent


@pytest.mark.skip_browser("webkit")
def test_skipped_on_webkit(page: Page, browser_name: str):
    """Shows SKIPPED for webkit. In a real project: write the reason here."""
    assert browser_name != "webkit"


@pytest.mark.only_browser("chromium")
def test_only_on_chromium(page: Page, browser_name: str):
    """Runs only for chromium; firefox and webkit show SKIPPED."""
    assert browser_name == "chromium"
