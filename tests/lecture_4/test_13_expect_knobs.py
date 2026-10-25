"""Part 3 · expect combinations. Slide "Six knobs on every expect"."""
import re

from playwright.sync_api import Page, expect

THE_INTERNET = "https://the-internet.herokuapp.com"


def test_not(page: Page):
    page.goto(f"{THE_INTERNET}/login")
    flash = page.locator("#flash")
    expect(flash).not_to_be_visible()  # no message before we log in


def test_timeout(page: Page):
    page.goto(f"{THE_INTERNET}/dynamic_loading/1")
    page.get_by_role("button", name="Start").click()
    finish = page.locator("#finish")
    expect(finish).to_be_visible(timeout=10_000)  # ~5 s to load, default limit is 5 s


def test_regex(page: Page):
    page.goto(f"{THE_INTERNET}/login")
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(re.compile("secure"))


def test_list_of_texts(page: Page):
    page.goto(f"{THE_INTERNET}/tables")
    last_names = page.locator("#table1 tbody td:first-child")
    expect(last_names).to_have_text(["Smith", "Bach", "Doe", "Conway"])  # count + order + texts


def test_filter_and_count(page: Page):
    page.goto(f"{THE_INTERNET}/tables")
    rows = page.locator("#table1 tbody tr")
    expect(rows.filter(has_text="Jason")).to_have_count(1)


def test_message_and_ignore_case(page: Page):
    page.goto(f"{THE_INTERNET}/login")
    heading = page.get_by_role("heading", level=2)
    expect(heading, "must be the login page") \
        .to_have_text("login page", ignore_case=True)
