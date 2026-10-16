"""Action — every user gesture has its own method.

Slide: "Every user gesture has its own method".
    click · dblclick · fill · check · select_option · hover · drag_to · set_input_files

Each action WAITS until the element is ready (visible, stable, enabled),
see tests/waits/test_01_waits.py.
"""
from pathlib import Path

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


def test_hover(page: Page):
    page.goto(f"{THE_INTERNET}/hovers")
    page.locator(".figure").first.hover()
    expect(page.get_by_text("name: user1")).to_be_visible()


def test_drag_to(page: Page):
    page.goto(f"{DEMOQA}/droppable")
    target = page.locator("#simpleDropContainer #droppable")

    page.locator("#draggable").drag_to(target)

    expect(target).to_have_text("Dropped!")


def test_upload_a_file(page: Page, tmp_path: Path):
    # tmp_path is a pytest fixture: a new empty folder for this test.
    cv = tmp_path / "cv.txt"
    cv.write_text("Nika - Test Automation Engineer")

    page.goto(f"{THE_INTERNET}/upload")
    page.locator("#file-upload").set_input_files(cv)
    page.locator("#file-submit").click()

    expect(page.get_by_role("heading", name="File Uploaded!")).to_be_visible()
    expect(page.locator("#uploaded-files")).to_have_text("cv.txt")
