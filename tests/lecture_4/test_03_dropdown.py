"""03 · Dropdown. select_option() picks by value or by label."""
from playwright.sync_api import Page, expect


def test_dropdown(page: Page):
    page.goto("https://the-internet.herokuapp.com/dropdown")
    dropdown = page.locator("#dropdown")  # 1
    dropdown.select_option("2")  # 2  by value
    expect(dropdown).to_have_value("2")
    dropdown.select_option(label="Option 1")  # 3  by text
    expect(dropdown).to_have_value("1")  # 4
    expect(page.locator("option:checked")).to_have_text("Option 1")


def test_dropdown_on_demoqa(page: Page):
    page.goto("https://demoqa.com/select-menu")
    old_menu = page.locator("#oldSelectMenu")
    old_menu.select_option("Green")  # a string matches the value OR the label
    expect(old_menu).to_have_value("2")  # <option value="2">Green</option>
