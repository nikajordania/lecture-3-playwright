"""Lecture 6 · 01 — Console: the test listens to what the page says.

Slides "Console · picture / code".
Listen first (page.on), then goto — the same rule as dialogs in lecture 4.
"""
from playwright.sync_api import Page

SAUCE = "https://www.saucedemo.com/"


def test_page_has_no_js_errors(page: Page):
    messages, crashes = [], []
    # 1 — every console message: log, warning, error
    page.on("console", lambda msg: messages.append(msg))
    # 2 — a JavaScript crash nobody caught
    page.on("pageerror", lambda err: crashes.append(err))
    page.goto(SAUCE)
    # 3 — keep only the red ones
    errors = [m.text for m in messages if m.type == "error"]
    # 4 — on FAIL the report shows the texts
    assert errors == [], errors
    assert crashes == [], crashes


def test_console_error_is_caught(page: Page):
    """Proof that the listener works: we print an error ourselves."""
    messages = []
    page.on("console", lambda msg: messages.append(msg))
    page.goto(SAUCE)
    page.evaluate("console.error('boom from the test')")
    errors = [m.text for m in messages if m.type == "error"]
    assert "boom from the test" in errors


def test_page_crash_is_caught(page: Page):
    """A crash in the page's JavaScript arrives as a "pageerror" event."""
    page.goto(SAUCE)
    with page.expect_event("pageerror") as info:
        page.evaluate("setTimeout(() => { throw new Error('crash!') }, 0)")
    assert "crash!" in str(info.value)
