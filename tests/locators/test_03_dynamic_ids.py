"""Locators — dynamic ids.

Slide: "An id that changes on every load".
Page:  https://demoqa.com/buttons
       The "Click Me" button gets a NEW random id on every page load,
       for example id="XopAA" now and id="hmvdI" after a reload.
       A locator built on that id works once and then breaks.
"""
from playwright.sync_api import Page, expect

BUTTONS = "https://demoqa.com/buttons"
CHALLENGING_DOM = "https://the-internet.herokuapp.com/challenging_dom"


def test_id_changes_after_reload(page: Page):
    page.goto(BUTTONS)
    click_me = page.get_by_role("button", name="Click Me", exact=True)

    first_id = click_me.get_attribute("id")
    page.reload()
    second_id = click_me.get_attribute("id")

    print(f"\nload 1: #{first_id}   load 2: #{second_id}")  # see it with: pytest -s
    # Two plain Python strings -> a plain assert is fine here.
    assert first_id != second_id


def test_locator_by_old_id_finds_nothing(page: Page):
    page.goto(BUTTONS)
    old_id = page.get_by_role("button", name="Click Me", exact=True).get_attribute("id")

    page.reload()

    # The id copied from DevTools a minute ago does not exist any more.
    expect(page.locator(f"#{old_id}")).to_have_count(0)


def test_stable_locator_by_role_works_on_every_load(page: Page):
    page.goto(BUTTONS)
    page.get_by_role("button", name="Click Me", exact=True).click()
    expect(page.locator("#dynamicClickMessage")).to_have_text("You have done a dynamic click")

    page.reload()
    page.get_by_role("button", name="Click Me", exact=True).click()
    expect(page.locator("#dynamicClickMessage")).to_have_text("You have done a dynamic click")


def test_stable_class_instead_of_generated_id(page: Page):
    page.goto(CHALLENGING_DOM)
    # These buttons have ids like "ba6d2130-aa04-013f-...", new on every load.
    green_button = page.locator("a.button.success")  # the class does not change
    first_id = green_button.get_attribute("id")

    page.reload()

    expect(green_button).to_be_visible()
    assert green_button.get_attribute("id") != first_id
