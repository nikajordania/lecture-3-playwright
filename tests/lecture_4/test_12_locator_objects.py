"""Part 2 · Locators as objects.

Slides: "A locator is a recipe, not an element", "Ask a locator, get a Python value",
        "Where to keep a locator", "Pass the locator, not the selector string".
"""
import pytest
from playwright.sync_api import Locator, Page, expect

THE_INTERNET = "https://the-internet.herokuapp.com"


# --- a recipe, not an element ---------------------------------------------------
def test_locator_is_a_recipe(page: Page):
    login = page.get_by_role("button", name="Login")  # nothing is searched yet
    page.goto(f"{THE_INTERNET}/login")
    expect(login).to_be_visible()  # search 1

    page.reload()  # the old button is gone, a new one is drawn
    expect(login).to_be_visible()  # search 2: the SAME locator finds the new button


# --- values you can take out ----------------------------------------------------
def test_text_count_attribute_and_lists(page: Page):
    page.goto(f"{THE_INTERNET}/tables")
    rows = page.locator("#table1 tbody tr")

    assert rows.count() == 4  # count(): answers at once
    jason_row = rows.filter(has_text="Jason")
    assert jason_row.locator("td").nth(1).inner_text() == "Jason"
    assert jason_row.get_by_role("link", name="edit").get_attribute("href") == "#edit"

    last_names = page.locator("#table1 tbody td:first-child")
    assert last_names.all_inner_texts() == ["Smith", "Bach", "Doe", "Conway"]

    for row in rows.all():  # all(): a list of locators, one per row
        expect(row).to_be_visible()


def test_input_value_checked_and_visible(page: Page):
    page.goto(f"{THE_INTERNET}/login")
    username = page.get_by_label("Username")
    username.fill("tomsmith")
    assert username.input_value() == "tomsmith"

    page.goto(f"{THE_INTERNET}/checkboxes")
    assert page.locator("#checkboxes input").nth(1).is_checked() is True

    page.goto(f"{THE_INTERNET}/hovers")
    # is_visible() does not wait: fine for "if", wrong for checks.
    assert page.locator(".figcaption").first.is_visible() is False


# --- where to keep it: level 4, a fixture ---------------------------------------
@pytest.fixture
def username(page: Page) -> Locator:
    return page.get_by_label("Username")


def test_locator_from_a_fixture(page: Page, username: Locator):
    page.goto(f"{THE_INTERNET}/login")
    username.fill("tomsmith")
    expect(username).to_have_value("tomsmith")


# --- pass the locator, not the string --------------------------------------------
def fill_and_check(field: Locator, text: str):
    field.fill(text)
    expect(field).to_have_value(text)


def test_login_fields(page: Page):
    page.goto(f"{THE_INTERNET}/login")
    fill_and_check(page.get_by_label("Username"), "tomsmith")
    fill_and_check(page.get_by_label("Password"), "secret")
