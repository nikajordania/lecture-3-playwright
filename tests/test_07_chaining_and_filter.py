"""01 · Find — chaining and filter().

Slide: "Zoom in: a locator inside a locator".
Each step makes the search area smaller:
    page.locator(".figure")  ->  .nth(1)  ->  .locator(".figcaption")
       all 3 cards              2nd card       only its caption
"""
from playwright.sync_api import Page, expect

THE_INTERNET = "https://the-internet.herokuapp.com"
WEBTABLES = "https://demoqa.com/webtables"


def test_chain_hover_card_caption(page: Page):
    page.goto(f"{THE_INTERNET}/hovers")

    card = page.locator(".figure").nth(1)  # the 2nd card
    caption = card.locator(".figcaption")  # search ONLY inside that card

    expect(caption).to_be_hidden()  # the caption appears only on hover
    card.hover()
    expect(caption).to_be_visible()
    expect(caption.get_by_role("heading")).to_have_text("name: user2")
    expect(caption.get_by_role("link", name="View profile")).to_have_attribute("href", "/users/2")


def test_filter_row_by_text_then_find_inside(page: Page):
    page.goto(f"{THE_INTERNET}/tables")

    # "the row that contains Jason" - no XPath needed
    jason_row = page.locator("#table1 tbody tr").filter(has_text="Jason")
    expect(jason_row).to_have_count(1)
    expect(jason_row.locator("td").nth(2)).to_have_text("jdoe@hotmail.com")
    expect(jason_row.get_by_role("link", name="edit")).to_have_attribute("href", "#edit")


def test_filter_has_and_has_not(page: Page):
    page.goto(f"{THE_INTERNET}/tables")
    rows = page.locator("#table1 tbody tr")

    # has= another locator: rows that contain a cell "$50.00" (Smith, Conway)
    fifty = rows.filter(has=page.get_by_text("$50.00", exact=True))
    expect(fifty).to_have_count(2)

    # has_not_text=: every row except Smith
    expect(rows.filter(has_not_text="Smith")).to_have_count(3)


def test_filter_text_is_a_part_match(page: Page):
    page.goto(WEBTABLES)
    rows = page.get_by_role("row")

    # "ierra" is inside "Cierra" AND "Kierra" - be careful with short texts
    expect(rows.filter(has_text="ierra")).to_have_count(2)
    expect(rows.filter(has_text="Kierra")).to_have_count(1)


def test_delete_one_row_in_web_table(page: Page):
    page.goto(WEBTABLES)

    alden = page.get_by_role("row").filter(has_text="Alden")
    alden.get_by_title("Delete").click()  # the Delete icon of THIS row only

    expect(alden).to_have_count(0)
    expect(page.get_by_role("row").filter(has_text="Cierra")).to_have_count(1)
