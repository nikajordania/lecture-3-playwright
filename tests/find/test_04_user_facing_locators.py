"""01 · Find — locators a user would understand.

Slide: "Locator ladder":  role -> label -> placeholder / text -> test id -> CSS -> XPath
Pages: the-internet login, demoqa text-box, the-internet hovers,
       demoqa webtables, demo.playwright.dev/todomvc
"""
import re

import pytest
from playwright.sync_api import Page, expect

THE_INTERNET = "https://the-internet.herokuapp.com"
DEMOQA = "https://demoqa.com"
TODO = "https://demo.playwright.dev/todomvc/"


@pytest.mark.smoke
def test_get_by_role_and_label(page: Page):
    page.goto(f"{THE_INTERNET}/login")

    # role = what the element IS (heading, textbox, button, link...)
    expect(page.get_by_role("heading", name="Login Page")).to_be_visible()

    # label = the text of <label for="username">Username</label>
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()

    expect(page.locator("#flash")).to_contain_text("You logged into a secure area!")


def test_get_by_role_link(page: Page):
    page.goto(THE_INTERNET)
    page.get_by_role("link", name="Form Authentication").click()
    expect(page).to_have_url(re.compile(r".*/login$"))


def test_get_by_placeholder(page: Page):
    page.goto(f"{DEMOQA}/text-box")

    # On demoqa the <label> is NOT linked to the input (no for="..."),
    # so get_by_label() finds nothing here...
    expect(page.get_by_label("Full Name")).to_have_count(0)

    # ...but the inputs have placeholders.
    page.get_by_placeholder("Full Name").fill("Anna Test")
    page.get_by_placeholder("name@example.com").fill("anna@test.ge")
    page.get_by_role("button", name="Submit").click()

    expect(page.locator("#output #name")).to_have_text("Name:Anna Test")


def test_get_by_text(page: Page):
    page.goto(f"{THE_INTERNET}/login")
    # Default: part of the text, case-insensitive.
    expect(page.get_by_text("log into the secure area")).to_be_visible()
    # exact=True: the whole text, case-sensitive.
    expect(page.get_by_text("Login Page", exact=True)).to_be_visible()


def test_get_by_alt_text_and_title(page: Page):
    page.goto(f"{THE_INTERNET}/hovers")
    # <img alt="User Avatar">  - three pictures
    expect(page.get_by_alt_text("User Avatar")).to_have_count(3)

    page.goto(f"{DEMOQA}/webtables")
    # <span title="Delete">  - one per row, 3 rows
    expect(page.get_by_title("Delete")).to_have_count(3)


def test_get_by_test_id(page: Page):
    page.goto(TODO)
    page.get_by_placeholder("What needs to be done?").fill("Buy milk")
    page.get_by_placeholder("What needs to be done?").press("Enter")

    # data-testid="todo-title" - an attribute developers add for tests
    expect(page.get_by_test_id("todo-title")).to_have_text("Buy milk")
    expect(page.get_by_test_id("todo-count")).to_have_text("1 item left")
