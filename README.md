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
| https://the-internet.herokuapp.com | login, tables, hovers, checkboxes, dropdown, keys, upload, alerts, new tab, dynamic loading |
| https://demoqa.com | dynamic ids, strict mode, buttons, droppable, select menu, web tables, dynamic properties, forms |
| https://demo.playwright.dev/todomvc | `data-testid`, `get_by_test_id()` |

## Slide → test file

| Part | Slide topic | File |
|---|---|---|
| 01 Find | DOM tree, DevTools, CSS selectors | `tests/test_01_css_selectors.py` |
| 01 Find | XPath: axes, `contains()`, `last()` | `tests/test_02_xpath.py` |
| 01 Find | An id that changes on every load | `tests/test_03_dynamic_ids.py` |
| 01 Find | Locator ladder: role, label, placeholder, text, alt, title, test id | `tests/test_04_user_facing_locators.py` |
| 01 Find | The accessibility tree | `tests/test_05_accessibility_tree.py` |
| 01 Find | Strict mode: one locator, three buttons | `tests/test_06_strict_mode.py` |
| 01 Find | Chaining and `filter()` | `tests/test_07_chaining_and_filter.py` |
| 02 Act | Every gesture has its own method | `tests/test_08_actions.py` |
| 02 Act | Dialogs and new tabs | `tests/test_09_dialogs_and_tabs.py` |
| 03 Check | `expect()` assertions | `tests/test_10_assertions.py` |
| 03 Check | Auto-waiting, assert vs expect | `tests/test_11_auto_waiting.py` |
| 04 Data | Boundaries, equivalence classes, `parametrize` | `tests/test_12_parametrize.py` |
| 05 Organize | Fixtures: `page`, `context`, `logged_in` | `tests/test_13_fixtures.py` + `conftest.py` |
| 05 Organize | Every test brings its own data | `tests/test_14_independence.py` + `conftest.py` |
| 05 Debug | Trace and bug report | `tests/test_15_debug_trace.py` |

## Run only what you need

```bash
uv run pytest tests/test_06_strict_mode.py -v     # one file
uv run pytest -k "strict or dialog" -v            # names that contain these words
uv run pytest -k "bad user" -v                    # one parametrize case by its id
uv run pytest -m smoke -v                         # tests marked @pytest.mark.smoke
uv run pytest -m "not slow"                       # skip the ~5 s waiting tests
uv run pytest --lf                                # only the tests that failed last time
uv run pytest -x                                  # stop at the first failure
uv run pytest -s tests/test_05_accessibility_tree.py   # show print() output
```

Markers are listed in `pyproject.toml`. A marker that is not listed there gives a warning.

## Watch and debug

```bash
uv run pytest tests/test_08_actions.py --headed --slowmo 500    # watch the browser
uv run pytest --browser firefox                                  # another browser (install it first)

# The trace demo: this test fails ON PURPOSE (it is hidden from a normal run)
uv run pytest -m broken --tracing retain-on-failure
uv run playwright show-trace test-results/<test folder>/trace.zip

uv run pytest -m broken --screenshot only-on-failure --video retain-on-failure
uv run playwright codegen https://the-internet.herokuapp.com/login   # record clicks as code
```

PowerShell, step by step with the Playwright Inspector:

```powershell
$env:PWDEBUG=1; uv run pytest -m broken; Remove-Item Env:PWDEBUG
```

## Expected result

`uv run pytest` runs all tests except the `broken` one.
One test is shown as **XFAIL** (`test_assert_looks_once`). That is correct:
it shows that a plain `assert` checks the page once and fails, while `expect()` waits.

## If a test is red

- **the-internet.herokuapp.com** sometimes shows "Application Error" for a minute. Run again with `uv run pytest --lf`.
- **demoqa.com** is slow because of its ads. `conftest.py` blocks the ad servers (`block_ads` fixture).
- Read the error from top to bottom: which test, what was expected, what was actually there, which locator. Then open the trace.
