"""Fixtures for lecture 4. Slide "The test asks, the fixture builds the page".

These fixtures are only visible to tests inside tests/lecture_4/.
The root conftest.py (block_ads, new_user) still works here too.
"""
import pytest
from playwright.sync_api import Page

from .pages.login_page import LoginPage
from .pages.secure_page import SecurePage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page).open()


@pytest.fixture
def secure_page(login_page: LoginPage) -> SecurePage:
    # A fixture can use another fixture.
    return login_page.login("tomsmith", "SuperSecretPassword!")
