# Lecture 4 · Playwright in Action — examples

Every example from the lecture 4 slides. Run them:

```bash
uv run pytest tests/lecture_4 -v                    # all of them
uv run pytest tests/lecture_4/test_07_dialogs.py    # one file
uv run pytest tests/lecture_4 -k "tab or window"    # by name
```

## Slide → file

| Slides | File |
|---|---|
| 01 Fill a form (picture + code) | `test_01_fill_form.py` |
| 02 Checkboxes | `test_02_checkboxes.py` |
| 03 Dropdown | `test_03_dropdown.py` |
| 04 Hover | `test_04_hover.py` |
| 05 Drag and drop | `test_05_drag_and_drop.py` |
| 06 Upload a file | `test_06_upload.py` |
| 07 Alerts | `test_07_dialogs.py` |
| 08 Back, forward, refresh | `test_08_back_forward_reload.py` |
| 09 New tab | `test_09_new_tab.py` |
| 10 New window | `test_10_new_window.py` |
| 11 Screenshots | `test_11_screenshots.py` |
| Part 2 · Locators as objects | `test_12_locator_objects.py` |
| Part 3 · expect combinations | `test_13_expect_knobs.py` |
| Part 4 · Classes and Page Objects | `test_14_page_objects.py`, `pages/`, `conftest.py` |

## Page classes

```
pages/
  base_page.py      BasePage: page, URL, open(), title()
  login_page.py     LoginPage(BasePage): username, password, submit, flash, login()
  secure_page.py    SecurePage(BasePage): heading, flash, logout()
  text_box_page.py  TextBoxPage: the demoqa form as a class
conftest.py         fixtures login_page and secure_page
```

## Reports (part 5)

```bash
uv run pytest tests/lecture_4 -v -rA                             # names + summary at the end
uv run pytest tests/lecture_4 --junitxml=report.xml              # JUnit XML for other tools
uv run pytest tests/lecture_4 --html=report.html --self-contained-html   # pytest-html: open in a browser
uv run pytest tests/lecture_4 --screenshot only-on-failure --tracing retain-on-failure
```

`pytest-html` is already in `pyproject.toml`. After pulling the project run `uv sync` once.
Do not commit `report.html`, `report.xml` or `test-results/`.
