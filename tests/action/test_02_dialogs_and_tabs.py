"""Action — dialogs (alert, confirm, prompt) and new tabs.

Slide: "Say how to answer before the dialog opens".
    1 page.once("dialog", ...)   <- register the answer FIRST
    2 click()                    <- this opens the dialog
    3 the handler answers it

No handler?  Playwright closes every dialog with "Cancel" (dismiss).
"""
from playwright.sync_api import Dialog, Page, expect

ALERTS = "https://the-internet.herokuapp.com/javascript_alerts"
DEMOQA_ALERTS = "https://demoqa.com/alerts"
WINDOWS = "https://the-internet.herokuapp.com/windows"


def test_alert_ok(page: Page):
    page.goto(ALERTS)
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Click for JS Alert").click()
    expect(page.locator("#result")).to_have_text("You successfully clicked an alert")


def test_confirm_accept(page: Page):
    page.goto(ALERTS)
    messages = []

    def answer_ok(dialog: Dialog):
        messages.append(dialog.message)  # remember what the dialog said
        dialog.accept()

    page.once("dialog", answer_ok)
    page.get_by_role("button", name="Click for JS Confirm").click()

    expect(page.locator("#result")).to_have_text("You clicked: Ok")
    assert messages == ["I am a JS Confirm"]


def test_confirm_without_handler_is_dismissed(page: Page):
    page.goto(ALERTS)
    # No page.once(...) here: Playwright presses "Cancel" for us.
    page.get_by_role("button", name="Click for JS Confirm").click()
    expect(page.locator("#result")).to_have_text("You clicked: Cancel")


def test_prompt_with_text(page: Page):
    page.goto(ALERTS)
    page.once("dialog", lambda dialog: dialog.accept("Nika"))  # text for the prompt
    page.get_by_role("button", name="Click for JS Prompt").click()
    expect(page.locator("#result")).to_have_text("You entered: Nika")


def test_demoqa_confirm_box(page: Page):
    page.goto(DEMOQA_ALERTS)
    page.once("dialog", lambda dialog: dialog.accept())
    page.locator("#confirmButton").click()
    expect(page.locator("#confirmResult")).to_have_text("You selected Ok")


def test_new_tab(page: Page):
    page.goto(WINDOWS)

    # "Wait for a new page WHILE I click the link"
    with page.context.expect_page() as new_tab_info:
        page.get_by_role("link", name="Click Here").click()
    new_tab = new_tab_info.value

    expect(new_tab.get_by_role("heading")).to_have_text("New Window")
    expect(new_tab).to_have_url(WINDOWS + "/new")
    new_tab.close()
