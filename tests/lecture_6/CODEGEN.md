# Lecture 6 · codegen — record a new test

`codegen` is the Playwright **recorder**. You click on a site,
Playwright writes the Python code.

> codegen writes the **steps**. You write the **test**.
> A test failed and you want to know why? See [TRACE.md](TRACE.md).

Run all commands in PowerShell, in the project folder
`D:\IdeaProjects\lecture-3-playwright`.
The terminal in PyCharm / IntelliJ IDEA (`Alt+F12`) or VS Code works the same way.

---

## 1 · Start the recorder

```powershell
uv run playwright codegen --target python-pytest -o tests/lecture_6/test_my_recording.py https://www.saucedemo.com
```

| Part | Meaning |
|---|---|
| `--target python-pytest` | write a **pytest test** |
| `-o tests/lecture_6/test_my_recording.py` | save it to this file (the name must start with `test_`) |
| `https://www.saucedemo.com` | the site to open |

Two windows open: the **browser** (you click here) and the
**Inspector** (the code appears here).

## 2 · Do the steps in the browser

1. **Username** → type `standard_user`
2. **Password** → type `secret_sauce`
3. Click **Login**
4. Click **Add to cart** under *Sauce Labs Backpack*

## 3 · Add a check

In the toolbar at the top of the page, click **Assert text**,
then click the red cart badge `1`.
codegen adds an `expect(...)` line.

| Button | Checks |
|---|---|
| **Assert visibility** | the element is on the screen |
| **Assert text** | the element has this text |
| **Assert value** | the input has this value |

## 4 · Close the browser

The file is saved now. It looks like this:

```python
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://www.saucedemo.com/")
    page.locator("[data-test=\"username\"]").click()
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"password\"]").click()
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.locator("[data-test=\"login-button\"]").click()
    page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    expect(page.locator("[data-test=\"shopping-cart-badge\"]")).to_contain_text("1")
```

## 5 · Clean up the draft

1. Give the test a real name: `test_example` → `test_add_backpack_to_cart`
2. Delete every `.click()` right before a `.fill()` — `fill` clicks by itself.
3. Delete steps you did by mistake.
4. Check that `expect(...)` tests the **goal** of the test.

```python
def test_add_backpack_to_cart(page: Page) -> None:
    page.goto("https://www.saucedemo.com/")
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.locator("[data-test=\"login-button\"]").click()
    page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    expect(page.locator("[data-test=\"shopping-cart-badge\"]")).to_have_text("1")
```

A fuller cleanup (fixture for the login, `get_by_test_id`): `test_12_codegen.py`.

## 6 · Run it

```powershell
uv run pytest tests/lecture_6/test_my_recording.py
```

Green = done. Red = open the trace ([TRACE.md](TRACE.md)).

---

## Only need one locator? Pick locator

1. In the toolbar, press **Record** to stop recording.
2. Press **Pick locator** and move the mouse over the page.
3. Click the element → its locator appears in the Inspector → copy it.

## Useful options

Add them to the command from step 1:

| Option | What it does |
|---|---|
| `-b firefox` / `-b webkit` | another browser |
| `--viewport-size "800,600"` | window size |
| `--device "iPhone 13"` | a phone |
| `--lang ka-GE` | site language |
| `--save-storage auth.json` | save the login when you close the browser |
| `--load-storage auth.json` | start already logged in |

> `auth.json` is a key to the account — never commit it to git.

All options: `uv run playwright codegen --help`

## Your own setup: `page.pause()`

Need something the options cannot do (for example, block pictures)?
Write the setup in Python and put `page.pause()` where recording should start.
Example: `codegen_custom_setup.py`.

```powershell
uv run python tests/lecture_6/codegen_custom_setup.py
```

In the Inspector press **Record** and click on the page.

---

## Problems

| Problem | Fix |
|---|---|
| `uv` is not recognized (classroom) | `$env:Path += ";C:\Users\student\AppData\Roaming\Python\Scripts"` |
| `Executable doesn't exist` | `uv run playwright install` |
| pytest does not find the test | the file name must start with `test_` |
| the file is empty | finish by closing the **browser**, not with `Ctrl+C` |

Docs: https://playwright.dev/python/docs/codegen
