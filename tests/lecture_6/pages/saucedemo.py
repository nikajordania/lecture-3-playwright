"""SauceDemo pages: login → inventory → cart → checkout (2 steps) → complete.

Rules used in every class:
  * element  → locator attribute (made once in __init__, found lazily)
  * action   → method; it returns the page the user lands on
  * NO asserts here — pages DO things, tests CHECK things
  * get_by_test_id(...) works because the test switches the
    test-id attribute to "data-test" (see fixture in test_13)
"""
from dataclasses import dataclass
from decimal import Decimal

from playwright.sync_api import Locator, Page

BASE = "https://www.saucedemo.com"


def money(text: str) -> Decimal:
    """'$29.99' or 'Item total: $29.99' → Decimal('29.99').

    Decimal, not float: 0.1 + 0.2 == 0.30000000000000004 with float.
    """
    return Decimal(text.rsplit("$", 1)[1])


@dataclass(frozen=True)
class Product:
    name: str
    price: Decimal


class BasePage:
    PATH = "/"

    def __init__(self, page: Page):
        self.page = page
        self.title = page.get_by_test_id("title")
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")

    @property
    def url(self) -> str:
        return BASE + self.PATH

    def cart_contents(self) -> list[int]:
        """The cart lives in localStorage as a JSON list of product ids."""
        return self.page.evaluate(
            "JSON.parse(localStorage.getItem('cart-contents') || '[]')"
        )


class LoginPage(BasePage):
    PATH = "/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.username = page.get_by_test_id("username")
        self.password = page.get_by_test_id("password")
        self.submit = page.get_by_test_id("login-button")
        self.error = page.get_by_test_id("error")

    def open(self) -> "LoginPage":
        self.page.goto(self.url)
        return self

    def login(self, user: str, password: str) -> "InventoryPage":
        self.username.fill(user)
        self.password.fill(password)
        self.submit.click()
        return InventoryPage(self.page)

    def login_expecting_error(self, user: str, password: str) -> "LoginPage":
        self.username.fill(user)
        self.password.fill(password)
        self.submit.click()
        return self


class InventoryPage(BasePage):
    PATH = "/inventory.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.items = page.get_by_test_id("inventory-item")
        self.names = page.get_by_test_id("inventory-item-name")
        self.prices = page.get_by_test_id("inventory-item-price")
        self.sort_select = page.get_by_test_id("product-sort-container")

    def item(self, name: str) -> Locator:
        """One product card — filter the list by its text."""
        return self.items.filter(has_text=name)

    def add_button(self, name: str) -> Locator:
        return self.item(name).get_by_role("button", name="Add to cart")

    def remove_button(self, name: str) -> Locator:
        return self.item(name).get_by_role("button", name="Remove")

    def product(self, name: str) -> Product:
        """Read name + price FROM THE PAGE — the source of truth for later checks."""
        price = self.item(name).get_by_test_id("inventory-item-price").inner_text()
        return Product(name, money(price))

    def add_to_cart(self, name: str) -> Product:
        product = self.product(name)
        self.add_button(name).click()
        return product

    def sort_by(self, value: str) -> "InventoryPage":
        """value: az | za | lohi | hilo"""
        self.sort_select.select_option(value)
        return self

    def all_names(self) -> list[str]:
        return self.names.all_inner_texts()

    def all_prices(self) -> list[Decimal]:
        return [money(p) for p in self.prices.all_inner_texts()]

    def open_cart(self) -> "CartPage":
        self.cart_link.click()
        return CartPage(self.page)


class CartPage(BasePage):
    PATH = "/cart.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.items = page.get_by_test_id("inventory-item")
        self.names = page.get_by_test_id("inventory-item-name")
        self.quantities = page.get_by_test_id("item-quantity")
        self.checkout_button = page.get_by_test_id("checkout")

    def products(self) -> list[Product]:
        result = []
        for row in self.items.all():
            name = row.get_by_test_id("inventory-item-name").inner_text()
            price = row.get_by_test_id("inventory-item-price").inner_text()
            result.append(Product(name, money(price)))
        return result

    def remove(self, name: str) -> "CartPage":
        self.items.filter(has_text=name).get_by_role("button", name="Remove").click()
        return self

    def checkout(self) -> "CheckoutInfoPage":
        self.checkout_button.click()
        return CheckoutInfoPage(self.page)


class CheckoutInfoPage(BasePage):
    PATH = "/checkout-step-one.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name = page.get_by_test_id("firstName")
        self.last_name = page.get_by_test_id("lastName")
        self.postal_code = page.get_by_test_id("postalCode")
        self.continue_button = page.get_by_test_id("continue")
        self.error = page.get_by_test_id("error")

    def fill(self, first: str, last: str, postal: str) -> "CheckoutInfoPage":
        # fill("") is fine: it clears the field — used by the validation test
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)
        return self

    def continue_to_overview(self) -> "CheckoutOverviewPage":
        self.continue_button.click()
        return CheckoutOverviewPage(self.page)


class CheckoutOverviewPage(BasePage):
    PATH = "/checkout-step-two.html"
    TAX_RATE = Decimal("0.08")

    def __init__(self, page: Page):
        super().__init__(page)
        self.names = page.get_by_test_id("inventory-item-name")
        self.payment_info = page.get_by_test_id("payment-info-value")
        self.shipping_info = page.get_by_test_id("shipping-info-value")
        self.subtotal = page.get_by_test_id("subtotal-label")
        self.tax = page.get_by_test_id("tax-label")
        self.total = page.get_by_test_id("total-label")
        self.finish_button = page.get_by_test_id("finish")

    def finish(self) -> "CheckoutCompletePage":
        self.finish_button.click()
        return CheckoutCompletePage(self.page)


class CheckoutCompletePage(BasePage):
    PATH = "/checkout-complete.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.header = page.get_by_test_id("complete-header")
        self.text = page.get_by_test_id("complete-text")
        self.back_home = page.get_by_test_id("back-to-products")

    def go_home(self) -> InventoryPage:
        self.back_home.click()
        return InventoryPage(self.page)
