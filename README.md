# Lecture 3 · From One Test to a Test Suite

Example tests for every topic of lecture 3. Python, pytest, Playwright and uv.
This project continues `lecture-2-playwright`. There, one test case became one test.
Here, many tests become a test suite.

## Start

```bash
uv sync
uv run playwright install chromium
uv run pytest
```

## Test sites

| Site | Used for |
|---|---|
| https://the-internet.herokuapp.com | login, tables, hovers, checkboxes, dropdown, upload, alerts, new tab, dynamic loading and controls |
| https://demoqa.com | buttons (dynamic ids), droppable, text box, forms, frames, web tables, dynamic properties |
| https://demo.playwright.dev/todomvc | `data-testid`, `get_by_test_id()` |

## Slide → test file

| Package | Slide topic | File |
|---|---|---|
| `locators` | DOM tree, DevTools, CSS selectors | `tests/locators/test_01_css_selectors.py` |
| `locators` | XPath: axes, `contains()`, `last()` | `tests/locators/test_02_xpath.py` |
| `locators` | An id that changes on every load | `tests/locators/test_03_dynamic_ids.py` |
| `locators` | Locator ladder: role, label, placeholder, text, alt, title, test id | `tests/locators/test_04_user_facing_locators.py` |
| `action` | Every gesture has its own method | `tests/action/test_01_actions.py` |
| `action` | Dialogs and new tabs | `tests/action/test_02_dialogs_and_tabs.py` |
| `check` | `expect()` assertions | `tests/check/test_01_assertions.py` |
| `data` | Boundaries, equivalence classes, `parametrize` | `tests/data/test_01_parametrize.py` |
| `data` | Fixture: before / after with `yield` | `tests/data/test_02_fixtures.py` |
| `check` | Many `expect()` conditions (table below) | `tests/check/test_02_expect_combinations.py` |
| `waits` | Actions wait by themselves, `assert` after `wait_for()` vs `expect()` | `tests/waits/test_01_waits.py` |

## Waits

`tests/waits/test_01_waits.py` shows three ways to deal with a slow page:

| Way | How it waits |
|---|---|
| action (`click`, `fill`...) | waits by itself until the element is ready (30 s) |
| `assert` | looks **once**, so call `wait_for()` first |
| `expect` | keeps looking until it passes or `timeout` ends (5 s by default; for slow things use `timeout=10_000`) |

Prefer `expect`: no extra wait line, and a clear error message.
Do not use `time.sleep()` - it always waits the full time.

## Which check for which condition?

| Condition | Check |
|---|---|
| a dialog opened | `page.once("dialog", handler)` before the click |
| all conditions are true | several `expect()` lines |
| any of two elements | `expect(a.or_(b)).to_be_visible()` |
| none of the conditions | several `expect(...).not_to_...()` lines |
| attribute has a value | `expect(loc).to_have_attribute("type", "password")` |
| attribute contains text | `expect(loc).to_have_attribute("href", re.compile("users"))` |
| element can be clicked | `expect(loc).to_be_enabled()` - or just `loc.click()`, it waits |
| checkbox is checked / not checked | `expect(loc).to_be_checked()` / `to_be_checked(checked=False)` |
| option is selected | `expect(loc).to_have_value("2")` |
| element is inside a frame | `page.frame_locator("#frame1").locator(...)` - no switching |
| element is hidden or gone | `expect(loc).to_be_hidden()` / `loc.wait_for(state="hidden")` |
| a new tab opened | `with page.context.expect_page() as info:` / `len(page.context.pages)` |
| element is in the HTML | `expect(loc).to_be_attached()` / `loc.wait_for(state="attached")` |
| number of elements | `expect(loc).to_have_count(n)` |
| element was removed | `expect(loc).to_have_count(0)` / `loc.wait_for(state="detached")` |
| text is in the element | `expect(loc).to_contain_text("...")` |
| input has a value | `expect(loc).to_have_value(re.compile("tom"))` |
| page title | `expect(page).to_have_title("...")` / `to_have_title(re.compile("..."))` |
| page url | `expect(page).to_have_url(...)`, `not_to_have_url(old)`, `page.wait_for_url("**/login")` |
| element is visible | `expect(loc).to_be_visible()` |
| every element is visible | `for el in loc.all(): expect(el).to_be_visible()` |
| at least one is visible | `expect(loc.filter(visible=True)).not_to_have_count(0)` |

## Run

```bash
uv run pytest tests/locators -v                          # one package
uv run pytest tests/check/test_01_assertions.py -v       # one file
uv run pytest -k "bad user" -v                           # one parametrize case by its id
uv run pytest --lf                                       # only the tests that failed last time
uv run pytest tests/action --slowmo 500                  # watch the browser slowly
uv run playwright codegen https://the-internet.herokuapp.com/login   # record clicks as code
```

## If a test is red

- **the-internet.herokuapp.com** is sometimes slow or shows "Application Error". Run again with `uv run pytest --lf`.
- **demoqa.com** is slow because of its ads. `conftest.py` blocks the ad servers (`block_ads` fixture).
- Read the error from top to bottom: which test, what was expected, what was actually there, which locator.
