# Lecture 6 · Trace Viewer and codegen — step by step

Two commands, two jobs:

| Command | What it does |
|---|---|
| `uv run playwright show-trace test-results/<test-name>/trace.zip` | Opens a **recording of a test that already ran**. You see every step, a screenshot, the DOM, the network, the console. |
| `uv run playwright codegen --target python-pytest https://www.saucedemo.com` | **Records you** clicking on a site and writes a **pytest test** for it. |

> Trace Viewer = look **back** at a test.
> codegen = write a **new** test.

All commands are for PowerShell, run from the project folder
(`D:\IdeaProjects\lecture-3-playwright`).

---

## Part A · `show-trace` — watch a test after it ran

A trace is a `trace.zip` file. pytest writes it only when you ask with `--tracing`.

### Step 1 · Run a test with tracing on

```powershell
uv run pytest tests/lecture_6/test_07_cookies.py --tracing on
```

`--tracing` has three values:

| Value | When is `trace.zip` saved? |
|---|---|
| `on` | for **every** test |
| `retain-on-failure` | only for tests that **failed** (best for everyday use) |
| `off` | never (default) |

### Step 2 · Find the trace file

pytest makes a folder `test-results/`, with one sub-folder per test:

```powershell
ls test-results
```

```text
tests-lecture-6-test-07-cookies-py-test-login-creates-a-cookie-chromium
tests-lecture-6-test-07-cookies-py-test-login-with-cookie-chromium
tests-lecture-6-test-07-cookies-py-test-no-cookie-no-inventory-chromium
```

The folder name is built from the test like this:

```text
tests/lecture_6/test_07_cookies.py :: test_login_with_cookie   [chromium]
  ↓   (every / _ . becomes -)
tests-lecture-6-test-07-cookies-py-test-login-with-cookie-chromium
```

Inside each folder there is one file: `trace.zip`.

### Step 3 · Open the trace

Put the folder name in place of `<test-name>`:

```powershell
uv run playwright show-trace test-results/tests-lecture-6-test-07-cookies-py-test-login-with-cookie-chromium/trace.zip
```

Tip: type `test-results/tests-lecture-6-test-07` and press **Tab** — PowerShell
fills in the rest of the name.

### Step 4 · Read the Trace Viewer window

```text
┌───────────────┬───────────────────────────────────────────────┐
│  Actions      │  Screenshot of the page at the chosen step    │
│  (left list)  │  (Before / Action / After tabs)               │
│               │                                               │
│ goto          │                                               │
│ add_cookies   │                                               │
│ expect ...    ├───────────────────────────────────────────────┤
│               │ Call · Log · Errors · Console · Network ·     │
│               │ Source · Attachments                          │
└───────────────┴───────────────────────────────────────────────┘
        Timeline with small screenshots along the top
```

1. Click a step in the **Actions** list on the left.
2. Look at the screenshot: **Before** = page before the step, **After** = page after it.
3. Open the tabs at the bottom:
   - **Call** — the locator, the arguments, how long the step took.
   - **Errors** — the error message (if the test failed).
   - **Console** — `console.log` messages from the page.
   - **Network** — every request and its status (200, 404, 500 ...).
   - **Source** — the line in your Python file that made this step.
4. The screenshot is a live DOM snapshot — you can right-click → **Inspect**
   like in normal DevTools.

### Step 5 · Use it for a failed test (the real use case)

```powershell
uv run pytest tests/lecture_6 --tracing retain-on-failure
ls test-results          # only folders for FAILED tests are here
uv run playwright show-trace test-results/<failed-test-folder>/trace.zip
```

Click the **red** step in the list → read **Errors** → look at the **Before**
screenshot. Most of the time you see the reason at once: wrong page, popup
on top, text is different, element not loaded yet.

### Other ways to open a trace

- Drag `trace.zip` onto https://trace.playwright.dev (works in the browser,
  the file stays on your computer).
- Run `uv run playwright show-trace` with **no** file and drop the zip into the window.

### Make a trace by hand (without `--tracing`)

See `test_trace_file_is_written` in `test_11_debugging.py`:

```python
context.tracing.start(screenshots=True, snapshots=True, sources=True)
# ... test steps ...
context.tracing.stop(path="trace.zip")
```

```powershell
uv run playwright show-trace trace.zip
```

---

## Part B · `codegen --target python-pytest` — record a new test

### Step 1 · Start the recorder

```powershell
uv run playwright codegen --target python-pytest https://www.saucedemo.com
```

Two windows open:

| Window | What you do |
|---|---|
| **Browser** | Use the site like a normal user. |
| **Playwright Inspector** | Watch the code appear. |

`--target python-pytest` means: write the code as a **pytest test function**
(with the `page` fixture). Without it you get a plain script with
`sync_playwright()` and `browser.launch()`.

### Step 2 · Do the steps in the browser

Example — log in and add a backpack to the cart:

1. Click **Username**, type `standard_user`
2. Click **Password**, type `secret_sauce`
3. Click **Login**
4. Click **Add to cart** under *Sauce Labs Backpack*
5. Click the cart icon

### Step 3 · Add a check (assert)

In the Inspector toolbar, click **Assert text** (or *Assert visibility*),
then click on the cart item name *Sauce Labs Backpack*.
codegen adds an `expect(...)` line.

### Step 4 · Look at the code

The Inspector now shows something like:

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
    page.locator("[data-test=\"shopping-cart-link\"]").click()
    expect(page.locator("[data-test=\"inventory-item-name\"]")).to_contain_text("Sauce Labs Backpack")
```

### Step 5 · Save it to a file

**Way 1 — copy:** click the **Copy** button in the Inspector, paste into a new
file, e.g. `tests/lecture_6/test_13_my_recording.py`.

**Way 2 — `-o` writes the file for you:**

```powershell
uv run playwright codegen --target python-pytest -o tests/lecture_6/test_13_my_recording.py https://www.saucedemo.com
```

The file is written when you close the browser.

> The file name **must start with `test_`**, otherwise pytest will not find it.

### Step 6 · Clean up the draft

codegen writes **steps**, you write the **test**:

1. Rename `test_example` → `test_add_backpack_to_cart`.
2. Remove extra `.click()` lines before `.fill()` — `fill` clicks by itself.
3. Remove `import re` if it is not used.
4. Check that the `expect(...)` really tests the goal of the test.

### Step 7 · Run it

```powershell
uv run pytest tests/lecture_6/test_13_my_recording.py
```

Green = done. Red = open the trace (Part A, step 5).

### Useful codegen options

```powershell
# other browser
uv run playwright codegen --target python-pytest -b firefox https://www.saucedemo.com

# window size
uv run playwright codegen --target python-pytest --viewport-size "1280,720" https://www.saucedemo.com

# phone
uv run playwright codegen --target python-pytest --device "iPhone 13" https://www.saucedemo.com

# language
uv run playwright codegen --target python-pytest --lang "en-US" https://www.saucedemo.com
```

---

## Cheat sheet

```powershell
# --- Trace ---
uv run pytest tests/lecture_6 --tracing retain-on-failure   # save trace for failed tests
uv run pytest tests/lecture_6 --tracing on                  # save trace for every test
ls test-results                                             # find the folder name
uv run playwright show-trace test-results/<test-name>/trace.zip

# --- codegen ---
uv run playwright codegen --target python-pytest https://www.saucedemo.com
uv run playwright codegen --target python-pytest -o tests/lecture_6/test_13_my_recording.py https://www.saucedemo.com
```

More detail on codegen: [CODEGEN.md](CODEGEN.md).
