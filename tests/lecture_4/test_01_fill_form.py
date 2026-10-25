"""01 · Fill a form. Slides "Fill a form the way a user does" + "Six user steps, six lines of code"."""
from playwright.sync_api import Page, expect

from .pages.text_box_page import TextBoxPage


def test_fill_form(page: Page):
    page.goto("https://demoqa.com/text-box")  # 1
    page.get_by_placeholder("Full Name").fill("Anna Test")  # 2
    page.get_by_placeholder("name@example.com").fill("anna@test.ge")  # 3
    page.get_by_placeholder("Current Address").fill("Tbilisi")  # 4
    page.get_by_role("button", name="Submit").click()  # 5
    output = page.locator("#output")  # 6
    expect(output.locator("#name")).to_have_text("Name:Anna Test")
    expect(output).to_contain_text("anna@test.ge")


def test_fill_form_with_a_page_class(page: Page):
    # The same test with a page class (part 4 of the lecture).
    text_box = TextBoxPage(page).open()
    text_box.fill_form("Anna Test", "anna@test.ge", "Tbilisi")
    expect(text_box.output.locator("#name")).to_have_text("Name:Anna Test")
