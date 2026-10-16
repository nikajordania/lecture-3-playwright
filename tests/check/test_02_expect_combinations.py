"""expect() in many combinations - each test waits for a different condition.

    expect(locator).to_be_visible / to_be_hidden / to_be_attached / to_be_enabled
    expect(locator).to_have_text / to_contain_text / to_have_value / to_have_attribute
    expect(locator).to_be_checked / to_have_count
    expect(page).to_have_url / to_have_title
    .not_to_...()  and  locator.or_()  for "not" and "either".

Pass timeout=10_000 where the page is slow (default is 5 s).
"""
import re

from playwright.sync_api import Dialog, Page, expect

THE_INTERNET = "https://the-internet.herokuapp.com"
DEMOQA = "https://demoqa.com"


def login(page: Page, password="SuperSecretPassword!"):
    page.goto(f"{THE_INTERNET}/login")
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Login").click()


# --- dialog ---
def test_alert_is_present(page: Page):
    page.goto(f"{THE_INTERNET}/javascript_alerts")
    seen = []

    def accept(dialog: Dialog):
        seen.append(dialog.type)  # "alert", "confirm" or "prompt"
        dialog.accept()

    page.once("dialog", accept)  # register BEFORE the click
    page.get_by_role("button", name="Click for JS Alert").click()

    assert seen == ["alert"]
    expect(page.locator("#result")).to_have_text("You successfully clicked an alert")


# --- all, any, none ---
def test_all_of(page: Page):
    login(page)
    expect(page).to_have_url(re.compile("secure"))  # all of them = one expect per line
    expect(page.get_by_role("heading", name="Secure Area", exact=True)).to_be_visible()
    expect(page.locator("#flash")).to_contain_text("You logged into a secure area!", timeout=10_000)


def test_any_of(page: Page):
    login(page, password="wrong")
    success_or_error = page.locator(".flash.success").or_(page.locator(".flash.error"))
    expect(success_or_error).to_be_visible(timeout=10_000)  # whichever comes first
    expect(success_or_error).to_contain_text("Your password is invalid!")


def test_none_of(page: Page):
    login(page, password="wrong")
    expect(page).not_to_have_url(re.compile("secure"))
    expect(page.locator(".flash.success")).not_to_be_visible()


# --- attributes -----------------------------------------------------------------
def test_element_attribute_to_include(page: Page):
    page.goto(f"{THE_INTERNET}/login")
    expect(page.get_by_label("Password")).to_have_attribute("type", "password")


def test_text_to_be_present_in_element_attribute(page: Page):
    page.goto(f"{THE_INTERNET}/hovers")
    page.locator(".figure").first.hover()
    expect(page.get_by_role("link", name="View profile")).to_have_attribute("href", re.compile("users"))


# --- checked / selected ---
def test_element_to_be_selected_and_selection_state(page: Page):
    page.goto(f"{THE_INTERNET}/checkboxes")
    boxes = page.locator("#checkboxes input")

    expect(boxes.nth(0)).to_be_checked(checked=False)
    boxes.nth(0).check()
    expect(boxes.nth(0)).to_be_checked()


def test_option_to_be_selected(page: Page):
    page.goto(f"{THE_INTERNET}/dropdown")
    page.locator("#dropdown").select_option("2")
    expect(page.locator("#dropdown")).to_have_value("2")
    expect(page.locator("#dropdown option:checked")).to_have_text("Option 2")


# --- enabled ---
def test_element_to_be_clickable(page: Page):
    page.goto(f"{DEMOQA}/dynamic-properties")
    button = page.locator("#enableAfter")  # disabled for the first ~5 s

    expect(button).to_be_enabled(timeout=10_000)  # the explicit check...
    button.click()  # ...but click() alone would also wait until it is enabled


# --- frames --------------------------------------------------------------------------
def test_frame_to_be_available_and_switch_to_it(page: Page):
    page.goto(f"{DEMOQA}/frames")
    # No switching: a frame_locator looks inside the frame, page stays the page.
    frame = page.frame_locator("#frame1")
    expect(frame.locator("#sampleHeading")).to_have_text("This is a sample page")
    expect(page.get_by_role("heading", name="Frames")).to_be_visible()  # still the main page


# --- hidden ---
def test_invisibility_of_element_located(page: Page):
    page.goto(f"{THE_INTERNET}/dynamic_loading/1")
    page.get_by_role("button", name="Start").click()
    expect(page.locator("#loading")).to_be_hidden(timeout=10_000)


# --- windows ------------------------------------------------------------------------------
def test_new_window_is_opened_and_number_of_windows(page: Page):
    page.goto(f"{THE_INTERNET}/windows")
    with page.context.expect_page() as new_page_info:
        page.get_by_role("link", name="Click Here").click()
    new_page = new_page_info.value

    assert len(page.context.pages) == 2
    expect(new_page.get_by_role("heading")).to_have_text("New Window")


# --- attached (in the HTML) vs visible (on the screen) ---
def test_presence_of_element_located(page: Page):
    page.goto(f"{THE_INTERNET}/dynamic_loading/1")
    finish = page.locator("#finish")
    expect(finish).to_be_attached()  # it IS in the HTML...
    expect(finish).not_to_be_visible()  # ...but not on the screen yet


def test_presence_of_all_elements_located(page: Page):
    page.goto(f"{THE_INTERNET}/add_remove_elements/")
    add = page.get_by_role("button", name="Add Element")
    for _ in range(3):
        add.click()
    expect(page.locator("#elements button")).to_have_count(3)


# --- removed and added again ---
def test_staleness_of(page: Page):
    page.goto(f"{THE_INTERNET}/dynamic_controls")
    checkbox = page.locator("#checkbox")

    page.get_by_role("button", name="Remove").click()
    expect(checkbox).to_have_count(0)  # gone from the HTML

    # A Playwright locator never becomes "stale": it searches again every time.
    page.get_by_role("button", name="Add").click()
    expect(checkbox).to_be_attached()  # the SAME locator finds the new checkbox


# --- text -------------------------------------------------------------------------------------
def test_text_to_be_present_in_element(page: Page):
    login(page)
    expect(page.locator("#flash")).to_contain_text("secure area", timeout=10_000)


def test_text_to_be_present_in_element_value(page: Page):
    page.goto(f"{THE_INTERNET}/login")
    page.get_by_label("Username").fill("tomsmith")
    expect(page.get_by_label("Username")).to_have_value(re.compile("tom"))


# --- title -----------------------------------------------------------------------------------
def test_title_is_and_title_contains(page: Page):
    page.goto(THE_INTERNET)
    expect(page).to_have_title("The Internet")
    expect(page).to_have_title(re.compile("Internet"))


# --- url --------------------------------------------------------------------------------------
def test_url_changes_contains_matches_to_be(page: Page):
    page.goto(THE_INTERNET)
    old_url = page.url
    page.get_by_role("link", name="Form Authentication").click()

    expect(page).not_to_have_url(old_url)
    expect(page).to_have_url(re.compile("login"))
    expect(page).to_have_url(re.compile(r".*/login$"))
    expect(page).to_have_url(f"{THE_INTERNET}/login")
    page.wait_for_url("**/login")  # the same as a wait without a check


# --- visibility -----------------------------------------------------------------------------
def test_visibility_of_element_located(page: Page):
    page.goto(f"{THE_INTERNET}/dynamic_loading/1")
    page.get_by_role("button", name="Start").click()
    expect(page.locator("#finish")).to_be_visible(timeout=10_000)


def test_visibility_of_all_elements_located(page: Page):
    page.goto(f"{THE_INTERNET}/tables")
    rows = page.locator("#table1 tbody tr")
    expect(rows).to_have_count(4)
    for row in rows.all():
        expect(row).to_be_visible()


def test_visibility_of_any_elements_located(page: Page):
    page.goto(f"{THE_INTERNET}/hovers")
    captions = page.locator(".figcaption")
    expect(captions.filter(visible=True)).to_have_count(0)  # all 3 hidden

    page.locator(".figure").nth(2).hover()
    expect(captions.filter(visible=True)).to_have_count(1)  # one is visible now
