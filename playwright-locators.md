# Playwright (Python): Locators Explained

Playwright recommends choosing a locator based on **how the user perceives the page**, not on how the page is built (HTML structure, CSS classes).

> **Rule of thumb:** what a user sees rarely changes. Paths and classes change with every redesign.

---

## 0. Project setup

### Using pip

```bash
# 1. Create the virtual environment
python -m venv .venv

# 2. Activate it
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows (cmd / PowerShell)

# 3. Install dependencies
python -m pip install --upgrade pip
pip install pytest pytest-playwright

# 4. Download browsers
playwright install                       # all browsers
playwright install --with-deps chromium  # only Chromium + system deps (Linux / CI)

# 5. Freeze dependencies
pip freeze > requirements.txt
```

On another machine: `pip install -r requirements.txt`, then `playwright install`.

### Using uv

**Option A — like pip, but faster**

```bash
uv venv                          # creates .venv
source .venv/bin/activate        # or .venv\Scripts\activate on Windows
uv pip install pytest pytest-playwright
playwright install chromium
```

**Option B — project-based (recommended)**

```bash
uv init                                  # creates pyproject.toml
uv add --dev pytest pytest-playwright    # adds dev dependencies, creates .venv
uv run playwright install chromium
uv run pytest
```

No need to activate `.venv`: `uv run` uses it automatically. Versions are locked in `uv.lock`. On another machine: `uv sync`, then `uv run playwright install`.

### Smoke test

`pytest-playwright` already includes `playwright`, so you don't install it separately.

```python
# test_example.py
def test_title(page):
    page.goto("https://playwright.dev")
    assert "Playwright" in page.title()
```

```bash
pytest --headed --browser chromium           # pip
uv run pytest --headed --browser chromium    # uv
```

The `page` fixture is provided automatically by the `pytest-playwright` plugin.

---

## 1. Summary table

Ordered from **most preferred** to **most fragile**.

| # | Locator | What it finds | Example | Stability | When to use |
|---|---|---|---|---|---|
| 1 | `get_by_role()` | ARIA role + accessible name | `page.get_by_role("button", name="Login")` | ⭐⭐⭐⭐⭐ | Default choice for anything interactive: buttons, links, checkboxes, headings, tables |
| 2 | `get_by_label()` | Field by its `<label>` text or `aria-label` | `page.get_by_label("Username")` | ⭐⭐⭐⭐⭐ | Form fields |
| 3 | `get_by_placeholder()` | `placeholder` attribute | `page.get_by_placeholder("Enter email")` | ⭐⭐⭐⭐ | Field without a `<label>` |
| 4 | `get_by_text()` | Visible text | `page.get_by_text("Hovers")` | ⭐⭐⭐⭐ | Non-interactive elements: paragraphs, divs, spans |
| 5 | `get_by_alt_text()` | `alt` attribute | `page.get_by_alt_text("logo")` | ⭐⭐⭐⭐ | Images, `<area>` |
| 6 | `get_by_title()` | `title` attribute | `page.get_by_title("Close")` | ⭐⭐⭐ | Icons with a tooltip |
| 7 | `get_by_test_id()` | `data-testid` attribute | `page.get_by_test_id("submit-btn")` | ⭐⭐⭐⭐⭐ (technically) | No role and no text, or the text changes (localization) |
| 8 | `locator("css")` | CSS selector | `page.locator("#username")` | ⭐⭐⭐ (id) / ⭐ (classes) | Stable `id`, legacy app |
| 9 | `locator("xpath")` | XPath | `page.locator("//form/button")` | ⭐ | Only when nothing else works |

---

## 2. Each locator in detail

### `get_by_role` — the main tool

Searches the **accessibility tree**, the same way a screen reader does.

```python
page.get_by_role("button", name="Login")
page.get_by_role("link", name="Hovers")
page.get_by_role("checkbox", name="Remember me").check()
page.get_by_role("heading", name="Login Page", level=2)
page.get_by_role("textbox", name="Username")      # same as get_by_label
```

- By default, `name` matches a **substring, case-insensitive**. Use `exact=True` for an exact match, or pass a regular expression.
- It also checks accessibility: if the test can't find a button by role, it may be an a11y bug.
- Downside: if the markup is built from `div`s without ARIA, there is no role (see section 6).

### `get_by_label`

Works with `<label for="...">`, with an `<input>` nested inside a `<label>`, and with `aria-label` / `aria-labelledby`.

```python
page.get_by_label("Username").fill("tomsmith")
```

### `get_by_placeholder`

The placeholder disappears when the user types, and designers often change it. So it is weaker than a label.

```python
page.get_by_placeholder("Enter email").fill("a@b.com")
```

### `get_by_text`

```python
import re

page.get_by_text("Hovers")               # substring, case-insensitive
page.get_by_text("Hovers", exact=True)   # exact match
page.get_by_text(re.compile(r"^Hover"))  # regex
```

- Whitespace is normalized.
- For buttons and links, prefer `get_by_role`: the same text can appear anywhere on the page.
- Breaks with localization and copywriting changes.

### `get_by_alt_text` / `get_by_title`

```python
page.get_by_alt_text("logo")
page.get_by_title("Close")
```

### `get_by_test_id` — an agreement with developers

```python
# if your project uses a different attribute name:
playwright.selectors.set_test_id_attribute("data-qa")

page.get_by_test_id("login-submit")
```

- **Pro:** does not depend on text or layout.
- **Con:** the user does not see it, so the test does not check what a real person sees. It also requires changes in the application code.

### `locator()` with CSS

```python
page.locator("#username")              # id: OK if stable
page.locator("[name='password']")      # attribute: acceptable
page.locator(".btn.btn-primary.mt-3")  # classes: break on redesign
```

Generated ids like `#input-4f8a2c` are unreliable.

### `locator()` with XPath

```python
page.locator("/html/body/div[2]/form/button")   # absolute: breaks first
page.locator("//button[text()='Login']")        # relative: a bit better
```

Playwright detects XPath automatically when the string starts with `//` or `..`. An absolute path depends on every `div` above the element.

---

## 3. Narrowing down: chaining and filters

Often one locator is not unique. Narrow it down instead of switching to XPath:

```python
# chaining: search inside a container
page.get_by_role("form").get_by_role("button", name="Login")

# filter by text or by a nested element
page.get_by_role("listitem").filter(has_text="Product 2")
page.get_by_role("listitem").filter(
    has=page.get_by_role("heading", name="Product 2")
).get_by_role("button", name="Add")

# exclusion
page.get_by_role("listitem").filter(has_not_text="Out of stock")

# logic
page.get_by_role("button", name="New").or_(page.get_by_text("Create"))
page.get_by_role("button").and_(page.get_by_title("Subscribe"))

# by position: last resort
page.get_by_role("row").nth(2)
page.get_by_role("row").first
page.get_by_role("row").last

# iframe
page.frame_locator("#editor").get_by_role("textbox")
```

---

## 4. Common behavior of all locators

- **Lazy.** A locator does not search for the element when it is created. It searches only when you act on it (`click`, `fill`, `expect`).
- **Auto-wait.** Before an action, it waits until the element is visible, stable, and enabled.
- **Strictness.** If a locator matches more than one element, the action fails with an error. This protects you from clicking the wrong element. Use `.first` deliberately, not to silence the error.

---

## 5. How to choose

```
Interactive element?      → get_by_role
Form field?               → get_by_label → get_by_placeholder
Plain text / image?       → get_by_text / get_by_alt_text
Nothing fits?             → ask devs for data-testid → get_by_test_id
No access to the code?    → CSS by stable id / attribute
Nothing at all?           → relative XPath (absolute — never)
```

To see which locator Playwright itself suggests:

```bash
playwright codegen https://the-internet.herokuapp.com/login
```

The **"Pick locator"** button shows the recommended locator for any element.

---

## 6. Deep dive: why `get_by_role` fails on `div`-based markup

### Where roles come from

Every element has a **role in the accessibility tree**. The browser builds this tree alongside the DOM. Screen readers and `get_by_role` both use it. There are two kinds of roles.

**Implicit** — given by semantic tags:

| Tag | Role |
|---|---|
| `<button>`, `<input type="submit">` | `button` |
| `<a href="...">` | `link` |
| `<input type="text">` | `textbox` |
| `<input type="checkbox">` | `checkbox` |
| `<select>` | `combobox` |
| `<h1>`…`<h6>` | `heading` |
| `<ul>/<ol>`, `<li>` | `list`, `listitem` |
| `<table>`, `<tr>`, `<td>` | `table`, `row`, `cell` |
| `<nav>`, `<main>`, `<form>`* | `navigation`, `main`, `form` |

\* `<form>` gets the `form` role only if it has an accessible name (`aria-label`, etc.).

**Explicit** — set with the `role="..."` attribute.

`<div>` and `<span>` have the role **`generic`**, which basically means no role. You cannot find them with `get_by_role("button")`, even if they look and behave like a button.

### What it looks like in practice

```html
<!-- 1. A real button -->
<button>Login</button>

<!-- 2. A "button" made of a div: looks the same, clicks the same -->
<div class="btn btn-primary" onclick="login()">Login</div>
```

```python
page.get_by_role("button", name="Login")   # finds only #1
page.get_by_text("Login")                  # finds both
```

A mouse user sees no difference. A screen reader user hears just "Login" for #2, without "button". A keyboard user (Tab → Enter) cannot reach it at all.

### Typical problem areas

**1. Clickable divs / spans**

```html
<div class="menu-item" onclick="...">Settings</div>
<span class="link" onclick="go()">Read more</span>
```

**2. Custom components** (dropdowns, tabs, modals, toggles) from UI libraries or hand-made:

```html
<div class="dropdown">
  <div class="dropdown-selected">Choose city</div>
  <div class="dropdown-options">
    <div class="option">Tbilisi</div>
    <div class="option">Batumi</div>
  </div>
</div>
```

There is nothing here for `get_by_role("combobox")` / `get_by_role("option")`.

**3. Role exists, but no name.** Common with icon buttons:

```html
<button><svg>...</svg></button>                       <!-- role button, empty name -->
<button aria-label="Close"><svg>...</svg></button>    <!-- name "Close" -->
```

```python
page.get_by_role("button", name="Close")  # finds only the second one
```

The first one can only be found with `get_by_role("button")` + `.nth()`, which is fragile.

**4. Field without a label**

```html
<input type="text" placeholder="Username">
```

The `textbox` role exists, but the name comes from the placeholder only as a fallback. `get_by_label("Username")` will not find it, while `get_by_role("textbox", name="Username")` will. The behavior depends on what exactly is set.

### How to check whether a role exists

**1. Codegen / Pick locator.** If Playwright suggests `get_by_text` or `locator(".class")` instead of `get_by_role`, the role or the name is missing.

**2. Chrome DevTools** → Elements → **Accessibility** tab. It shows the `Role` and `Name` of the selected element. If it says `generic` and the name is empty, `get_by_role` will not help.

**3. ARIA snapshot from a test:**

```python
print(page.locator("form").aria_snapshot())
```

```yaml
- form:
  - textbox "Username"
  - textbox "Password"
  - button "Login"
```

Anything missing from the snapshot cannot be found with `get_by_role`.

### What to do

**Best solution: fix the markup.** This is not a request to "make it easier for tests". It is a real accessibility defect.

```html
<!-- best: a semantic tag -->
<button class="btn btn-primary">Login</button>

<!-- if the tag can't be changed: role + tabindex + keyboard handling -->
<div role="button" tabindex="0" onclick="login()" onkeydown="...">Login</div>

<!-- icon button -->
<button aria-label="Close"><svg>...</svg></button>
```

`role="button"` on a div gives only the role. Keyboard focus (`tabindex`) and Enter/Space handling must be implemented by the developer. That's why `<button>` is always better.

**If you can't change the markup**, go down the priority list:

```python
page.get_by_text("Login", exact=True)                   # visible text
page.get_by_test_id("login-btn")                        # if data-testid was added
page.locator(".dropdown").get_by_text("Tbilisi")        # narrow by container
page.locator("div.option").filter(has_text="Batumi")    # CSS + filter
```

### A useful side effect

If `get_by_role` can't find an element that the user can see, the test has effectively found an accessibility bug. That's why many teams write tests on roles on purpose: they check functionality and a11y at the same time. For full accessibility checks there is a separate tool: `axe-playwright-python`.
