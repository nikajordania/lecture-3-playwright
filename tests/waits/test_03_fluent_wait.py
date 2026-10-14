"""Fluent Wait  ->  Playwright: choose how often to check, ignore errors while waiting.

Selenium (Java style, the idea is the same in Python)
    Wait<WebDriver> wait = new FluentWait<>(driver)
        .withTimeout(Duration.ofSeconds(10))      // how long in total
        .pollingEvery(Duration.ofMillis(500))     // how often to check
        .ignoring(NoSuchElementException.class);  // errors that mean "not yet"

Playwright
    expect() and wait_for() ARE already fluent waits: they re-check
    many times (first fast, then about every 1 s) and ignore "not found yet".
    You almost never need more. When you do:
        page.wait_for_function(js, polling=500, timeout=10_000)
        your own small polling loop - see fluent_wait() below
"""
from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

DYNAMIC_LOADING_1 = "https://the-internet.herokuapp.com/dynamic_loading/1"
DYNAMIC_LOADING_2 = "https://the-internet.herokuapp.com/dynamic_loading/2"


def fluent_wait(page: Page, condition, timeout_ms=10_000, poll_ms=500, ignoring=()):
    """Call condition() every poll_ms until it returns a truthy value.

    Errors listed in `ignoring` mean "not ready yet - try again".
    After timeout_ms -> TimeoutError, like Selenium's FluentWait.
    """
    waited = 0
    while waited <= timeout_ms:
        try:
            result = condition()
            if result:
                return result
        except ignoring:
            pass  # like .ignoring(NoSuchElementException.class)
        page.wait_for_timeout(poll_ms)  # pause; never time.sleep() in Playwright tests
        waited += poll_ms
    raise TimeoutError(f"condition was not true after {timeout_ms} ms")


def test_wait_for_function_with_polling(page: Page):
    page.goto(DYNAMIC_LOADING_1)
    page.get_by_role("button", name="Start").click()

    # JavaScript runs in the browser every 500 ms until it returns true.
    page.wait_for_function(
        "() => getComputedStyle(document.querySelector('#finish')).display !== 'none'",
        polling=500,
        timeout=10_000,
    )
    expect(page.locator("#finish")).to_have_text("Hello World!")


def test_own_fluent_wait_ignoring_errors(page: Page):
    page.goto(DYNAMIC_LOADING_2)
    page.get_by_role("button", name="Start").click()

    # inner_text(timeout=200): if the element is not there yet it raises
    # TimeoutError after 0.2 s. fluent_wait() ignores it and tries again.
    text = fluent_wait(
        page,
        lambda: page.locator("#finish h4").inner_text(timeout=200),
        timeout_ms=10_000,
        poll_ms=500,
        ignoring=(PlaywrightTimeoutError,),
    )

    assert text == "Hello World!"


def test_expect_is_already_a_fluent_wait(page: Page):
    page.goto(DYNAMIC_LOADING_2)
    page.get_by_role("button", name="Start").click()

    # Same result, one line: retries, ignores "not found yet", 10 s limit.
    expect(page.locator("#finish h4")).to_have_text("Hello World!", timeout=10_000)
