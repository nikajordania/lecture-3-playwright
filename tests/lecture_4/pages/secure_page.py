"""The page after a successful login: the-internet.herokuapp.com/secure"""
from playwright.sync_api import Page

from .base_page import BASE, BasePage


class SecurePage(BasePage):
    URL = BASE + "/secure"

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="Secure Area")
        self.flash = page.locator("#flash")
        self.logout_link = page.get_by_role("link", name="Logout")

    def logout(self):
        # Imported here, not at the top: login_page.py already imports this file.
        from .login_page import LoginPage

        self.logout_link.click()
        return LoginPage(self.page)  # after logout the user is on the login page
