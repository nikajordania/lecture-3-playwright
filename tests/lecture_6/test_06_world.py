"""Lecture 6 · 06 — The user's world: language, time zone, place, theme.

Slides "Sensors and Rendering fake the user's world" and its code twin.
"""
import pytest
from playwright.sync_api import Browser, Page

TBILISI = {"latitude": 41.7151, "longitude": 44.8271}


@pytest.fixture
def tbilisi_page(browser: Browser):
    context = browser.new_context(
        locale="ka-GE",
        timezone_id="Asia/Tbilisi",
        geolocation=TBILISI,
        permissions=["geolocation"],   # no "Allow location?" pop-up
        color_scheme="dark",
    )
    page = context.new_page()
    page.goto("https://playwright.dev/python/")
    yield page
    context.close()


def test_language(tbilisi_page: Page):
    assert tbilisi_page.evaluate("navigator.language") == "ka-GE"


def test_time_zone(tbilisi_page: Page):
    zone = tbilisi_page.evaluate("Intl.DateTimeFormat().resolvedOptions().timeZone")
    assert zone == "Asia/Tbilisi"


def test_location(tbilisi_page: Page):
    coords = tbilisi_page.evaluate("""() => new Promise(done =>
        navigator.geolocation.getCurrentPosition(
            p => done([p.coords.latitude, p.coords.longitude])))""")
    assert coords == [TBILISI["latitude"], TBILISI["longitude"]]


def test_dark_theme(tbilisi_page: Page):
    dark = tbilisi_page.evaluate("matchMedia('(prefers-color-scheme: dark)').matches")
    assert dark is True
