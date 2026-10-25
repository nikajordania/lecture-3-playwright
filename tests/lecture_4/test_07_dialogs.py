"""07 · Alerts. Give the answer BEFORE the click."""
from playwright.sync_api import Dialog, Page, expect

ALERTS = "https://the-internet.herokuapp.com/javascript_alerts"


def test_dialogs(page: Page):
    page.goto(ALERTS)
    result = page.locator("#result")

    page.once("dialog", lambda d: d.accept())  # 1  alert -> OK
    page.get_by_role("button", name="Click for JS Alert").click()
    expect(result).to_have_text("You successfully clicked an alert")

    page.once("dialog", lambda d: d.accept())  # 2  confirm -> OK
    page.get_by_role("button", name="Click for JS Confirm").click()
    expect(result).to_have_text("You clicked: Ok")

    page.once("dialog", lambda d: d.accept("Anna"))  # 3  prompt -> text + OK
    page.get_by_role("button", name="Click for JS Prompt").click()
    expect(result).to_have_text("You entered: Anna")

    page.get_by_role("button", name="Click for JS Confirm").click()  # 4  no handler
    expect(result).to_have_text("You clicked: Cancel")


def test_dialog_message_and_type(page: Page):
    page.goto(ALERTS)
    seen = []

    def remember_and_dismiss(dialog: Dialog):
        seen.append((dialog.type, dialog.message))
        dialog.dismiss()  # = Cancel

    page.once("dialog", remember_and_dismiss)
    page.get_by_role("button", name="Click for JS Confirm").click()

    assert seen == [("confirm", "I am a JS Confirm")]
    expect(page.locator("#result")).to_have_text("You clicked: Cancel")


def test_demoqa_confirm(page: Page):
    page.goto("https://demoqa.com/alerts")
    page.once("dialog", lambda d: d.accept())
    page.locator("#confirmButton").click()
    expect(page.locator("#confirmResult")).to_have_text("You selected Ok")
