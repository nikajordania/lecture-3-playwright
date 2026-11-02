"""Lecture 5 · 01 — iframes: a page inside a page.

Slides "01 · iframes · picture / code".
A locator on `page` searches only the main document. To look inside
an iframe, first make a frame locator, then search inside it.
"""
from playwright.sync_api import Page, expect

DEMOQA_FRAMES = "https://demoqa.com/frames"
NESTED_FRAMES = "https://the-internet.herokuapp.com/nested_frames"


def test_iframe(page: Page):
    page.goto(DEMOQA_FRAMES)
    # 1 — from the main page the heading is not found: it lives in the iframe
    expect(page.locator("#sampleHeading")).to_have_count(0)
    # 2 — a locator for the iframe element
    frame = page.frame_locator("#frame1")
    # 3 — search inside the frame, expect works as usual
    heading = frame.locator("#sampleHeading")
    expect(heading).to_have_text("This is a sample page")
    # no "switch back" needed: page is still the main page
    expect(page.get_by_role("heading", name="Frames", exact=True)).to_be_visible()


def test_nested_frames(page: Page):
    page.goto(NESTED_FRAMES)
    # 4 — a frame inside a frame: chain frame_locator twice
    top = page.frame_locator('frame[name="frame-top"]')
    middle = top.frame_locator('frame[name="frame-middle"]')
    expect(middle.locator("#content")).to_have_text("MIDDLE")


def test_frame_by_name(page: Page):
    """Another way: page.frame(name=...) gives a Frame object.

    A Frame has the same methods as page: locator(), get_by_role(), ...
    """
    page.goto(NESTED_FRAMES)
    bottom = page.frame(name="frame-bottom")
    assert bottom is not None, "frame-bottom not found"
    expect(bottom.locator("body")).to_have_text("BOTTOM")
