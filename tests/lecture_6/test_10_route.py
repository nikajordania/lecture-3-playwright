"""Lecture 6 · 10 — page.route: the test answers instead of the server.

Slides "Change the network · picture / code".
Set the route FIRST, then goto.
"""
from playwright.sync_api import Page, expect

BOOKS = "**/BookStore/v1/Books"
BOOKS_PAGE = "https://demoqa.com/books"

FAKE_BOOK = {
    "isbn": "1111111111111",
    "title": "Testing with Playwright",
    "subTitle": "A lecture 6 example",
    "author": "Lecture 6",
    "publish_date": "2026-11-03T00:00:00.000Z",
    "publisher": "BTU",
    "pages": 42,
    "description": "A book that exists only inside this test.",
    "website": "https://playwright.dev/python/",
}


def test_empty_book_list(page: Page):
    # 2 — every request to BOOKS goes to our function
    page.route(BOOKS, lambda route: route.fulfill(
        json={"books": []}))           # 4 — our answer: an empty list
    page.goto(BOOKS_PAGE)               # 1 — the page asks as usual
    expect(page.locator("tbody tr")).to_have_count(0)


def test_one_fake_book(page: Page):
    page.route(BOOKS, lambda route: route.fulfill(json={"books": [FAKE_BOOK]}))
    page.goto(BOOKS_PAGE)
    expect(page.locator("tbody tr")).to_have_count(1)
    expect(page.get_by_role("link", name="Testing with Playwright")).to_be_visible()


def test_books_without_images(page: Page):
    # 3 — abort: the request fails, the page still works
    page.route("**/*.jpg", lambda route: route.abort())
    page.goto(BOOKS_PAGE)
    expect(page.locator("tbody tr").first).to_be_visible()
