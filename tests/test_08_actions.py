"""02 · Act — every user gesture has its own method.

Slide: "Every user gesture has its own method".
    click · dblclick · fill · press · check · select_option · hover · drag_to · set_input_files

Each action WAITS until the element is ready (visible, stable, enabled),
see tests/test_11_auto_waiting.py.
"""
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

THE_INTERNET = "https://the-internet.herokuapp.com"
DEMOQA = "https://demoqa.com"


def test_click_double_click_right_click(page: Page):
    page.goto(f"{DEMOQA}/buttons")

    page.get_by_role("button", name="Double Click Me").dblclick()
    expect(page.locator("#doubleClickMessage")).to_have_text("You have done a double click")

    page.get_by_role("button", name="Right Click Me").click(button="right")
    expect(page.locator("#rightClickMessage")).to_have_text("You have done a right click")


def test_fill_and_clear(page: Page):
    page.goto(f"{THE_INTERNET}/login")
    username = page.get_by_label("Username")

    username.fill("tomsmith")  # fill() replaces the whole value
    expect(username).to_have_value("tomsmith")

    username.clear()
    expect(username).to_have_value("")


@pytest.mark.parametrize("key, shown", [("Escape", "ESCAPE"), ("Tab", "TAB"), ("a", "A")])
def test_press_a_key(page: Page, key, shown):
    page.goto(f"{THE_INTERNET}/key_presses")
    # Not "Enter" here: Enter in this one-field form submits it and reloads the page.
    page.locator("#target").press(key)
    expect(page.locator("#result")).to_have_text(f"You entered: {shown}")


def test_press_sequentially_types_like_a_person(page: Page):
    page.goto(f"{THE_INTERNET}/key_presses")
    # One key at a time: the page shows the LAST key.
    page.locator("#target").press_sequentially("qa", delay=100)
    expect(page.locator("#result")).to_have_text("You entered: A")


def test_check_and_uncheck(page: Page):
    page.goto(f"{THE_INTERNET}/checkboxes")
    boxes = page.locator("#checkboxes input[type='checkbox']")

    boxes.nth(0).check()  # was empty -> ticked
    boxes.nth(1).uncheck()  # was ticked -> empty

    expect(boxes.nth(0)).to_be_checked()
    expect(boxes.nth(1)).not_to_be_checked()


def test_select_option(page: Page):
    page.goto(f"{THE_INTERNET}/dropdown")
    dropdown = page.locator("#dropdown")

    dropdown.select_option("2")  # by value: <option value="2">
    expect(dropdown).to_have_value("2")

    dropdown.select_option(label="Option 1")  # by the visible text
    expect(dropdown).to_have_value("1")


def test_select_option_on_demoqa(page: Page):
    page.goto(f"{DEMOQA}/select-menu")
    old_menu = page.locator("#oldSelectMenu")
    old_menu.select_option("Green")  # a string matches the value OR the text
    expect(old_menu).to_have_value("2")  # <option value="2">Green</option>


def test_hover(page: Page):
    page.goto(f"{THE_INTERNET}/hovers")
    page.locator(".figure").first.hover()
    expect(page.get_by_text("name: user1")).to_be_visible()


def test_drag_to(page: Page):
    page.goto(f"{DEMOQA}/droppable")
    target = page.locator("#simpleDropContainer #droppable")

    page.locator("#draggable").drag_to(target)

    expect(target).to_have_text("Dropped!")


def test_drag_to_html5_columns(page: Page):
    page.goto(f"{THE_INTERNET}/drag_and_drop")
    page.locator("#column-a").drag_to(page.locator("#column-b"))
    # The two boxes changed places: the left box now says B.
    expect(page.locator("#column-a header")).to_have_text("B")


def test_upload_a_file(page: Page, tmp_path: Path):
    # tmp_path is a pytest fixture: a new empty folder for this test.
    cv = tmp_path / "cv.txt"
    cv.write_text("Nika - Test Automation Engineer")

    page.goto(f"{THE_INTERNET}/upload")
    page.locator("#file-upload").set_input_files(cv)
    page.locator("#file-submit").click()

    expect(page.get_by_role("heading", name="File Uploaded!")).to_be_visible()
    expect(page.locator("#uploaded-files")).to_have_text("cv.txt")
