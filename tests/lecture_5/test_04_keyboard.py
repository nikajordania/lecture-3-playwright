"""Lecture 5 · 04 — Keyboard: Tab, shortcuts, arrow keys.

Slides "04 · Keyboard · picture / code".
locator.press() first focuses the element, then presses the key.
Keys join with "+": "ControlOrMeta+A" is Ctrl+A on Windows/Linux
and Cmd+A on Mac.
"""
from playwright.sync_api import Page, expect

BASE = "https://the-internet.herokuapp.com"


def test_tab_moves_focus(page: Page):
    page.goto(BASE + "/login")
    username = page.get_by_label("Username")
    username.fill("tomsmith")
    # 1 — press Tab
    username.press("Tab")
    # 2 — the cursor is now in the password field
    expect(page.get_by_label("Password")).to_be_focused()


def test_select_all_and_delete(page: Page):
    page.goto(BASE + "/login")
    username = page.get_by_label("Username")
    username.fill("tomsmith")
    # 3 — select all, then delete
    username.press("ControlOrMeta+A")
    username.press("Delete")
    expect(username).to_have_value("")


def test_enter_submits_the_form(page: Page):
    page.goto(BASE + "/login")
    page.get_by_label("Username").fill("tomsmith")
    password = page.get_by_label("Password")
    password.fill("SuperSecretPassword!")
    # no click on the button: Enter sends the form
    password.press("Enter")
    expect(page).to_have_url(BASE + "/secure")


def test_slider_keys(page: Page):
    page.goto(BASE + "/horizontal_slider")
    slider = page.locator("input[type='range']")
    value = page.locator("#range")
    # 4 — every ArrowRight moves one step (0.5): 0 -> 0.5 -> 1.0 -> 1.5
    for _ in range(3):
        slider.press("ArrowRight")
    expect(value).to_have_text("1.5")
    # End jumps to the maximum
    slider.press("End")
    expect(value).to_have_text("5")
