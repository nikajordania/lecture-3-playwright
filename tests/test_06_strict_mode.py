"""01 · Find — strict mode.

Slide: "One locator, three buttons".
Page:  https://demoqa.com/buttons
       "Double Click Me", "Right Click Me", "Click Me"
       get_by_role(name="Click Me") is a PART match -> all three buttons.

An action (click, fill...) needs exactly ONE element.
If the locator finds more, Playwright stops with "strict mode violation".
"""
import re

import pytest
from playwright.sync_api import Error, Page, expect

BUTTONS = "https://demoqa.com/buttons"
DROPPABLE = "https://demoqa.com/droppable"


def test_three_buttons_match(page: Page):
    page.goto(BUTTONS)
    expect(page.get_by_role("button", name="Click Me")).to_have_count(3)


def test_click_raises_strict_mode_violation(page: Page):
    page.goto(BUTTONS)
    with pytest.raises(Error, match="strict mode violation"):
        page.get_by_role("button", name="Click Me").click(timeout=3_000)


def test_fix_1_exact(page: Page):
    page.goto(BUTTONS)
    page.get_by_role("button", name="Click Me", exact=True).click()
    expect(page.locator("#dynamicClickMessage")).to_have_text("You have done a dynamic click")


def test_fix_2_nth_and_last(page: Page):
    page.goto(BUTTONS)
    buttons = page.get_by_role("button", name="Click Me")
    # nth() counts from 0: 0 = Double, 1 = Right, 2 = Click Me
    expect(buttons.nth(2)).to_have_text("Click Me")
    expect(buttons.last).to_have_text("Click Me")


def test_first_picks_the_wrong_button(page: Page):
    page.goto(BUTTONS)
    # .first hides the problem: no error, but it is a different button.
    expect(page.get_by_role("button", name="Click Me").first).to_have_text("Double Click Me")


def test_fix_3_filter_with_regex(page: Page):
    page.goto(BUTTONS)
    only_click_me = page.get_by_role("button").filter(has_text=re.compile(r"^Click Me$"))
    expect(only_click_me).to_have_count(1)


def test_duplicate_id_on_one_page(page: Page):
    page.goto(DROPPABLE)
    # An id should be unique, but this page has TWO elements with id="droppable"
    # (one is on another tab of the page).
    expect(page.locator("#droppable")).to_have_count(2)

    # Fix: search inside a unique parent first.
    simple = page.locator("#simpleDropContainer").locator("#droppable")
    expect(simple).to_have_count(1)
    expect(simple).to_have_text("Drop Here")
