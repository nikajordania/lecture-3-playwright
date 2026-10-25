"""09 · New tab. Every tab is its own Page object."""
from playwright.sync_api import Page, expect


def test_new_tab(page: Page):
    page.goto("https://the-internet.herokuapp.com/windows")
    with page.context.expect_page() as new_tab_info:  # 1
        page.get_by_role("link", name="Click Here").click()  # 2
    new_tab = new_tab_info.value  # 3
    expect(new_tab.locator("h3")).to_have_text("New Window")
    assert len(page.context.pages) == 2
    page.bring_to_front()  # 4
    new_tab.close()  # 5
    expect(page.locator("h3")).to_have_text("Opening a new window")
