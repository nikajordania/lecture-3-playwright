"""Lecture 6 · codegen with your own setup (slide "page.pause() starts
recording from your code").

Not a test: pytest does not collect this file (no test_ prefix).
Run it:
    uv run python tests/lecture_6/codegen_custom_setup.py

The browser opens with our settings and the Playwright Inspector.
Press "Record" in the Inspector and click on the page: the code appears.
Close the browser to finish.
"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # 1 — you must see the window to record
    browser = p.chromium.launch(headless=False)
    # 2 — any context options: language, size, cookies, storage_state …
    context = browser.new_context(locale="ka-GE")
    # 3 — something the codegen flags cannot do: block all .jpg pictures
    context.route("**/*.jpg", lambda route: route.abort())
    page = context.new_page()
    page.goto("https://demoqa.com/books")
    # 4 — the Inspector opens here: Record, Pick locator, Assert …
    page.pause()
    browser.close()
