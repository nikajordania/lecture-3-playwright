"""10 · New window. expect_popup() catches the new window."""
import pytest
from playwright.sync_api import Page, expect


def test_new_window(page: Page):
    page.goto("https://demoqa.com/browser-windows")
    button = page.get_by_role("button", name="New Window", exact=True)
    with page.expect_popup() as popup_info:  # 1
        button.click()  # 2
    popup = popup_info.value  # 3
    heading = popup.locator("#sampleHeading")  # 4
    expect(heading).to_have_text("This is a sample page")
    popup.close()  # 5
    expect(page.locator("h1")).to_have_text("Browser Windows")


@pytest.mark.parametrize("button_name", ["New Tab", "New Window"])
def test_tab_or_window_is_the_same_for_playwright(page: Page, button_name):
    page.goto("https://demoqa.com/browser-windows")
    with page.expect_popup() as popup_info:
        page.get_by_role("button", name=button_name, exact=True).click()
    expect(popup_info.value.locator("#sampleHeading")).to_have_text("This is a sample page")
