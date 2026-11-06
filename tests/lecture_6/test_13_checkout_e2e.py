"""Lecture 6 · 13 — A full shop scenario on saucedemo.com (end-to-end).

One big story + smaller data-driven tests around it.

Good practices you can find here (search for "PRACTICE"):
   1  Page Object Model            — tests/lecture_6/pages/saucedemo.py
   2  Stable locators              — get_by_test_id + data-test attribute
   3  Fixtures for setup/teardown  — test-id switch, JS-error guard, login
   4  Test data in ONE place       — constants + dataclass Product
   5  Expected values come from the page, not copy-pasted numbers
   6  Money as Decimal, not float
   7  Web-first assertions (expect) — they wait by themselves, no sleep()
   8  Check the STATE too, not only the screen (localStorage)
   9  Parametrize + readable ids   — one test body, many data rows
  10  Arrange / Act / Assert        — every test reads top to bottom
  11  Tests are independent        — each one starts from a clean context

Run:
    uv run pytest tests/lecture_6/test_13_checkout_e2e.py -v
    uv run pytest tests/lecture_6/test_13_checkout_e2e.py -k full_checkout --slowmo 300
    uv run pytest tests/lecture_6/test_13_checkout_e2e.py --tracing retain-on-failure
"""
import re
from decimal import ROUND_HALF_UP, Decimal

import pytest
from playwright.sync_api import Page, Playwright, expect

from .pages.saucedemo import (
    BASE,
    CheckoutOverviewPage,
    InventoryPage,
    LoginPage,
    money,
)

# ---------- PRACTICE 4 · test data in one place ----------

USER = "standard_user"
PASSWORD = "secret_sauce"
CUSTOMER = {"first": "Nika", "last": "Tester", "postal": "0108"}

BACKPACK = "Sauce Labs Backpack"
BOLT_SHIRT = "Sauce Labs Bolt T-Shirt"
FLEECE = "Sauce Labs Fleece Jacket"
BIKE_LIGHT = "Sauce Labs Bike Light"


# ---------- PRACTICE 3 · fixtures ----------

@pytest.fixture(autouse=True)
def data_test_ids(playwright: Playwright):
    """PRACTICE 2: SauceDemo marks elements with data-test="...".

    Tell Playwright, so get_by_test_id("x") finds [data-test="x"].
    Put the default back after the test — other files expect data-testid.
    """
    playwright.selectors.set_test_id_attribute("data-test")
    yield
    playwright.selectors.set_test_id_attribute("data-testid")


@pytest.fixture(autouse=True)
def no_js_errors(page: Page):
    """Every test here ALSO fails if the page throws an uncaught JS error.

    The check runs in the teardown part (after yield) — after the test body.
    """
    errors: list[str] = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    yield
    assert errors == [], f"JavaScript errors on the page: {errors}"


@pytest.fixture
def inventory(page: Page) -> InventoryPage:
    """Logged in through the real login form → on the Products page."""
    inventory = LoginPage(page).open().login(USER, PASSWORD)
    expect(page).to_have_url(inventory.url)
    return inventory


def expected_tax(subtotal: Decimal) -> Decimal:
    """SauceDemo tax is 8 %, rounded to cents. PRACTICE 6: Decimal."""
    return (subtotal * CheckoutOverviewPage.TAX_RATE).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )


# ======================================================================
# 1 · The big story: buy 3 products, change your mind once, pay, check all
# ======================================================================

def test_full_checkout_with_three_products(inventory: InventoryPage, page: Page):
    # --- Arrange: the shop is open, the cart is empty --------------------
    expect(inventory.title).to_have_text("Products")
    expect(inventory.items).to_have_count(6)
    expect(inventory.cart_badge).to_be_hidden()
    assert inventory.cart_contents() == []

    # --- Act 1: add four products (PRACTICE 5: prices read from the page) -
    bought = [inventory.add_to_cart(name)
              for name in (BACKPACK, BIKE_LIGHT, BOLT_SHIRT, FLEECE)]

    # --- Assert 1: badge, buttons and storage all agree ------------------
    expect(inventory.cart_badge).to_have_text("4")
    for product in bought:
        expect(inventory.remove_button(product.name)).to_be_visible()
        expect(inventory.add_button(product.name)).to_have_count(0)
    assert len(inventory.cart_contents()) == 4           # PRACTICE 8

    # --- Act 2: open the cart and remove one product ---------------------
    cart = inventory.open_cart()
    expect(page).to_have_url(cart.url)
    expect(cart.title).to_have_text("Your Cart")
    cart.remove(BIKE_LIGHT)
    bought = [p for p in bought if p.name != BIKE_LIGHT]

    # --- Assert 2: the cart shows exactly what we kept -------------------
    expect(cart.items).to_have_count(3)
    expect(cart.names).to_have_text([p.name for p in bought])   # order matters
    expect(cart.quantities).to_have_text(["1", "1", "1"])
    expect(cart.cart_badge).to_have_text("3")
    assert cart.products() == bought                     # same names AND prices
    assert len(cart.cart_contents()) == 3

    # --- Act 3: fill the customer form -----------------------------------
    info = cart.checkout()
    expect(page).to_have_url(info.url)
    expect(info.title).to_have_text("Checkout: Your Information")
    overview = info.fill(**CUSTOMER).continue_to_overview()

    # --- Assert 3: the overview — money is calculated, not hard-coded ----
    expect(page).to_have_url(overview.url)
    expect(overview.title).to_have_text("Checkout: Overview")
    expect(overview.names).to_have_text([p.name for p in bought])
    expect(overview.payment_info).to_have_text("SauceCard #31337")
    expect(overview.shipping_info).to_have_text("Free Pony Express Delivery!")

    subtotal = sum((p.price for p in bought), Decimal("0"))
    tax = expected_tax(subtotal)
    total = subtotal + tax
    expect(overview.subtotal).to_have_text(f"Item total: ${subtotal}")
    expect(overview.tax).to_have_text(f"Tax: ${tax}")
    expect(overview.total).to_have_text(f"Total: ${total}")
    # and once more the other way round: the page's own numbers add up
    assert money(overview.subtotal.inner_text()) + money(overview.tax.inner_text()) \
        == money(overview.total.inner_text())

    # --- Act 4: finish the order -----------------------------------------
    complete = overview.finish()

    # --- Assert 4: success page, cart is empty everywhere ----------------
    expect(page).to_have_url(complete.url)
    expect(complete.title).to_have_text("Checkout: Complete!")
    expect(complete.header).to_have_text("Thank you for your order!")
    expect(complete.text).to_contain_text("dispatched")
    expect(complete.cart_badge).to_be_hidden()
    assert complete.cart_contents() == []

    # --- Act 5 + Assert 5: back to the shop, everything is reset ---------
    home = complete.go_home()
    expect(page).to_have_url(home.url)
    expect(page.get_by_role("button", name="Remove")).to_have_count(0)
    expect(page.get_by_role("button", name="Add to cart")).to_have_count(6)


# ======================================================================
# 2 · Login — one body, many data rows (PRACTICE 9)
# ======================================================================

@pytest.mark.parametrize(
    ("user", "password", "message"),
    [
        ("locked_out_user", PASSWORD, "Sorry, this user has been locked out."),
        (USER, "wrong_password",
         "Username and password do not match any user in this service"),
        ("", PASSWORD, "Username is required"),
        (USER, "", "Password is required"),
    ],
    ids=["locked-out", "wrong-password", "no-username", "no-password"],
)
def test_login_errors(page: Page, user: str, password: str, message: str):
    login = LoginPage(page).open()

    login.login_expecting_error(user, password)

    expect(login.error).to_be_visible()
    expect(login.error).to_contain_text(message)
    expect(page).to_have_url(BASE + "/")                 # we did NOT get in
    expect(login.username).to_have_class(re.compile(r"\berror\b"))   # red field


# ======================================================================
# 3 · Checkout form validation — each missing field has its own message
# ======================================================================

@pytest.mark.parametrize(
    ("first", "last", "postal", "message"),
    [
        ("", "Tester", "0108", "Error: First Name is required"),
        ("Nika", "", "0108", "Error: Last Name is required"),
        ("Nika", "Tester", "", "Error: Postal Code is required"),
    ],
    ids=["no-first-name", "no-last-name", "no-postal-code"],
)
def test_checkout_form_validation(inventory: InventoryPage, page: Page,
                                  first: str, last: str, postal: str, message: str):
    inventory.add_to_cart(BACKPACK)
    info = inventory.open_cart().checkout()

    info.fill(first, last, postal).continue_button.click()

    expect(info.error).to_have_text(message)
    expect(page).to_have_url(info.url)                   # still on step one
    expect(info.cart_badge).to_have_text("1")            # cart not lost


# ======================================================================
# 4 · Sorting — the list must REALLY be sorted, for all four options
# ======================================================================

@pytest.mark.parametrize(
    ("option", "key", "reverse"),
    [
        ("az", "names", False),
        ("za", "names", True),
        ("lohi", "prices", False),
        ("hilo", "prices", True),
    ],
    ids=["name-a-z", "name-z-a", "price-low-high", "price-high-low"],
)
def test_sorting(inventory: InventoryPage, option: str, key: str, reverse: bool):
    inventory.sort_by(option)

    expect(inventory.sort_select).to_have_value(option)
    values = inventory.all_names() if key == "names" else inventory.all_prices()
    assert len(values) == 6
    assert values == sorted(values, reverse=reverse), f"{option}: {values}"


# ======================================================================
# 5 · The cart survives a reload (it is kept in localStorage)
# ======================================================================

def test_cart_survives_reload(inventory: InventoryPage, page: Page):
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(FLEECE)

    page.reload()

    expect(inventory.cart_badge).to_have_text("2")
    expect(inventory.remove_button(BACKPACK)).to_be_visible()
    expect(inventory.remove_button(FLEECE)).to_be_visible()
    cart = inventory.open_cart()
    expect(cart.names).to_have_text([BACKPACK, FLEECE])
