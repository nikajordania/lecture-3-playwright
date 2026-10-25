"""05 · Drag and drop. drag_to() does the whole gesture."""
from playwright.sync_api import Page, expect


def test_drag_and_drop(page: Page):
    page.goto("https://demoqa.com/droppable")
    source = page.locator("#draggable")  # 1
    target = page.locator("#simpleDropContainer #droppable")  # 2  (2 x #droppable on this page)
    expect(target).to_have_text("Drop Here")
    source.drag_to(target)  # 3
    expect(target).to_have_text("Dropped!")  # 4


def test_drag_step_by_step_with_the_mouse(page: Page):
    page.goto("https://demoqa.com/droppable")
    target = page.locator("#simpleDropContainer #droppable")
    page.locator("#draggable").hover()
    page.mouse.down()
    target.hover()
    page.mouse.up()
    expect(target).to_have_text("Dropped!")


def test_drag_html5_columns(page: Page):
    page.goto("https://the-internet.herokuapp.com/drag_and_drop")
    page.locator("#column-a").drag_to(page.locator("#column-b"))
    expect(page.locator("#column-a header")).to_have_text("B")  # the boxes swapped
