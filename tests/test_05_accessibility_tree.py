"""01 · Find — the accessibility tree.

Slide: "The browser also builds a tree of roles".
get_by_role() does not read HTML tags - it reads this tree:

    - textbox "Username"
    - textbox "Password"
    - button "Login"

DevTools -> Elements -> Accessibility pane shows the same tree.
"""
from playwright.sync_api import Page, expect

LOGIN = "https://the-internet.herokuapp.com/login"


def test_print_the_accessibility_tree(page: Page):
    page.goto(LOGIN)
    tree = page.locator("#login").aria_snapshot()
    print("\n" + tree)  # run with -s to see it

    assert 'textbox "Username"' in tree
    assert 'button "Login"' in tree


def test_login_form_matches_aria_snapshot(page: Page):
    page.goto(LOGIN)
    # Lines we do not list (for example "- text: Username") are allowed.
    expect(page.locator("#login")).to_match_aria_snapshot(
        """
        - textbox "Username"
        - textbox "Password"
        - button "Login"
        """
    )


def test_role_and_css_find_the_same_element(page: Page):
    page.goto(LOGIN)
    by_role = page.get_by_role("textbox", name="Username")
    # Same element: the one with id="username"
    expect(by_role).to_have_attribute("id", "username")
    # The button's name "Login" comes from the text inside it:
    # <button><i class="fa fa-sign-in"> Login</i></button>
    expect(page.get_by_role("button", name="Login")).to_have_attribute("type", "submit")
