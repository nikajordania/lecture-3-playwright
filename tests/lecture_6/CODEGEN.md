# Lecture 6 · codegen — a full guide for students

`codegen` is the Playwright **recorder**. You click on a website, and Playwright
writes the Python code for every click and every key you type.

> codegen writes the **steps**. You write the **test**.
> The recorded code is a first draft, not a finished test (part 9).

Docs: https://playwright.dev/python/docs/codegen

---

## Contents

1. [What happens when you run it](#1--what-happens-when-you-run-it)
2. [Before you start](#2--before-you-start)
3. [Your first recording](#3--your-first-recording-step-by-step)
4. [Save the code to a file](#4--save-the-code-to-a-file)
5. [Where to run it: terminal, PyCharm / IntelliJ IDEA, VS Code](#5--where-to-run-it)
6. [The toolbar: Record, Pick locator, Assert](#6--the-toolbar)
7. [Options: browser, size, device, language, login](#7--options)
8. [Record from your own code: `page.pause()`](#8--record-from-your-own-code-pagepause)
9. [From draft to test](#9--from-draft-to-test)
10. [Problems and fixes](#10--problems-and-fixes)
11. [Practice](#11--practice)
12. [Cheat sheet](#12--cheat-sheet)

---

## 1 · What happens when you run it

```powershell
uv run playwright codegen https://www.saucedemo.com
```

Two windows open:

| Window | What you do there |
|---|---|
| **Browser** (Chromium) | Use the site like a normal user: click, type, choose. |
| **Playwright Inspector** | Watch the code appear, line by line. Copy it. |

When you close the browser, recording stops.
The code is **not saved** unless you copy it or use `-o` (part 4).

---

## 2 · Before you start

You need the project and its packages. In the project folder:

```powershell
uv sync                          # installs pytest, pytest-playwright, playwright
uv run playwright install        # downloads chromium, firefox, webkit (once)
```

Check that it works:

```powershell
uv run playwright --version
```

**Classroom computers:** `uv` is not on PATH by default. Run this first in every
new terminal:

```powershell
$env:Path += ";C:\Users\student\AppData\Roaming\Python\Scripts"
```

> Why `uv run` in front? It runs `playwright` from the project's `.venv`.
> Then the codegen version is the same as the library version in your tests.

---

## 3 · Your first recording (step by step)

We record a login on SauceDemo and add one item to the cart.

1. Start codegen with the pytest target:

   ```powershell
   uv run playwright codegen --target python-pytest https://www.saucedemo.com
   ```

2. In the **browser**:
   - click **Username**, type `standard_user`
   - click **Password**, type `secret_sauce`
   - click **Login**
   - click **Add to cart** under *Sauce Labs Backpack*

3. Add a check: in the toolbar, choose **Assert text**, click the cart badge
   (the red `1`), confirm.

4. Look at the **Inspector**. You will see something like this:

   ```python
   import re
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

5. Press **Copy** in the Inspector, or close the browser if you used `-o`.

6. Run it:

   ```powershell
   uv run pytest tests/lecture_6/test_draft.py -v
   ```

---

## 4 · Save the code to a file

| Flag | What it does |
|---|---|
| `--target python-pytest` | pytest test: a `test_example(page)` function. **Use this one.** |
| `--target python` | a plain script with `sync_playwright()` (the default) |
| `--target python-async` | a script with `async` / `await` |
| `-o <file>` | writes the code to the file when you close the browser |

```powershell
uv run playwright codegen --target python-pytest -o tests/lecture_6/test_draft.py https://www.saucedemo.com
```

- The file name must start with `test_`, or pytest does not find it.
- `-o` **overwrites** the file. Use a new name for every recording.
- You can also change the language in the Inspector: the **Target** list at the top.

---

## 5 · Where to run it

codegen is a **command-line tool**. It is not a part of one editor.
Any terminal works, and every IDE has a terminal.

### 5.1 · Windows terminal (PowerShell)

```powershell
cd D:\IdeaProjects\lecture-3-playwright
uv run playwright codegen --target python-pytest https://www.saucedemo.com
```

### 5.2 · PyCharm / IntelliJ IDEA — the built-in terminal

1. Open the project.
2. Open the terminal: **View → Tool Windows → Terminal** (`Alt+F12`).
3. Run the same command as above.

The terminal opens in the project folder, so paths like `tests/lecture_6/...` work.

### 5.3 · PyCharm / IntelliJ IDEA — a Run Configuration (one click ▶)

Good when you record the same site many times.

1. **Run → Edit Configurations… → `+` → Python**
2. Change **Script path** to **Module name** and write: `playwright`
3. **Parameters:**
   `codegen --target python-pytest -o tests/lecture_6/test_draft.py https://www.saucedemo.com`
4. **Working directory:** the project folder (`D:\IdeaProjects\lecture-3-playwright`)
5. **Python interpreter:** the project's `.venv` (the uv environment)
6. Name it `codegen saucedemo`, press **OK**, then **▶ Run**.

This is the same as `python -m playwright codegen ...`.
In IntelliJ IDEA you need the **Python** plugin for this.

### 5.4 · VS Code

The Playwright extension for VS Code has **Record new** and **Record at cursor**
buttons, but they work with **Playwright Test for JavaScript / TypeScript**.
For Python, open the VS Code terminal (**View → Terminal**) and use the same
`uv run playwright codegen ...` command.

### Same command, any place

| Where | How |
|---|---|
| PowerShell | `uv run playwright codegen ...` |
| PyCharm / IDEA terminal | `uv run playwright codegen ...` |
| PyCharm / IDEA Run Config | module `playwright`, parameters `codegen ...` |
| VS Code terminal | `uv run playwright codegen ...` |
| No uv | `.venv\Scripts\activate`, then `playwright codegen ...` |

---

## 6 · The toolbar

The toolbar is at the top of the recording browser (and in the Inspector).

| Button | What it does | Code it writes |
|---|---|---|
| **Record** (red circle) | turns recording on / off | — |
| **Pick locator** | hover an element → see its locator, click → copy it | — (the locator only) |
| **Assert visibility** | click an element → check it is on the screen | `expect(...).to_be_visible()` |
| **Assert text** | click an element → check its text | `expect(...).to_contain_text("...")` |
| **Assert value** | click an input → check what is in it | `expect(...).to_have_value("...")` |

### Pick locator — useful even if you write tests by hand

1. Press **Record** to stop recording.
2. Press **Pick locator**.
3. Move the mouse over the page: every element shows its locator.
4. Click the element. The locator appears in the Inspector field.
5. Change it there if you want (the page shows what it matches), then copy it.

> codegen prefers **role, text and test id** locators — like the "locator ladder"
> from lecture 3. Only when it finds none of them does it fall back to CSS.

---

## 7 · Options

All flags: `uv run playwright codegen --help`

### 7.1 · Browser (lecture 6, part 02)

```powershell
uv run playwright codegen -b firefox https://demoqa.com
uv run playwright codegen -b webkit https://demoqa.com
uv run playwright codegen --channel chrome https://demoqa.com     # your real Google Chrome
uv run playwright codegen --channel msedge https://demoqa.com     # Microsoft Edge
```

### 7.2 · Window size and devices

```powershell
uv run playwright codegen --viewport-size "800,600" https://playwright.dev
uv run playwright codegen --device "iPhone 13" https://playwright.dev
uv run playwright codegen --device "Pixel 7" https://playwright.dev
```

`--device` sets the size, the user agent, touch and the pixel ratio together.
In a pytest test the same is: `uv run pytest --device "iPhone 13"`.

### 7.3 · The user's world: language, time, place, theme

```powershell
uv run playwright codegen --lang ka-GE --timezone Asia/Tbilisi `
    --geolocation "41.7151,44.8271" --color-scheme dark https://playwright.dev
```

| Flag | In a test (`browser.new_context(...)`) |
|---|---|
| `--lang ka-GE` | `locale="ka-GE"` |
| `--timezone Asia/Tbilisi` | `timezone_id="Asia/Tbilisi"` |
| `--geolocation "41.7151,44.8271"` | `geolocation={...}` + `permissions=["geolocation"]` |
| `--color-scheme dark` | `color_scheme="dark"` |
| `--user-agent "..."` | `user_agent="..."` |

### 7.4 · Test ids

SauceDemo uses `data-test`, but Playwright looks for `data-testid`.
Tell codegen the right name, and it writes `get_by_test_id(...)`:

```powershell
uv run playwright codegen --target python-pytest --test-id-attribute data-test https://www.saucedemo.com
```

```python
page.get_by_test_id("username").fill("standard_user")   # instead of locator("[data-test=\"username\"]")
```

In the test, set the same attribute (see `test_12_codegen.py`):

```python
playwright.selectors.set_test_id_attribute("data-test")
```

### 7.5 · Login once, record many times (lecture 6, part 04)

**Save** the login (cookies + localStorage) when you close the browser:

```powershell
uv run playwright codegen --save-storage auth.json https://www.saucedemo.com
# log in, then close the browser
```

**Load** it next time — you start already logged in:

```powershell
uv run playwright codegen --load-storage auth.json https://www.saucedemo.com/inventory.html
```

The same file works in tests:

```python
context = browser.new_context(storage_state="auth.json")
```

> ⚠️ `auth.json` is a **key to the account**. Never commit it.
> Add it to `.gitignore`:
> ```
> auth.json
> ```

### 7.6 · More flags

| Flag | Use |
|---|---|
| `--http-credentials "admin:admin"` | the browser sign-in window (Basic auth, lecture 5). The password goes into the code! |
| `--ignore-https-errors` | test sites with a bad certificate |
| `--save-har network.har` | saves all network traffic (DevTools → Network) to a file |
| `--timeout 10000` | action timeout in ms |
| `--user-data-dir C:\pw-profile` | a real browser profile that keeps everything. Use a **new, empty** folder: Chrome 136+ blocks the default profile. |

---

## 8 · Record from your own code: `page.pause()`

codegen flags cannot do everything. For example, they cannot block pictures
with `route()`. Then write the setup yourself and call `page.pause()`.

### 8.1 · From a script — `codegen_custom_setup.py`

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)       # you must see the window
    context = browser.new_context(locale="ka-GE")     # any context options
    context.route("**/*.jpg", lambda route: route.abort())   # no pictures
    page = context.new_page()
    page.goto("https://demoqa.com/books")
    page.pause()                                      # the Inspector opens here
    browser.close()
```

```powershell
uv run python tests/lecture_6/codegen_custom_setup.py
```

In the Inspector press **Record** and click on the page. The code appears.

> The file has no `test_` prefix on purpose: pytest does not collect it.

### 8.2 · Inside a pytest test

```python
def test_something(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.locator("#user-name").fill("standard_user")
    page.pause()          # stops here: Step over, Resume, Record, Pick locator
    ...
```

In this project the demo test is skipped unless you switch it on:

```powershell
$env:LECTURE6_PAUSE=1; uv run pytest tests/lecture_6/test_11_debugging.py -k pause --headed
Remove-Item Env:LECTURE6_PAUSE   # turn it off again
```

### 8.3 · Inspector from the first line: `PWDEBUG`

```powershell
$env:PWDEBUG=1; uv run pytest tests/lecture_6/test_07_cookies.py
Remove-Item Env:PWDEBUG          # turn it off again
```

---

## 9 · From draft to test

codegen records **what you did**, not **what you wanted to check**.
After recording, clean up the draft:

| Draft from codegen | Real test |
|---|---|
| name `test_example` | a name that says what is checked: `test_backpack_in_cart` |
| `click()` before every `fill()` | delete the `click()`, `fill()` is enough |
| login steps inside every test | a fixture (`logged_in_page` in `conftest.py`) or `storage_state` |
| `locator("[data-test=\"x\"]")` | `get_by_test_id("x")` or `get_by_role(...)` |
| no checks, or a weak `to_contain_text` | strong `expect(...)` checks: `to_have_text`, `to_have_url`, `to_be_visible` |
| text and URLs inside the code | constants or `@pytest.mark.parametrize` |
| extra steps (you clicked by mistake) | delete them |
| `page.wait_for_timeout(...)` | delete — `expect` waits by itself |

**Before** (codegen):

```python
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

**After** (you):

```python
def test_backpack_in_cart(data_test_ids, logged_in_page: Page):
    page = logged_in_page                                  # login → fixture
    page.get_by_test_id("add-to-cart-sauce-labs-backpack").click()
    expect(page.get_by_test_id("shopping-cart-badge")).to_have_text("1")
    expect(page.get_by_test_id("remove-sauce-labs-backpack")).to_be_visible()
```

Full example: `test_12_codegen.py`.

### When codegen is a good idea — and when not

| ✅ Good | ❌ Not good |
|---|---|
| a new site: "what are the locators here?" | a finished, clean test suite |
| a long form with many fields | checks — you must think about them yourself |
| Pick locator for one hard element | dynamic data (ids that change, dates) |
| showing a bug: "these are my steps" | copying the draft to the repo without cleanup |

---

## 10 · Problems and fixes

| Problem | Fix |
|---|---|
| `uv` is not recognized | classroom PATH line from part 2 |
| `Executable doesn't exist ...` | `uv run playwright install` (or `install firefox`) |
| the file from `-o` is empty or missing | nothing was recorded, or you stopped with `Ctrl+C` — finish by closing the browser window |
| pytest does not find the test | the file name must start with `test_` |
| the test passes in codegen, fails in pytest | different window size / language: check `conftest.py` → `browser_context_args` |
| codegen writes `nth(0)` or long CSS | the element has no good name: use Pick locator and write a better locator |
| ads cover buttons (demoqa) | in tests, the `block_ads` fixture; in codegen, use `page.pause()` with `route()` |
| `--user-data-dir` does not open your Chrome profile | Chrome 136+ blocks it — use a new empty folder |
| the code has `.click()` on an input and then `.fill()` | normal for codegen — delete the `click()` |

---

## 11 · Practice

1. **First draft.** Record a login on `https://www.saucedemo.com` with
   `--target python-pytest -o tests/lecture_6/test_my_login.py`.
   Add one **Assert text** for the page title *Products*. Run it with pytest.

2. **Clean it up.** Use the table in part 9: a good name, no extra `click()`,
   `get_by_test_id`, strong checks. Run it again.

3. **Pick locator.** Open `https://demoqa.com/automation-practice-form`.
   With **Pick locator**, find locators for *First Name*, *Gender → Male*,
   and *Submit*. Write them in a test by hand.

4. **Phone.** Record the same SauceDemo login with `--device "iPhone 13"`.
   Is the code different? Why or why not?

5. **Login once.** Save the login with `--save-storage auth.json`, then open
   `/inventory.html` with `--load-storage auth.json`.
   Did you see the login page? Add `auth.json` to `.gitignore`.

---

## 12 · Cheat sheet

```powershell
# record
uv run playwright codegen https://www.saucedemo.com

# record a pytest test into a file
uv run playwright codegen --target python-pytest -o tests/lecture_6/test_draft.py https://www.saucedemo.com

# use data-test ids
uv run playwright codegen --target python-pytest --test-id-attribute data-test https://www.saucedemo.com

# browsers
uv run playwright codegen -b firefox https://demoqa.com
uv run playwright codegen --channel chrome https://demoqa.com

# size and devices
uv run playwright codegen --viewport-size "800,600" https://playwright.dev
uv run playwright codegen --device "iPhone 13" https://playwright.dev

# language, time, place, theme
uv run playwright codegen --lang ka-GE --timezone Asia/Tbilisi --geolocation "41.7151,44.8271" --color-scheme dark https://playwright.dev

# login once
uv run playwright codegen --save-storage auth.json https://www.saucedemo.com
uv run playwright codegen --load-storage auth.json https://www.saucedemo.com/inventory.html

# your own setup + page.pause()
uv run python tests/lecture_6/codegen_custom_setup.py

# Inspector from the first line of a test
$env:PWDEBUG=1; uv run pytest tests/lecture_6/test_07_cookies.py

# all flags
uv run playwright codegen --help
```

## Docs (switch the language to Python)

- Test generator — https://playwright.dev/python/docs/codegen
- Locators — https://playwright.dev/python/docs/locators
- Debugging, Inspector — https://playwright.dev/python/docs/debug
- Authentication, storage state — https://playwright.dev/python/docs/auth
- Emulation (devices, locale, geolocation) — https://playwright.dev/python/docs/emulation
