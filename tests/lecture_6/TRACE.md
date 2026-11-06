# Lecture 6 · Trace Viewer — see why a test failed

A **trace** is a recording of a test that already ran.
For every step you see a screenshot, the page, the network and the console.

> Trace = look **back** at a test.
> To write a **new** test, see [CODEGEN.md](CODEGEN.md).

Run all commands in PowerShell, in the project folder
`D:\IdeaProjects\lecture-3-playwright`.

---

## 1 · Run the tests with a trace

```powershell
uv run pytest tests/lecture_6 --tracing retain-on-failure
```

`retain-on-failure` = keep a trace only for **failed** tests.
Want a trace for every test? Use `--tracing on`.

## 2 · Find the trace file

```powershell
ls test-results
```

Every test has its own folder. Inside it there is `trace.zip`:

```text
test-results/
└── tests-lecture-6-test-07-cookies-py-test-login-with-cookie-chromium/
    └── trace.zip
```

## 3 · Open it

```powershell
uv run playwright show-trace test-results/<folder>/trace.zip
```

Tip: type `test-results/tests-lecture-6-test-07` and press **Tab** —
PowerShell writes the rest of the name for you.

## 4 · Find the problem

```text
┌──────────────┬──────────────────────────────────┐
│ Actions      │ Screenshot of the page           │
│              │ (Before / After)                 │
│ goto         │                                  │
│ fill         │                                  │
│ click   ❌   ├──────────────────────────────────┤
│              │ Errors · Console · Network ·     │
│              │ Source                           │
└──────────────┴──────────────────────────────────┘
```

1. Click the **red** step on the left.
2. Open **Errors** — read the message.
3. Look at the **Before** screenshot — what did the page look like?
4. If you need more: **Network** (requests and status codes),
   **Console** (JavaScript errors), **Source** (your Python line).

Usually you see the reason at once: wrong page, a popup on top,
different text, the element was not there yet.

---

## Cheat sheet

```powershell
uv run pytest tests/lecture_6 --tracing retain-on-failure   # trace for failed tests
uv run pytest tests/lecture_6 --tracing on                  # trace for every test
ls test-results                                             # find the folder
uv run playwright show-trace test-results/<folder>/trace.zip
```

No terminal? Drag `trace.zip` onto https://trace.playwright.dev
(the file stays on your computer).

Docs: https://playwright.dev/python/docs/trace-viewer-intro
