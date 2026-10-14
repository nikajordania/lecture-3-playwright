"""01 · Find — CSS selectors.

Slides: "DOM tree", "DevTools: inspect and copy", "Locator ladder".
Page:   https://the-internet.herokuapp.com/tables
        Table "Example 2" (#table2) has class names on every cell.

Open the page, press F12 and try every selector in the Console:
    document.querySelectorAll("#table2 td.last-name")
"""
import pytest
from playwright.sync_api import Page, expect

TABLES = "https://the-internet.herokuapp.com/tables"
TEXT_BOX = "https://demoqa.com/text-box"


@pytest.mark.smoke
def test_by_id(page: Page):
    # #id  ->  <table id="table2">
    page.goto(TABLES)
    expect(page.locator("#table2")).to_be_visible()


def test_by_class(page: Page):
    page.goto(TABLES)
    # .class  ->  every element with class="last-name" inside #table2.
    # The header <span class="last-name"> matches too: 1 + 4 rows = 5.
    expect(page.locator("#table2 .last-name")).to_have_count(5)

    # tag.class  ->  only <td class="last-name">: the 4 data rows.
    expect(page.locator("#table2 td.last-name")).to_have_count(4)


def test_by_attribute(page: Page):
    page.goto(TABLES)
    # [attribute='value']  ->  <a href="#edit">
    expect(page.locator("#table2 a[href='#edit']")).to_have_count(4)
    # The same links exist in #table1 too: 8 on the whole page.
    expect(page.locator("a[href='#edit']")).to_have_count(8)


def test_descendant_child_and_nth_child(page: Page):
    page.goto(TABLES)
    # "A B"  = B somewhere inside A (descendant)
    # "A > B" = B directly inside A (child)
    rows = page.locator("#table2 tbody > tr")
    expect(rows).to_have_count(4)

    # :nth-child(3) = the 3rd row  ->  Doe, Jason
    expect(page.locator("#table2 tbody > tr:nth-child(3) td.first-name")).to_have_text("Jason")
    # :first-child / :last-child
    expect(page.locator("#table2 tbody > tr:first-child td.last-name")).to_have_text("Smith")
    expect(page.locator("#table2 tbody > tr:last-child td.last-name")).to_have_text("Conway")


def test_playwright_has_text_pseudo_class(page: Page):
    page.goto(TABLES)
    # :has-text() is NOT standard CSS - it is a Playwright extension.
    # "the row that contains Conway"  ->  its e-mail cell
    expect(page.locator("#table2 tr:has-text('Conway') td.email")).to_have_text(
        "tconway@earthlink.net"
    )


def test_form_fields_by_css(page: Page):
    page.goto(TEXT_BOX)
    # Same form, three different CSS ideas:
    page.locator("input[placeholder='Full Name']").fill("Anna Test")  # attribute
    page.locator("input[type='email']").fill("anna@test.ge")  # tag + attribute
    page.locator("textarea#currentAddress").fill("Tbilisi")  # tag + id
    page.locator("#submit").click()  # id

    expect(page.locator("#output #name")).to_have_text("Name:Anna Test")
    expect(page.locator("#output #email")).to_have_text("Email:anna@test.ge")
