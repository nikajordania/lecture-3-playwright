"""Fixtures only for tests/lecture_6.

Slide "One fixture sets the size for every test" (part 02).
A fixture with the SAME NAME as a pytest-playwright fixture replaces it,
but only for the tests in this folder. The argument with the same name
gives us the original values, so we keep them and change one key.
"""
import pytest

SAUCE = "https://www.saucedemo.com"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        # every page in this folder speaks English, whatever the computer says
        "locale": "en-US",
        # more keys you can put here (see the slides):
        # "viewport": {"width": 1920, "height": 1080},
        # "timezone_id": "Asia/Tbilisi",
        # "storage_state": "state.json",
    }


# The same trick works for HOW the browser starts (part 03):
#
# @pytest.fixture(scope="session")
# def browser_type_launch_args(browser_type_launch_args):
#     return {**browser_type_launch_args, "slow_mo": 500}
#
# It is commented out on purpose: the browser is shared by the whole run,
# so put it in the ROOT conftest.py if you want it, not in a sub-folder.


@pytest.fixture
def logged_in_page(page, context):
    """A SauceDemo page that is already logged in — through a cookie."""
    context.add_cookies([
        {"name": "session-username", "value": "standard_user", "url": SAUCE},
    ])
    page.goto(SAUCE + "/inventory.html")
    return page
