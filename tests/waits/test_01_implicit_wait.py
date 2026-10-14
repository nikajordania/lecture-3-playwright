"""Implicit Wait  ->  Playwright: auto-waiting + default timeouts.

Selenium
    driver.implicitly_wait(10)
    Every find_element() waits up to 10 s, then NoSuchElementException.
    Set once, works for all elements of this driver.

Playwright has NO implicit wait - it does not need one:
    every action (click, fill...) waits by itself        default 30 s
    every expect() check retries by itself               default 5 s

The closest thing to implicitly_wait() is changing these defaults:
    page.set_default_timeout(10_000)              actions, wait_for(), wait_for_url()...
    page.set_default_navigation_timeout(10_000)   goto(), reload(), wait_for_url()
    expect.set_options(timeout=10_000)            every expect() in the run

Selenium: implicit 30 s + explicit 10 s can add up to 40 s.
Playwright: one call has ONE timeout. A timeout= on the call wins,
otherwise the default is used. Nothing adds up.
"""
import pytest
from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

DYNAMIC_LOADING_2 = "https://the-internet.herokuapp.com/dynamic_loading/2"  # "Hello World!" after ~5 s
DYNAMIC_CONTROLS = "https://the-internet.herokuapp.com/dynamic_controls"  # input enabled after ~3 s


def test_actions_wait_without_any_wait_code(page: Page):
    page.goto(DYNAMIC_CONTROLS)
    page.get_by_role("button", name="Enable").click()

    # Selenium would need a wait here. Playwright: fill() waits by itself
    # until the input is visible, enabled and editable (up to 30 s).
    page.locator("#input-example input").fill("no wait code")

    expect(page.locator("#input-example input")).to_have_value("no wait code")


def test_default_timeout_too_short_fails(page: Page):
    # Like implicitly_wait(2): from now on this page waits max 2 s.
    page.set_default_timeout(2_000)
    page.goto(DYNAMIC_LOADING_2)
    page.get_by_role("button", name="Start").click()

    # The text needs ~5 s, the page waits only 2 s -> TimeoutError
    with pytest.raises(PlaywrightTimeoutError):
        page.get_by_text("Hello World!").wait_for()


def test_timeout_of_the_call_wins(page: Page):
    page.set_default_timeout(2_000)  # the default for this page
    page.goto(DYNAMIC_LOADING_2)
    page.get_by_role("button", name="Start").click()

    # timeout= on this call replaces the default (it is not 2 s + 10 s).
    page.get_by_text("Hello World!").wait_for(timeout=10_000)


@pytest.fixture
def expect_waits_10s():
    """Change the expect() default for ONE test, then put it back.

    expect.set_options() is global: without the reset every later test
    in the run would also wait 10 s.
    """
    expect.set_options(timeout=10_000)
    yield
    expect.set_options(timeout=5_000)  # 5 s is Playwright's default


def test_global_expect_timeout(page: Page, expect_waits_10s):
    page.goto(DYNAMIC_LOADING_2)
    page.get_by_role("button", name="Start").click()

    # No timeout= here: the 10 s from the fixture is used.
    expect(page.get_by_text("Hello World!")).to_be_visible()
