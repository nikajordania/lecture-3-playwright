"""Fixtures - the simplest before / after.

    code before yield  ->  runs BEFORE the test   (setup)
    yield              ->  the test runs here
    code after yield   ->  runs AFTER the test    (teardown, even if the test failed)

A test gets a fixture by writing its name as an argument.
Run with -s to see the prints:  uv run pytest tests/data/test_02_fixtures.py -s
"""
import pytest
from playwright.sync_api import Page, expect


@pytest.fixture
def login_page(page: Page):
    print("\nbefore: open the login page")
    page.goto("https://the-internet.herokuapp.com/login")

    yield page

    print("\nafter: close the page")
    page.close()


def test_login_page_title(login_page: Page):
    expect(login_page.get_by_role("heading", name="Login Page")).to_be_visible()
