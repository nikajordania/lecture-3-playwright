"""11 · Screenshots. screenshot() on a page or on a locator.

The slide saves into shots/. Here we use tmp_path so the project stays clean.
Automatic screenshots of failed tests (no code):
    uv run pytest --screenshot only-on-failure      -> test-results/<test>/test-failed-1.png
"""
from pathlib import Path

from playwright.sync_api import Page


def test_screenshots(page: Page, tmp_path: Path):
    page.goto("https://the-internet.herokuapp.com/tables")
    page.screenshot(path=tmp_path / "visible.png")  # 1  what fits on the screen
    page.screenshot(path=tmp_path / "full.png", full_page=True)  # 2  the whole page
    page.locator("#table1").screenshot(path=tmp_path / "table.png")  # 3  one element

    for name in ["visible.png", "full.png", "table.png"]:
        assert (tmp_path / name).stat().st_size > 0


def test_screenshot_as_bytes(page: Page):
    page.goto("https://the-internet.herokuapp.com/tables")
    data = page.screenshot()  # no path -> the picture comes back as bytes
    assert data[:4] == b"\x89PNG"
