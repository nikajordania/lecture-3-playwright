"""Data — one test function, many test cases.

Slides: "Test design tells you which values to try",
        "Don't copy the test. Separate the data.",
        "One function, a table of data, three tests".

    uv run pytest tests/data/test_01_parametrize.py -v
    uv run pytest -k "bad user" -v          <- one case by its id
"""
import pytest
from playwright.sync_api import Page, expect

LOGIN = "https://the-internet.herokuapp.com/login"
PRACTICE_FORM = "https://demoqa.com/automation-practice-form"
TEXT_BOX = "https://demoqa.com/text-box"


# --- 1. Login: 3 rows of data, readable ids ---------------------------------
@pytest.mark.parametrize(
    "user, password, msg",
    [
        ("tomsmith", "SuperSecretPassword!", "You logged into a secure area!"),
        ("wrong", "SuperSecretPassword!", "Your username is invalid!"),
        ("tomsmith", "wrong", "Your password is invalid!"),
    ],
    ids=["valid", "bad user", "bad password"],
)
def test_login(page: Page, user, password, msg):
    page.goto(LOGIN)
    page.get_by_label("Username").fill(user)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#flash")).to_contain_text(msg)


# --- 2. Boundary values: "Mobile" must have exactly 10 digits ----------------
#   HTML: <input id="userNumber" minlength="10" maxlength="10" pattern="\d*">
#
#        9 digits  |  10 digits  |  11 digits
#        too short |    valid    |  the 11th is not typed (maxlength)
@pytest.mark.parametrize(
    "typed, value_in_field, is_valid",
    [
        ("123456789", "123456789", False),
        ("1234567890", "1234567890", True),
        ("12345678901", "1234567890", True),
        ("12345abcde", "12345abcde", False),
    ],
    ids=["9 digits", "10 digits", "11 digits", "letters"],
)
def test_mobile_number_boundaries(page: Page, typed, value_in_field, is_valid):
    page.goto(PRACTICE_FORM)
    mobile = page.get_by_placeholder("Mobile Number")

    mobile.fill(typed)

    expect(mobile).to_have_value(value_in_field)
    # Ask the browser itself: does this value pass the HTML rules?
    assert mobile.evaluate("element => element.validity.valid") == is_valid


# --- 3. Equivalence classes: invalid e-mail -----------------------
@pytest.mark.parametrize("email", ["anna.test.ge", "anna@", "@test.ge"], ids=["no @", "no domain", "no name"])
def test_invalid_email_is_marked_red(page: Page, email):
    page.goto(TEXT_BOX)
    page.get_by_placeholder("name@example.com").fill(email)
    page.get_by_role("button", name="Submit").click()
    expect(page.get_by_placeholder("name@example.com")).to_contain_class("field-error")
