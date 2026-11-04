"""Lecture 6 · 02 — Network: watch requests, go offline, block files.

Slides "Network · picture / code".
demoqa.com/books builds its table from the JSON of /BookStore/v1/Books.
"""
import pytest
from playwright.sync_api import BrowserContext, Error, Page, expect

BOOKS_PAGE = "https://demoqa.com/books"
SAUCE = "https://www.saucedemo.com/"


def test_books_request(page: Page):
    # 1 — wait for one request by its URL pattern
    with page.expect_response("**/BookStore/v1/Books") as info:
        page.goto(BOOKS_PAGE)
    response = info.value
    # 2 — status and body, like the Network panel
    assert response.status == 200
    books = response.json()["books"]
    # the table shows exactly the books from the JSON
    expect(page.locator("tbody tr")).to_have_count(len(books))


def test_offline(page: Page, context: BrowserContext):
    page.goto(SAUCE)
    # 3 — like the "Offline" option in Network
    context.set_offline(True)
    with pytest.raises(Error):
        page.reload()  # no internet → Playwright raises an error
    context.set_offline(False)


def test_without_images(page: Page):
    # 4 — like "Block request URL": every .jpg request fails
    page.route("**/*.jpg", lambda route: route.abort())
    page.goto(BOOKS_PAGE)
    expect(page.locator("tbody tr").first).to_be_visible()
    # the picture did not load: its natural width is 0
    width = page.locator("tbody img").first.evaluate("img => img.naturalWidth")
    assert width == 0
