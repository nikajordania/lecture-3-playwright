"""Check — expect(): what the user should see.

Slide: "expect(locator) - what the user should see".
Every expect() checks again and again until it passes or 5 s run out.

    to_be_visible / to_be_hidden      to_have_text / to_contain_text
    to_have_value                     to_be_checked
    to_have_count                     to_have_url / to_have_title
    to_be_enabled / to_be_disabled    to_have_attribute / to_contain_class
"""
import re

import pytest
from playwright.sync_api import Page, expect

THE_INTERNET = "https://the-internet.herokuapp.com"


def test_visible_and_contain_text(page: Page):
    page.goto(f"{THE_INTERNET}/login")
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("wrong")
    page.get_by_role("button", name="Login").click()

    flash = page.locator("#flash")
    expect(flash).to_be_visible()
    # to_contain_text: the flash also has a "×" close button inside,
    # so to_have_text("Your password is invalid!") would fail.
    expect(flash).to_contain_text("Your password is invalid!")
    expect(flash).to_contain_class("error")


def test_have_text_value_and_attribute(page: Page):
    page.goto(f"{THE_INTERNET}/login")
    expect(page.get_by_role("heading", level=2)).to_have_text("Login Page")

    password = page.get_by_label("Password")
    password.fill("secret")
    expect(password).to_have_value("secret")
    expect(password).to_have_attribute("type", "password")  # dots, not letters


def test_checked_and_not_checked(page: Page):
    page.goto(f"{THE_INTERNET}/checkboxes")
    boxes = page.locator("#checkboxes input")
    expect(boxes.nth(0)).not_to_be_checked()  # "not_" = the opposite check
    expect(boxes.nth(1)).to_be_checked()


def test_count(page: Page):
    page.goto(f"{THE_INTERNET}/tables")
    expect(page.locator("#table1 tbody tr")).to_have_count(4)


def test_url_and_title(page: Page):
    page.goto(f"{THE_INTERNET}/login")
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(re.compile(r".*/secure"))  # expect(page), not a locator
    expect(page).to_have_title("The Internet")


def test_hidden_disabled_and_enabled(page: Page):
    page.goto(f"{THE_INTERNET}/dynamic_loading/1")
    expect(page.locator("#finish")).to_be_hidden()  # in the HTML, but not shown

    page.goto(f"{THE_INTERNET}/dynamic_controls")
    expect(page.locator("#input-example input")).to_be_disabled()
    expect(page.get_by_role("button", name="Enable")).to_be_enabled()


def test_custom_message_in_the_report(page: Page):
    page.goto(f"{THE_INTERNET}/login")
    # The text is printed in the error if the check fails.
    expect(page.get_by_role("button", name="Login"), "Login button must be on the page").to_be_visible()
