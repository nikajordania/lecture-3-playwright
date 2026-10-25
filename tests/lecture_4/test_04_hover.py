"""04 · Hover. hover() moves the mouse, nothing more."""
from playwright.sync_api import Page, expect


def test_hover(page: Page):
    page.goto("https://the-internet.herokuapp.com/hovers")
    card = page.locator(".figure").nth(1)  # 1
    caption = card.locator(".figcaption")
    expect(caption).to_be_hidden()
    card.hover()  # 2
    expect(caption).to_be_visible()  # 3
    expect(caption).to_contain_text("name: user2")
    link = caption.get_by_role("link", name="View profile")  # 4
    expect(link).to_have_attribute("href", "/users/2")
