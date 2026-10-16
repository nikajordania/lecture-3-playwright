"""05 · Debug — a red test on purpose, to practise with the trace.

Slides: "The trace replays a failed test, step by step",
        "The failed test already wrote half the report".

This test is marked `broken`. pyproject.toml hides it from a normal run
(addopts = -m "not broken"). Run it on purpose:

    uv run pytest -m broken --tracing retain-on-failure
    uv run playwright show-trace test-results/<folder of the test>/trace.zip

Other ways to look at a failure:
    uv run pytest -m broken --headed --slowmo 500         watch it
    uv run pytest -m broken --screenshot only-on-failure  a picture
    $env:PWDEBUG=1; uv run pytest -m broken               step by step (PowerShell)
    page.pause()  in the code                             stop here and open the Inspector
"""
import pytest
from playwright.sync_api import Page, expect

LOGIN = "https://the-internet.herokuapp.com/login"


@pytest.mark.broken
def test_login_with_a_typo_in_the_locator(page: Page):
    page.goto(LOGIN)
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()

    # BUG IN THE TEST: "#flsh" instead of "#flash".
    # The trace shows: the login worked, the message is on the page,
    # only our locator finds nothing -> fix the test, not the app.
    expect(page.locator("#flsh")).to_contain_text("secure area", timeout=3_000)
