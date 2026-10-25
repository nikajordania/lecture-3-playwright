"""08 · Back, forward, refresh. Three buttons, three page methods."""
import re

from playwright.sync_api import Page, expect


def test_back_forward_reload(page: Page):
    page.goto("https://the-internet.herokuapp.com/")  # 1
    page.get_by_role("link", name="Checkboxes").click()  # 2
    expect(page).to_have_url(re.compile(r"/checkboxes$"))
    page.go_back()  # 3
    expect(page).to_have_url("https://the-internet.herokuapp.com/")
    page.go_forward()  # 4
    expect(page).to_have_url(re.compile(r"/checkboxes$"))
    page.reload()  # 5
    expect(page.locator("h3")).to_have_text("Checkboxes")
