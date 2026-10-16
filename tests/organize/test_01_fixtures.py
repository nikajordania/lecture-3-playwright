"""05 · Organize — fixtures.

Slide: "Fixtures prepare the stage for every test".

    browser   one for the whole run           (from pytest-playwright)
    context   NEW for every test - like a new incognito window
    page      NEW for every test - one tab inside that context
    logged_in OUR fixture in conftest.py: setup -> yield -> teardown

A test gets a fixture by writing its name as an argument.
"""
import re

from playwright.sync_api import BrowserContext, Page, expect

THE_INTERNET = "https://the-internet.herokuapp.com"


def test_starts_already_logged_in(logged_in: Page):
    # No login steps here: the fixture did them before the test started.
    expect(logged_in.get_by_role("heading", name="Secure Area")).to_be_visible()
    expect(logged_in.locator("#flash")).to_contain_text("You logged into a secure area!")


def test_logout(logged_in: Page):
    logged_in.get_by_role("link", name="Logout").click()

    expect(logged_in).to_have_url(re.compile(r".*/login"))
    expect(logged_in.locator("#flash")).to_contain_text("You logged out of the secure area!")
    # The fixture's teardown sees we are not on /secure and skips the logout.


def test_every_test_gets_a_fresh_context(page: Page, context: BrowserContext):
    # The test before this one was logged in - but its cookies are gone:
    # this test has its own new context.
    assert context.cookies() == []

    page.goto(f"{THE_INTERNET}/secure")

    # Not logged in -> the site sends us back to the login page.
    expect(page).to_have_url(re.compile(r".*/login"))
    expect(page.locator("#flash")).to_contain_text("You must login to view the secure area!")
