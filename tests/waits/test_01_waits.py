"""Waits: three ways to deal with a slow page.

    action  (click, fill...)  waits by itself until the element is ready (30 s)
    assert                    looks ONCE   -> wait first with wait_for(), then assert
    expect                    keeps looking -> waits by itself (default 5 s, here timeout=10_000)

    time.sleep(5)             always waits 5 s, ready or not  -> do not use it
"""
from playwright.sync_api import Page, expect

THE_INTERNET = "https://the-internet.herokuapp.com"
LOADING = f"{THE_INTERNET}/dynamic_loading/1"  # "Hello World!" is hidden, shows up ~5 s after Start


def test_action_waits_until_input_is_enabled(page: Page):
    page.goto(f"{THE_INTERNET}/dynamic_controls")
    page.get_by_role("button", name="Enable").click()

    # The input is disabled for ~3 s. fill() waits until it can be edited.
    text_input = page.locator("#input-example input")
    text_input.fill("Ready")

    expect(text_input).to_have_value("Ready")


def test_assert_after_wait_for(page: Page):
    page.goto(LOADING)
    page.get_by_role("button", name="Start").click()
    finish = page.locator("#finish")

    # assert finish.is_visible() right here would fail: it checks only once.
    finish.wait_for(state="visible", timeout=10_000)

    assert finish.is_visible()
    assert finish.inner_text() == "Hello World!"


def test_expect_waits_by_itself(page: Page):
    page.goto(LOADING)
    page.get_by_role("button", name="Start").click()
    finish = page.locator("#finish")

    expect(finish).to_be_visible(timeout=10_000)
    expect(finish).to_have_text("Hello World!")
