# Lecture 6 · Inside the Browser — examples

Every example from the lecture 6 slides. Run them:

```powershell
uv run pytest tests/lecture_6 -v                                   # all (chromium)
uv run pytest tests/lecture_6/test_07_cookies.py                   # one file
uv run pytest tests/lecture_6 --browser chromium --browser firefox --browser webkit
uv run pytest tests/lecture_6 --browser-channel chrome             # real Chrome
uv run pytest tests/lecture_6 --headed --slowmo 500                # watch it
uv run pytest tests/lecture_6 --tracing retain-on-failure          # trace on failure
uv run playwright show-trace test-results/<test-name>/trace.zip
uv run playwright codegen --target python-pytest https://www.saucedemo.com
```

Once, for firefox and webkit: `uv run playwright install`.
Classroom computers: `$env:Path += ";C:\Users\student\AppData\Roaming\Python\Scripts"` first.

The tests use live sites (saucedemo.com, demoqa.com, playwright.dev).
If a site is slow, run the failed tests again: `uv run pytest --lf`.

## Slide → file

| Part · slides | File |
|---|---|
| 01 Console · picture / code | `test_01_console.py` |
| 01 Network · picture / code | `test_02_network.py` |
| 02 Engines · three browsers · markers and channels | `test_03_browsers.py` |
| 02 Breakpoints · window size · one fixture for every test | `test_04_viewport.py`, `conftest.py` |
| 03 Contexts · incognito · launch options | `test_05_launch_and_context.py` |
| 03 The user's world (Sensors, Rendering) | `test_06_world.py` |
| 04 Anatomy of a cookie · login with a cookie | `test_07_cookies.py` |
| 04 storage_state | `test_08_storage_state.py` |
| 05 evaluate · the JS click trap | `test_09_evaluate.py` |
| 05 Change the network (route) | `test_10_route.py` |
| 06 Inspector · Trace Viewer | `test_11_debugging.py` |
| 06 codegen: draft → test, test ids | `test_12_codegen.py` |
| Practice: full shop scenario (POM, parametrize, money, storage) | `test_13_checkout_e2e.py`, `pages/saucedemo.py` |
| 06 codegen with your own setup (page.pause) | `codegen_custom_setup.py` (run with `uv run python`) |

## DevTools panel → Playwright

| DevTools | In a test |
|---|---|
| Elements | `page.locator(...)`, `codegen` |
| Console | `page.on("console")`, `page.on("pageerror")`, `page.evaluate(...)` |
| Network | `page.expect_response(...)`, `context.set_offline(True)`, `page.route(...)` |
| Application | `context.cookies()`, `context.add_cookies(...)`, `context.clear_cookies()`, `storage_state` |
| Device Toolbar | `viewport`, `page.set_viewport_size(...)`, `devices[...]`, `--device` |
| Sensors, Rendering | `locale`, `timezone_id`, `geolocation` + `permissions`, `color_scheme` |
| Sources | `page.pause()`, `PWDEBUG=1`, Trace Viewer |
| Recorder | `playwright codegen` |

## codegen commands

```powershell
uv run playwright codegen https://www.saucedemo.com                         # record
uv run playwright codegen --target python-pytest -o tests/lecture_6/test_draft.py https://www.saucedemo.com
uv run playwright codegen --test-id-attribute data-test https://www.saucedemo.com   # get_by_test_id(...)
uv run playwright codegen --device "iPhone 13" playwright.dev
uv run playwright codegen --viewport-size "800,600" playwright.dev
uv run playwright codegen --color-scheme dark --lang ka-GE --timezone Asia/Tbilisi --geolocation "41.7151,44.8271" playwright.dev
uv run playwright codegen -b firefox https://demoqa.com
uv run playwright codegen --save-storage auth.json https://www.saucedemo.com   # log in, close
uv run playwright codegen --load-storage auth.json https://www.saucedemo.com/inventory.html
uv run playwright codegen --help                                               # all flags
uv run python tests/lecture_6/codegen_custom_setup.py                         # own setup + page.pause()
```

Never commit `auth.json`: it is a key to the account.

## Notes

- `test_default_viewport` fails on purpose with `--device`: the size is no longer 1280 × 720.
- `test_pause_in_the_middle` is skipped unless `$env:LECTURE6_PAUSE=1`.
- `test_launch_options` opens a real window (headless=False); it needs a screen.
