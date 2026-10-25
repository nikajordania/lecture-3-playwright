"""Slide "A page becomes a class": element -> locator attribute, user action -> method."""
from playwright.sync_api import Page

from .base_page import BASE, BasePage
from .secure_page import SecurePage


class LoginPage(BasePage):
    URL = BASE + "/login"

    def __init__(self, page: Page):
        super().__init__(page)  # runs BasePage.__init__: stores self.page
        self.username = page.get_by_label("Username")
        self.password = page.get_by_label("Password")
        self.submit = page.get_by_role("button", name="Login")
        self.flash = page.locator("#flash")

    def _fill_and_submit(self, user: str, password: str) -> None:
        self.username.fill(user)
        self.password.fill(password)
        self.submit.click()

    def login(self, user: str, password: str) -> SecurePage:
        """Correct data: the user lands on /secure -> we return that page."""
        self._fill_and_submit(user, password)
        return SecurePage(self.page)

    def login_expecting_error(self, user: str, password: str) -> "LoginPage":
        """Wrong data: the user stays here -> we return this same page."""
        self._fill_and_submit(user, password)
        return self
