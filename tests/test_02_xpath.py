"""01 · Find — XPath.

Slide: "Locator ladder" (XPath is the last step: use it when nothing else works).
Page:  https://the-internet.herokuapp.com/tables
       Table "Example 1" (#table1) has NO class names, so CSS cannot say
       "the e-mail of Jason". XPath can walk from one cell to another.

    Last Name | First Name | Email            | Due     | Web Site | Action
    Smith     | John       | jsmith@gmail.com | $50.00  | ...      | edit delete
    Bach      | Frank      | fbach@yahoo.com  | $51.00  | ...      | edit delete
    Doe       | Jason      | jdoe@hotmail.com | $100.00 | ...      | edit delete
    Conway    | Tim        | tconway@...      | $50.00  | ...      | edit delete

Try in DevTools -> Console:  $x("//table[@id='table1']//td[text()='Jason']")
"""
from playwright.sync_api import Page, expect

TABLES = "https://the-internet.herokuapp.com/tables"
CHALLENGING_DOM = "https://the-internet.herokuapp.com/challenging_dom"

TABLE1 = "//table[@id='table1']"


def test_xpath_prefix_and_text(page: Page):
    page.goto(TABLES)
    # A selector that starts with // is XPath. "xpath=" makes it explicit.
    expect(page.locator("xpath=//h3")).to_have_text("Data Tables")
    expect(page.locator(f"{TABLE1}//td[text()='Jason']")).to_be_visible()


def test_following_and_preceding_sibling(page: Page):
    page.goto(TABLES)
    jason = f"{TABLE1}//td[text()='Jason']"
    # following-sibling::td[1] = the next cell to the right -> Email
    expect(page.locator(f"{jason}/following-sibling::td[1]")).to_have_text("jdoe@hotmail.com")
    # preceding-sibling::td = the cell to the left -> Last Name
    expect(page.locator(f"{jason}/preceding-sibling::td")).to_have_text("Doe")


def test_parent_and_position(page: Page):
    page.goto(TABLES)
    # Go UP to the row (parent::tr), then DOWN to the 4th cell (Due).
    due = page.locator(f"{TABLE1}//td[text()='jdoe@hotmail.com']/parent::tr/td[4]")
    expect(due).to_have_text("$100.00")

    # (...)[last()] = the last match on the page
    expect(page.locator(f"({TABLE1}//tbody/tr)[last()]/td[1]")).to_have_text("Conway")
    expect(page.locator(f"{TABLE1}//tbody/tr")).to_have_count(4)


def test_contains_and_starts_with(page: Page):
    page.goto(TABLES)
    # contains(text(), '...') = part of the text
    expect(page.locator(f"{TABLE1}//td[contains(text(), '@yahoo')]")).to_have_text(
        "fbach@yahoo.com"
    )
    # starts-with() and "and"
    expect(
        page.locator(f"{TABLE1}//td[starts-with(text(), '$5') and contains(text(), '.00')]")
    ).to_have_count(3)  # $50.00, $51.00, $50.00


def test_xpath_in_a_table_without_ids(page: Page):
    page.goto(CHALLENGING_DOM)
    # "The edit link in the row of Iuvaret3": no id, no class - only text.
    edit = page.locator("//td[text()='Iuvaret3']/following-sibling::td/a[text()='edit']")
    expect(edit).to_have_attribute("href", "#edit")
