"""02 · Checkboxes. check() sets a state, click() only toggles."""
from playwright.sync_api import Page, expect


def test_checkboxes(page: Page):
    page.goto("https://the-internet.herokuapp.com/checkboxes")
    boxes = page.locator("#checkboxes input")  # 1
    boxes.nth(0).check()  # 2
    boxes.nth(1).uncheck()  # 3
    expect(boxes.nth(0)).to_be_checked()  # 4
    expect(boxes.nth(1)).not_to_be_checked()
    # state from data: True = tick, False = untick
    boxes.nth(1).set_checked(True)
    expect(boxes.nth(1)).to_be_checked()


def test_click_only_toggles(page: Page):
    page.goto("https://the-internet.herokuapp.com/checkboxes")
    second = page.locator("#checkboxes input").nth(1)  # starts ticked
    second.click()
    second.click()
    expect(second).to_be_checked()  # two clicks: back where it started
