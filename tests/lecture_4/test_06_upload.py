"""06 · Upload a file. set_input_files() fills a file input — no file dialog."""
from pathlib import Path

from playwright.sync_api import Page, expect


def test_upload(page: Page, tmp_path: Path):
    cv = tmp_path / "cv.txt"  # 1  tmp_path: a new empty folder for this test
    cv.write_text("Anna Test - QA")
    page.goto("https://the-internet.herokuapp.com/upload")
    page.locator("#file-upload").set_input_files(cv)  # 2
    page.locator("#file-submit").click()  # 3
    expect(page.locator("h3")).to_have_text("File Uploaded!")  # 4
    expect(page.locator("#uploaded-files")).to_have_text("cv.txt")


def test_upload_from_memory(page: Page):
    # No file on the disk at all.
    page.goto("https://the-internet.herokuapp.com/upload")
    page.locator("#file-upload").set_input_files(
        files=[{"name": "notes.txt", "mimeType": "text/plain", "buffer": b"hello"}]
    )
    page.locator("#file-submit").click()
    expect(page.locator("#uploaded-files")).to_have_text("notes.txt")
