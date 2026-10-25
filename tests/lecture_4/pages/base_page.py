"""BasePage: what EVERY page has. Slide "Shared code lives in one base class"."""
from playwright.sync_api import Page

BASE = "https://the-internet.herokuapp.com"


class BasePage:
    URL = BASE  # each child class sets its own URL

    def __init__(self, page: Page):
        self.page = page  # the object keeps its browser tab

    def open(self):
        self.page.goto(self.URL)
        return self  # so we can write LoginPage(page).open().login(...)

    def title(self) -> str:
        return self.page.title()
