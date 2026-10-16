"""05 · Organize — every test brings its own data.

Slide: "Every test brings its own data".

BAD (chained tests):
    test_create_user  ->  test_edit_user  ->  test_delete_user
    edit and delete need the user that create made.
    1 real bug in create = 3 red tests, and running one test alone breaks.

GOOD (this file):
    each test asks for the `new_user` fixture (see conftest.py).
    The fixture adds a NEW user with a unique e-mail for this test only.
    Any order, any subset:  uv run pytest -k delete   still works.
Page: https://demoqa.com/webtables
"""
from playwright.sync_api import Locator, Page, expect


def test_create_user(new_user: Locator):
    expect(new_user).to_contain_text("Nika")
    expect(new_user).to_contain_text("QA")


def test_edit_user_salary(page: Page, new_user: Locator):
    new_user.get_by_title("Edit").click()

    salary = page.get_by_placeholder("Salary")
    salary.fill("9000")
    page.get_by_role("button", name="Submit").click()

    expect(new_user).to_contain_text("9000")


def test_delete_user(new_user: Locator):
    new_user.get_by_title("Delete").click()
    expect(new_user).to_have_count(0)


def test_search_finds_only_this_user(page: Page, new_user: Locator):
    email = new_user.get_by_role("cell").nth(3).inner_text()  # 4th column = Email

    page.get_by_placeholder("Type to search").fill(email)

    expect(page.locator("tbody tr")).to_have_count(1)
    expect(page.locator("tbody tr")).to_contain_text(email)
