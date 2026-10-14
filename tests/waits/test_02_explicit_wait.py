"""Explicit Wait  ->  Playwright: wait for ONE condition, only where you ask.

Selenium
    WebDriverWait(driver, 10).until(
        expected_conditions.visibility_of_element_located((By.ID, "finish"))
    )

Playwright - three kinds of explicit waits:
    1. expect(locator).to_be_visible(timeout=10_000)    check + wait   (use this first)
    2. locator.wait_for(state="visible", timeout=...)   only wait, no check
       states: "visible", "hidden", "attached", "detached"
    3. page.wait_for_url(), page.wait_for_load_state(),
       page.expect_response(), page.context.expect_page()   page / network events
"""
from playwright.sync_api import Page, expect

THE_INTERNET = "https://the-internet.herokuapp.com"


def test_expect_with_timeout(page: Page):
    # Selenium: WebDriverWait(driver, 10).until(visibility_of_element_located((By.ID, "finish")))
    page.goto(f"{THE_INTERNET}/dynamic_loading/1")
    page.get_by_role("button", name="Start").click()

    expect(page.locator("#finish")).to_be_visible(timeout=10_000)
    expect(page.locator("#finish")).to_have_text("Hello World!")


def test_wait_for_visible_and_hidden(page: Page):
    page.goto(f"{THE_INTERNET}/dynamic_loading/1")
    page.get_by_role("button", name="Start").click()

    loading = page.locator("#loading")  # "Loading..." with a spinner
    loading.wait_for(state="visible")  # the spinner appeared
    loading.wait_for(state="hidden", timeout=10_000)  # ...and went away

    expect(page.locator("#finish")).to_be_visible()


def test_wait_for_detached_and_attached(page: Page):
    page.goto(f"{THE_INTERNET}/dynamic_controls")
    checkbox = page.locator("#checkbox")

    page.get_by_role("button", name="Remove").click()
    checkbox.wait_for(state="detached")  # removed from the HTML

    page.get_by_role("button", name="Add").click()
    checkbox.wait_for(state="attached")  # back in the HTML


def test_selenium_lambda_example(page: Page):
    # Selenium:
    #   wait = WebDriverWait(driver, timeout=10)
    #   wait.until(lambda d: driver.find_element(
    #       By.CSS_SELECTOR, "#checkbox-example #message").is_displayed())
    page.goto(f"{THE_INTERNET}/dynamic_controls")
    page.get_by_role("button", name="Remove").click()

    message = page.locator("#checkbox-example #message")
    message.wait_for(timeout=10_000)  # state="visible" is the default
    expect(message).to_have_text("It's gone!")


def test_wait_for_url_and_load_state(page: Page):
    page.goto(f"{THE_INTERNET}/login")
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()

    page.wait_for_url("**/secure")  # ** = any text before /secure
    page.wait_for_load_state("load")  # "domcontentloaded", "load" or "networkidle"
    expect(page.get_by_role("heading", name="Secure Area")).to_be_visible()


def test_wait_for_a_network_response(page: Page):
    page.goto(f"{THE_INTERNET}/login")
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")

    # Wait for the server's answer WHILE we click.
    with page.expect_response("**/authenticate") as response_info:
        page.get_by_role("button", name="Login").click()

    response = response_info.value
    assert response.request.method == "POST"
    assert "username=tomsmith" in response.request.post_data  # what the form sent
    expect(page).to_have_url(f"{THE_INTERNET}/secure")
