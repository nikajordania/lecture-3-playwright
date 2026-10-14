# Waits: Selenium → Playwright

```bash
uv run pytest tests/waits -v
```

## Three Selenium wait types, adapted

| Selenium | What it does | Playwright | File |
|---|---|---|---|
| **Implicit Wait**<br>`driver.implicitly_wait(10)` | every `find_element` waits up to 10 s, then `NoSuchElementException` | no implicit wait needed: every action waits by itself (30 s), every `expect()` retries (5 s).<br>Change the defaults with `page.set_default_timeout()`, `page.set_default_navigation_timeout()`, `expect.set_options(timeout=...)` | `test_01_implicit_wait.py` |
| **Explicit Wait**<br>`WebDriverWait(driver, 10).until(EC...)` | waits for one condition on one element | `expect(locator).to_be_visible(timeout=10_000)`<br>`locator.wait_for(state="visible" / "hidden" / "attached" / "detached")`<br>`page.wait_for_url()`, `page.wait_for_load_state()`, `page.expect_response()` | `test_02_explicit_wait.py` |
| **Fluent Wait**<br>timeout + polling + ignoring | checks every N ms, ignores "not found yet" errors | `expect()` already polls and ignores "not found".<br>`page.wait_for_function(js, polling=500)`<br>own loop: `fluent_wait()` in the test file | `test_03_fluent_wait.py` |
| `time.sleep(5)` | always waits 5 s | `page.wait_for_timeout(5000)` exists, but **do not use it** in tests | — |

## Implicit vs explicit — the Playwright version

| Selenium | Playwright |
|---|---|
| Implicit wait is for all elements of the driver | Default timeouts are per page (`page.set_default_timeout`) or for the whole run (`expect.set_options`) |
| Explicit wait needs an `ExpectedCondition` | `expect()` *is* the condition: `to_be_visible()`, `to_have_text()`... |
| Implicit is for elements that load fast, explicit for slow ones and for properties (visible, clickable, selected) | Actions wait for *actionability* by themselves: attached → visible → stable → enabled → receives events. Add `timeout=` only for slow things |
| Implicit 30 s + explicit 10 s can add up to **40 s** | **Nothing adds up**: one call has one timeout. `timeout=` on the call wins, otherwise the default |

## expected_conditions → Playwright

All of these are in `test_04_expected_conditions.py`.

| Selenium `EC.` | Playwright |
|---|---|
| `alert_is_present` | `page.once("dialog", handler)` before the click |
| `all_of` | several `expect()` lines |
| `any_of` | `expect(a.or_(b)).to_be_visible()` |
| `none_of` | several `expect(...).not_to_...()` lines |
| `element_attribute_to_include` | `expect(loc).to_have_attribute("type", "password")` |
| `element_to_be_clickable` | `expect(loc).to_be_enabled()` — or just `loc.click()`, it waits |
| `element_to_be_selected`, `element_located_to_be_selected` | `expect(loc).to_be_checked()` |
| `element_selection_state_to_be`, `element_located_selection_state_to_be` | `expect(loc).to_be_checked(checked=False)` |
| `frame_to_be_available_and_switch_to_it` | `page.frame_locator("#frame1").locator(...)` — no switching |
| `invisibility_of_element`, `invisibility_of_element_located` | `expect(loc).to_be_hidden()` / `loc.wait_for(state="hidden")` |
| `new_window_is_opened`, `number_of_windows_to_be` | `with page.context.expect_page() as info:` / `len(page.context.pages)` |
| `presence_of_element_located` | `expect(loc).to_be_attached()` / `loc.wait_for(state="attached")` |
| `presence_of_all_elements_located` | `expect(loc).to_have_count(n)` |
| `staleness_of` | `expect(loc).to_have_count(0)` / `loc.wait_for(state="detached")` — a locator is never stale |
| `text_to_be_present_in_element` | `expect(loc).to_contain_text("...")` |
| `text_to_be_present_in_element_attribute` | `expect(loc).to_have_attribute("href", re.compile("users"))` |
| `text_to_be_present_in_element_value` | `expect(loc).to_have_value(re.compile("tom"))` |
| `title_is`, `title_contains` | `expect(page).to_have_title("...")` / `to_have_title(re.compile("..."))` |
| `url_to_be`, `url_contains`, `url_matches`, `url_changes` | `expect(page).to_have_url(...)`, `not_to_have_url(old)`, `page.wait_for_url("**/login")` |
| `visibility_of`, `visibility_of_element_located` | `expect(loc).to_be_visible()` |
| `visibility_of_all_elements_located` | `for el in loc.all(): expect(el).to_be_visible()` |
| `visibility_of_any_elements_located` | `expect(loc.filter(visible=True)).not_to_have_count(0)` |
