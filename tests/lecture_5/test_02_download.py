"""Lecture 5 · 02 — Download: click a link, catch the file.

Slides "02 · Download · picture / code".
The list on the-internet /download is uploaded by users and changes
every day, so the test never hard-codes a file name: it takes the
first link and compares the downloaded name with the link text.
"""
from pathlib import Path

from playwright.sync_api import Page

URL = "https://the-internet.herokuapp.com/download"


def test_download(page: Page, tmp_path: Path):
    page.goto(URL)
    # 1 — any file is fine, keep its name
    link = page.locator(".example a").first
    name = link.inner_text().strip()
    # 2 — start waiting for the download, then click
    with page.expect_download() as info:
        link.click()
    download = info.value
    # 3 — the name the server gives the file
    assert download.suggested_filename == name
    # 4 — tmp_path: a new empty folder for this test (pytest fixture)
    path = tmp_path / download.suggested_filename
    download.save_as(path)
    assert path.exists()
    assert path.stat().st_size > 0, "the file is empty"
