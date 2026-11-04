"""Lecture 6 · 11 — Debugging: Inspector, Trace Viewer, codegen.

Slides "Inspector stops the test like a breakpoint", "The trace is
DevTools after the test failed", "codegen writes the first draft".

From the terminal (PowerShell):
    $env:PWDEBUG=1; uv run pytest tests/lecture_6 -k login_with_cookie
    uv run pytest tests/lecture_6 --tracing retain-on-failure
    uv run playwright show-trace test-results/<test-name>/trace.zip
    uv run playwright codegen --target python-pytest https://www.saucedemo.com
"""
import os
from pathlib import Path

import pytest
from playwright.sync_api import Browser, Page, expect

URL = "https://www.saucedemo.com/"


@pytest.mark.skipif(not os.environ.get("LECTURE6_PAUSE"),
                    reason="demo: $env:LECTURE6_PAUSE=1, then run with --headed")
def test_pause_in_the_middle(page: Page):
    page.goto(URL)
    page.locator("#user-name").fill("standard_user")
    page.pause()   # the Inspector opens: Step over, Resume, Pick locator
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()


def test_trace_file_is_written(browser: Browser, tmp_path: Path):
    """The same trace that --tracing makes, started by hand."""
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    page.goto(URL)
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    expect(page.locator("[data-test='title']")).to_have_text("Products")
    trace = tmp_path / "trace.zip"
    context.tracing.stop(path=trace)
    context.close()
    assert trace.exists() and trace.stat().st_size > 0
    # open it:  uv run playwright show-trace <path>   or  trace.playwright.dev
