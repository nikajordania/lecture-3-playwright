"""Selenium expected_conditions  ->  Playwright.

Selenium:   WebDriverWait(driver, 10).until(EC.<condition>(...))
Playwright: expect(...).<check>(timeout=10_000)  - or no wait code at all,
            because actions wait by themselves.

Every test below starts with the Selenium line it replaces.
The full table is in tests/waits/README.md.
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


# --- alert_is_present ---------------------------------------------------------
def test_alert_is_present(page: Page):
    # Selenium: WebDriverWait(driver, 6).until(EC.alert_is_present()).accept()
    page.goto(f"{THE_INTERNET}/javascript_alerts")
    seen = []

    def accept(dialog: Dialog):
        seen.append(dialog.type)  # "alert", "confirm" or "prompt"
        dialog.accept()

    page.once("dialog", accept)  # register BEFORE the click
    page.get_by_role("button", name="Click for JS Alert").click()

    assert seen == ["alert"]
    expect(page.locator("#result")).to_have_text("You successfully clicked an alert")


# --- all_of / any_of / none_of ------------------------------------------------
def test_all_of(page: Page):
    # Selenium: EC.all_of(EC.url_contains("secure"), EC.visibility_of_element_located(...))
    login(page)
    expect(page).to_have_url(re.compile("secure"))  # all of them = one expect per line
    expect(page.get_by_role("heading", name="Secure Area")).to_be_visible()
    expect(page.locator("#flash")).to_contain_text("You logged into a secure area!")


def test_any_of(page: Page):
    # Selenium: EC.any_of(EC.visibility_of_element_located(SUCCESS), EC.visibility_of_element_located(ERROR))
    login(page, password="wrong")
    success_or_error = page.locator(".flash.success").or_(page.locator(".flash.error"))
    expect(success_or_error).to_be_visible()  # whichever comes first
    expect(success_or_error).to_contain_text("Your password is invalid!")


def test_none_of(page: Page):
    # Selenium: EC.none_of(EC.url_contains("secure"), EC.visibility_of_element_located(SUCCESS))
    login(page, password="wrong")
    expect(page).not_to_have_url(re.compile("secure"))
    expect(page.locator(".flash.success")).not_to_be_visible()


# --- attributes -----------------------------------------------------------------
def test_element_attribute_to_include(page: Page):
    # Selenium: EC.element_attribute_to_include((By.ID, "password"), "type")
    page.goto(f"{THE_INTERNET}/login")
    expect(page.get_by_label("Password")).to_have_attribute("type", "password")


def test_text_to_be_present_in_element_attribute(page: Page):
    # Selenium: EC.text_to_be_present_in_element_attribute((By.CSS_SELECTOR, "a"), "href", "users")
    page.goto(f"{THE_INTERNET}/hovers")
    page.locator(".figure").first.hover()
    expect(page.get_by_role("link", name="View profile")).to_have_attribute("href", re.compile("users"))


# --- selected / checked -----------------------------------------------------------
def test_element_to_be_selected_and_selection_state(page: Page):
    # Selenium: EC.element_to_be_selected(el)                         -> to_be_checked()
    #           EC.element_located_to_be_selected(locator)            -> to_be_checked()
    #           EC.element_selection_state_to_be(el, False)           -> to_be_checked(checked=False)
    #           EC.element_located_selection_state_to_be(loc, False)  -> to_be_checked(checked=False)
    page.goto(f"{THE_INTERNET}/checkboxes")
    boxes = page.locator("#checkboxes input")

    expect(boxes.nth(0)).to_be_checked(checked=False)
    boxes.nth(0).check()
    expect(boxes.nth(0)).to_be_checked()


def test_option_to_be_selected(page: Page):
    # Selenium: EC.element_to_be_selected(driver.find_element(By.CSS_SELECTOR, "option[value='2']"))
    page.goto(f"{THE_INTERNET}/dropdown")
    page.locator("#dropdown").select_option("2")
    expect(page.locator("#dropdown")).to_have_value("2")
    expect(page.locator("#dropdown option:checked")).to_have_text("Option 2")


# --- clickable ---------------------------------------------------------------------
def test_element_to_be_clickable(page: Page):
    # Selenium: WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "enableAfter"))).click()
    page.goto(f"{DEMOQA}/dynamic-properties")
    button = page.locator("#enableAfter")  # disabled for the first ~5 s

    expect(button).to_be_enabled(timeout=10_000)  # the explicit check...
    button.click()  # ...but click() alone would also wait until it is enabled


# --- frames --------------------------------------------------------------------------
def test_frame_to_be_available_and_switch_to_it(page: Page):
    # Selenium: WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it("frame1"))
    #           ... driver.switch_to.default_content()
    page.goto(f"{DEMOQA}/frames")
    # No switching: a frame_locator looks inside the frame, page stays the page.
    frame = page.frame_locator("#frame1")
    expect(frame.locator("#sampleHeading")).to_have_text("This is a sample page")
    expect(page.get_by_role("heading", name="Frames")).to_be_visible()  # still the main page


# --- invisibility ----------------------------------------------------------------------
def test_invisibility_of_element_located(page: Page):
    # Selenium: EC.invisibility_of_element_located((By.ID, "loading"))
    #           EC.invisibility_of_element(element)
    page.goto(f"{THE_INTERNET}/dynamic_loading/1")
    page.get_by_role("button", name="Start").click()
    expect(page.locator("#loading")).to_be_hidden(timeout=10_000)


# --- windows ------------------------------------------------------------------------------
def test_new_window_is_opened_and_number_of_windows(page: Page):
    # Selenium: EC.new_window_is_opened(handles_before)
    #           EC.number_of_windows_to_be(2)
    page.goto(f"{THE_INTERNET}/windows")
    with page.context.expect_page() as new_page_info:
        page.get_by_role("link", name="Click Here").click()
    new_page = new_page_info.value

    assert len(page.context.pages) == 2
    expect(new_page.get_by_role("heading")).to_have_text("New Window")


# --- presence (in the HTML) vs visibility (on the screen) ---------------------------------
def test_presence_of_element_located(page: Page):
    # Selenium: EC.presence_of_element_located((By.ID, "finish"))
    page.goto(f"{THE_INTERNET}/dynamic_loading/1")
    finish = page.locator("#finish")
    expect(finish).to_be_attached()  # it IS in the HTML...
    expect(finish).not_to_be_visible()  # ...but not on the screen yet


def test_presence_of_all_elements_located(page: Page):
    # Selenium: EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#elements button"))
    page.goto(f"{THE_INTERNET}/add_remove_elements/")
    add = page.get_by_role("button", name="Add Element")
    for _ in range(3):
        add.click()
    expect(page.locator("#elements button")).to_have_count(3)


# --- staleness -------------------------------------------------------------------------------
def test_staleness_of(page: Page):
    # Selenium: EC.staleness_of(element) - the old element was removed from the page.
    page.goto(f"{THE_INTERNET}/dynamic_controls")
    checkbox = page.locator("#checkbox")

    page.get_by_role("button", name="Remove").click()
    expect(checkbox).to_have_count(0)  # gone from the HTML

    # A Playwright locator never becomes "stale": it searches again every time.
    # Selenium would throw StaleElementReferenceException with the old element.
    page.get_by_role("button", name="Add").click()
    expect(checkbox).to_be_attached()  # the SAME locator finds the new checkbox


# --- text -------------------------------------------------------------------------------------
def test_text_to_be_present_in_element(page: Page):
    # Selenium: EC.text_to_be_present_in_element((By.ID, "flash"), "secure area")
    login(page)
    expect(page.locator("#flash")).to_contain_text("secure area")


def test_text_to_be_present_in_element_value(page: Page):
    # Selenium: EC.text_to_be_present_in_element_value((By.ID, "username"), "tom")
    page.goto(f"{THE_INTERNET}/login")
    page.get_by_label("Username").fill("tomsmith")
    expect(page.get_by_label("Username")).to_have_value(re.compile("tom"))


# --- title -----------------------------------------------------------------------------------
def test_title_is_and_title_contains(page: Page):
    # Selenium: EC.title_is("The Internet") / EC.title_contains("Internet")
    page.goto(THE_INTERNET)
    expect(page).to_have_title("The Internet")
    expect(page).to_have_title(re.compile("Internet"))


# --- url --------------------------------------------------------------------------------------
def test_url_changes_contains_matches_to_be(page: Page):
    page.goto(THE_INTERNET)
    old_url = page.url
    page.get_by_role("link", name="Form Authentication").click()

    expect(page).not_to_have_url(old_url)  # EC.url_changes(old_url)
    expect(page).to_have_url(re.compile("login"))  # EC.url_contains("login")
    expect(page).to_have_url(re.compile(r".*/login$"))  # EC.url_matches(r".*/login$")
    expect(page).to_have_url(f"{THE_INTERNET}/login")  # EC.url_to_be(".../login")
    page.wait_for_url("**/login")  # the same as a wait without a check


# --- visibility -----------------------------------------------------------------------------
def test_visibility_of_element_located(page: Page):
    # Selenium: EC.visibility_of_element_located((By.ID, "finish"))
    #           EC.visibility_of(element)
    page.goto(f"{THE_INTERNET}/dynamic_loading/1")
    page.get_by_role("button", name="Start").click()
    expect(page.locator("#finish")).to_be_visible(timeout=10_000)


def test_visibility_of_all_elements_located(page: Page):
    # Selenium: EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#table1 tbody tr"))
    page.goto(f"{THE_INTERNET}/tables")
    rows = page.locator("#table1 tbody tr")
    expect(rows).to_have_count(4)
    for row in rows.all():
        expect(row).to_be_visible()


def test_visibility_of_any_elements_located(page: Page):
    # Selenium: EC.visibility_of_any_elements_located((By.CSS_SELECTOR, ".figcaption"))
    page.goto(f"{THE_INTERNET}/hovers")
    captions = page.locator(".figcaption")
    expect(captions.filter(visible=True)).to_have_count(0)  # all 3 hidden

    page.locator(".figure").nth(2).hover()
    expect(captions.filter(visible=True)).to_have_count(1)  # one is visible now
