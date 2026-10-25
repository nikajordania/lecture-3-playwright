"""Part 4 · Classes and Page Objects.

Classes: pages/base_page.py, pages/login_page.py, pages/secure_page.py
Fixtures: conftest.py (login_page, secure_page)
"""
from playwright.sync_api import Page, expect

from .pages.login_page import LoginPage
from .pages.secure_page import SecurePage


def test_login_before_pom(page: Page):
    # BEFORE: 5 lines about HOW (selectors, clicks)
    page.goto("https://the-internet.herokuapp.com/login")
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#flash")).to_contain_text("secure area")


def test_login_after_pom(page: Page):
    # AFTER: 3 lines about WHAT (open, log in, check)
    login_page = LoginPage(page).open()
    secure_page = login_page.login("tomsmith", "SuperSecretPassword!")
    expect(secure_page.flash).to_contain_text("secure area")


def test_valid_login(login_page: LoginPage):
    # The fixture already opened the login page.
    secure = login_page.login("tomsmith", "SuperSecretPassword!")
    expect(secure.flash).to_contain_text("secure area")


def test_wrong_password(login_page: LoginPage):
    same_page = login_page.login_expecting_error("tomsmith", "wrong")
    expect(same_page.flash).to_contain_text("Your password is invalid!")


def test_pages_lead_to_pages(login_page: LoginPage):
    secure = login_page.login("tomsmith", "SuperSecretPassword!")  # -> SecurePage
    expect(secure.flash).to_contain_text("secure area")
    back = secure.logout()  # -> LoginPage
    expect(back.flash).to_contain_text("logged out")


def test_secure_page_fixture(secure_page: SecurePage):
    expect(secure_page.heading).to_be_visible()


def test_inherited_methods(login_page: LoginPage):
    # open() and title() come from BasePage
    assert login_page.title() == "The Internet"
    assert login_page.URL.endswith("/login")
