"""The same idea for a form: demoqa.com/text-box"""
from playwright.sync_api import Page


class TextBoxPage:
    URL = "https://demoqa.com/text-box"

    def __init__(self, page: Page):
        self.page = page
        self.full_name = page.get_by_placeholder("Full Name")
        self.email = page.get_by_placeholder("name@example.com")
        self.current_address = page.get_by_placeholder("Current Address")
        self.submit = page.get_by_role("button", name="Submit")
        self.output = page.locator("#output")

    def open(self):
        self.page.goto(self.URL)
        return self

    def fill_form(self, name: str, email: str, address: str) -> None:
        self.full_name.fill(name)
        self.email.fill(email)
        self.current_address.fill(address)
        self.submit.click()
