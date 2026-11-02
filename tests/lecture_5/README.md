# Lecture 5 · Tricky UI — examples

Every example from the lecture 5 slides. Run them:

```bash
uv run pytest tests/lecture_5 -v                          # all of them
uv run pytest tests/lecture_5/test_03_basic_auth.py       # one file
uv run pytest tests/lecture_5 -k "frame or shadow"        # by name
uv run pytest tests/lecture_5 --device "iPhone 13"        # everything as a phone
uv run pytest tests/lecture_5 --html=report.html --self-contained-html
```

The tests use live practice sites. If a site is slow or shows
"Application Error", run the failed tests again: `uv run pytest --lf`.

## Slide → file

| Slides | File | Page |
|---|---|---|
| 01 iframes | `test_01_iframes.py` | demoqa.com/frames, the-internet /nested_frames |
| 02 Download | `test_02_download.py` | the-internet /download |
| 03 Basic auth | `test_03_basic_auth.py` | the-internet /basic_auth (admin / admin) |
| 04 Keyboard | `test_04_keyboard.py` | the-internet /login, /horizontal_slider |
| 05 Shadow DOM | `test_05_shadow_dom.py` | practice.expandtesting.com/shadowdom |
| 06 Mobile | `test_06_mobile.py` | practice.expandtesting.com |

## One line per problem

| Problem | Tool |
|---|---|
| a page inside a page | `page.frame_locator("#id").locator(...)` |
| a file comes back | `with page.expect_download() as info:` |
| browser sign-in window | `browser.new_context(http_credentials={...})` |
| no mouse | `locator.press("Tab")`, `expect(...).to_be_focused()` |
| hidden HTML | CSS or `get_by_role` — not XPath |
| small screen | `browser.new_context(**playwright.devices["iPhone 13"])` |

## Docs (switch the language to Python)

- Frames — https://playwright.dev/python/docs/frames
- Downloads — https://playwright.dev/python/docs/downloads
- HTTP authentication — https://playwright.dev/python/docs/network#http-authentication
- Keys and shortcuts — https://playwright.dev/python/docs/input#keys-and-shortcuts
- Shadow DOM — https://playwright.dev/python/docs/locators#locate-in-shadow-dom
- Emulation — https://playwright.dev/python/docs/emulation
