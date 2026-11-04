"""Lecture 6 · 12 — codegen: from a recorded draft to a real test.

Slides "codegen" ... "codegen writes the steps, you write the test".

Record it yourself (PowerShell):
    uv run playwright codegen --target python-pytest https://www.saucedemo.com
    uv run playwright codegen --target python-pytest --test-id-attribute data-test `
        -o tests/lecture_6/test_draft.py https://www.saucedemo.com
More commands: README.md, part "codegen".
"""
import pytest
from playwright.sync_api import Page, Playwright, expect


# ---------- 1 · the draft, as codegen writes it ----------
# Kept as an example. It works, but: a click() before every fill(),
# the login inside the test, the name test_example.

def test_example(page: Page) -> None:
    page.goto("https://www.saucedemo.com/")
    page.locator("[data-test=\"username\"]").click()
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"password\"]").click()
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.locator("[data-test=\"login-button\"]").click()
    page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    expect(page.locator("[data-test=\"shopping-cart-badge\"]")).to_contain_text("1")


# ---------- 2 · the same idea, after cleanup ----------

@pytest.fixture
def data_test_ids(playwright: Playwright):
    """SauceDemo uses data-test, Playwright's default is data-testid.

    Same as codegen --test-id-attribute data-test. Put back afterwards,
    so other tests are not affected.
    """
    playwright.selectors.set_test_id_attribute("data-test")
    yield
    playwright.selectors.set_test_id_attribute("data-testid")


def test_backpack_in_cart(data_test_ids, logged_in_page: Page):
    page = logged_in_page                       # login → fixture (conftest.py)
    page.get_by_test_id("add-to-cart-sauce-labs-backpack").click()
    badge = page.get_by_test_id("shopping-cart-badge")
    expect(badge).to_have_text("1")             # a real check
    expect(page.get_by_test_id("remove-sauce-labs-backpack")).to_be_visible()
