"""Lecture 6 · 05 — How the browser starts, and contexts.

Slides "One browser, many contexts", "Every context is a fresh incognito
window", "Launch options · picture / code".

Launch options for one run, from the terminal:
    uv run pytest tests/lecture_6 --headed --slowmo 500
"""
import time
from pathlib import Path

from playwright.sync_api import Browser, Playwright, expect

SAUCE = "https://www.saucedemo.com"
COOKIE = {"name": "session-username", "value": "standard_user", "url": SAUCE}


def test_contexts_do_not_share_cookies(browser: Browser):
    """Two users in one test: context A is logged in, context B is not."""
    nika = browser.new_context()
    ana = browser.new_context()
    nika.add_cookies([COOKIE])

    assert len(nika.cookies()) == 1
    assert ana.cookies() == []   # a new context is like a new incognito window

    page_b = ana.new_page()
    page_b.goto(SAUCE + "/inventory.html")
    # Ana has no cookie → SauceDemo sends her back to the login page
    expect(page_b.locator("[data-test='error']")).to_contain_text("only access")
    nika.close()
    ana.close()


def test_launch_options(playwright: Playwright):
    """Start a browser ourselves with the options from the slide."""
    browser = playwright.chromium.launch(
        headless=False,               # 1 — show the window
        slow_mo=300,                  # 3 — wait 300 ms after every action
        args=["--start-maximized"],   # 4 — a Chrome switch
    )
    # maximized only works when Playwright does not force its 1280 × 720
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    page.goto(SAUCE)
    assert page.viewport_size is None
    expect(page).to_have_title("Swag Labs")
    browser.close()


def test_persistent_profile_remembers(playwright: Playwright, tmp_path: Path):
    """The opposite of incognito: a real profile folder keeps cookies."""
    profile = tmp_path / "profile"

    first = playwright.chromium.launch_persistent_context(profile)
    first.add_cookies([{**COOKIE, "expires": time.time() + 600}])
    first.close()

    # a new start with the SAME folder: yesterday's cookie is still there
    second = playwright.chromium.launch_persistent_context(profile)
    names = [c["name"] for c in second.cookies()]
    second.close()
    assert "session-username" in names
