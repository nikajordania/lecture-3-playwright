"""Waits: Selenium wait types adapted to Playwright.

    test_01_implicit_wait.py       Implicit Wait  ->  auto-waiting + default timeouts
    test_02_explicit_wait.py       Explicit Wait  ->  expect(..., timeout=), wait_for(), wait_for_url()...
    test_03_fluent_wait.py         Fluent Wait    ->  wait_for_function(polling=), own polling helper
    test_04_expected_conditions.py every Selenium expected_condition -> its Playwright line

Run only this package:   uv run pytest tests/waits -v
"""
