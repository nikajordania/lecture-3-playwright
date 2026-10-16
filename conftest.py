"""Shared fixtures for every test in this project.

pytest finds conftest.py by itself: test files use these fixtures
by writing their name as a test argument. No import is needed.

Slide: "Fixtures prepare the stage for every test".
"""
import re
import uuid

import pytest
from playwright.sync_api import Page, expect

THE_INTERNET = "https://the-internet.herokuapp.com"
DEMOQA = "https://demoqa.com"

# demoqa.com loads many ads. They make the page slow and can cover buttons.
AD_SERVERS = re.compile(
    r"googlesyndication|doubleclick|googletagservices|adservice|"
    r"amazon-adsystem|adnxs|criteo|pubmatic|taboola"
)


@pytest.fixture(autouse=True)
def block_ads(page: Page):
    """autouse=True: runs for EVERY test, the test does not ask for it.

    page.route() catches each network request. Requests to ad servers
    are aborted, everything else goes to the network as usual.
    """
    page.route(AD_SERVERS, lambda route: route.abort())
    yield


@pytest.fixture
def new_user(page: Page):
    """Adds a NEW row to demoqa.com/webtables and gives the test that row.

    Every test that uses this fixture gets its own user with its own
    e-mail, so the tests do not depend on each other.
    Slide 05 · "Every test brings its own data".
    """
    email = f"nika.{uuid.uuid4().hex[:6]}@test.ge"  # unique for every test

    page.goto(f"{DEMOQA}/webtables")
    page.get_by_role("button", name="Add", exact=True).click()
    page.get_by_placeholder("First Name").fill("Nika")
    page.get_by_placeholder("Last Name").fill("Tester")
    page.get_by_placeholder("name@example.com").fill(email)
    page.get_by_placeholder("Age").fill("30")
    page.get_by_placeholder("Salary").fill("5000")
    page.get_by_placeholder("Department").fill("QA")
    page.get_by_role("button", name="Submit").click()

    row = page.get_by_role("row").filter(has_text=email)
    expect(row).to_have_count(1)
    yield row
    # No teardown: demoqa keeps the table only in the browser tab,
    # and pytest-playwright closes the tab (context) after every test.
