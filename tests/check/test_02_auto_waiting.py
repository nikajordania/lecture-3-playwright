"""03 · Check — auto-waiting, and assert vs expect.

Slides: "click() waits until the element is ready",
        "assert looks once. expect keeps looking."

    actions  (click, fill...)  wait up to 30 s: attached -> visible -> stable -> enabled
    expect()                   re-checks up to 5 s (change it with timeout=...)
    time.sleep(5)              always waits 5 s, ready or not  -> do not use it
"""
import pytest
from playwright.sync_api import Page, expect

THE_INTERNET = "https://the-internet.herokuapp.com"
DYNAMIC_PROPERTIES = "https://demoqa.com/dynamic-properties"


@pytest.mark.slow
def test_hidden_element_appears(page: Page):
    page.goto(f"{THE_INTERNET}/dynamic_loading/1")
    page.get_by_role("button", name="Start").click()
    # "Hello World!" is already in the HTML, only hidden (display: none).
    # to_have_text() would pass at once - check that it becomes VISIBLE.
    # It takes ~5 s and 5 s is the default limit, so give it more time.
    finish = page.locator("#finish")
    expect(finish).to_be_visible(timeout=10_000)
    expect(finish).to_have_text("Hello World!")


@pytest.mark.slow
def test_element_is_added_later(page: Page):
    page.goto(f"{THE_INTERNET}/dynamic_loading/2")
    page.get_by_role("button", name="Start").click()
    # Here the element does not exist at all until the loading ends.
    expect(page.get_by_text("Hello World!")).to_be_visible(timeout=10_000)


def test_fill_waits_until_input_is_enabled(page: Page):
    page.goto(f"{THE_INTERNET}/dynamic_controls")
    page.get_by_role("button", name="Enable").click()

    # The input is still disabled for ~3 s. No sleep needed:
    # fill() waits until the input can be edited, then types.
    text_input = page.locator("#input-example input")
    text_input.fill("Ready")

    expect(text_input).to_have_value("Ready")
    expect(page.locator("#message")).to_have_text("It's enabled!")


@pytest.mark.slow
def test_button_becomes_enabled_and_visible(page: Page):
    page.goto(DYNAMIC_PROPERTIES)
    enable_after = page.locator("#enableAfter")

    expect(enable_after).to_be_disabled()
    expect(enable_after).to_be_enabled(timeout=10_000)
    expect(page.locator("#visibleAfter")).to_be_visible(timeout=10_000)


@pytest.mark.slow
@pytest.mark.xfail(strict=True, reason="assert reads the page only ONCE - the text is not there yet")
def test_assert_looks_once(page: Page):
    page.goto(f"{THE_INTERNET}/dynamic_loading/2")
    page.get_by_role("button", name="Start").click()

    # is_visible() answers right now (no waiting): False -> AssertionError.
    # xfail = "we expect this test to fail" - pytest shows it as XFAIL, not red.
    assert page.get_by_text("Hello World!").is_visible()


@pytest.mark.slow
def test_expect_keeps_looking(page: Page):
    page.goto(f"{THE_INTERNET}/dynamic_loading/2")
    page.get_by_role("button", name="Start").click()

    # The same check with expect(): it retries until the text is there.
    expect(page.get_by_text("Hello World!")).to_be_visible(timeout=10_000)
