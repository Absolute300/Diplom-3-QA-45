import allure

from data import IngredientIds
from helpers import extract_order_number
from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage
from urls import CONSTRUCTOR_URL


class MainPage(BasePage):
    @allure.step("Open constructor")
    def open_constructor(self):
        self.open(CONSTRUCTOR_URL)
        self.wait_constructor_loaded()

    @allure.step("Wait for constructor content")
    def wait_constructor_loaded(self):
        self.wait_visible(MainPageLocators.CONSTRUCTOR_TITLE)
        self.wait_visible(MainPageLocators.INGREDIENTS_MENU)
        self.wait_visible(MainPageLocators.CONSTRUCTOR_BASKET)
        self.wait_visible(MainPageLocators.ingredient_card(IngredientIds.BUN))

    @allure.step("Click Constructor link")
    def click_constructor(self):
        self.click(MainPageLocators.CONSTRUCTOR_LINK)
        self.wait_constructor_loaded()

    @allure.step("Go to order feed")
    def go_to_order_feed(self):
        self.click(MainPageLocators.ORDER_FEED_LINK)

    @allure.step("Open ingredient details")
    def open_ingredient_details(self, ingredient_id=IngredientIds.SAUCE):
        self.click(MainPageLocators.ingredient_card(ingredient_id))
        self.wait_present(MainPageLocators.MODAL_OPENED)
        return self.wait_visible(MainPageLocators.MODAL_CONTAINER)

    @allure.step("Close ingredient modal")
    def close_ingredient_modal(self):
        self.click(MainPageLocators.MODAL_CLOSE_BUTTON)
        self.wait_invisible(MainPageLocators.MODAL_OPENED)

    @allure.step("Check ingredient modal is opened")
    def is_ingredient_modal_opened(self):
        return self.wait_visible(MainPageLocators.INGREDIENT_DETAILS_TITLE).is_displayed()

    @allure.step("Get ingredient counter")
    def get_ingredient_counter(self, ingredient_id):
        counter = self.find_element(
            MainPageLocators.ingredient_counter_in_card(ingredient_id)
        )
        return int(counter.text)

    @allure.step("Add ingredient to order")
    def add_ingredient_to_order(self, ingredient_id):
        source = self.find_element(MainPageLocators.ingredient_card(ingredient_id))
        target = self.find_element(MainPageLocators.CONSTRUCTOR_DROP_TARGET)
        counter_locator = MainPageLocators.ingredient_counter_in_card(ingredient_id)
        old_value = int(self.find_element(counter_locator).text)
        self.wait_counter_increased_with_fallback(
            source, target, counter_locator, old_value
        )

    @allure.step("Add basic ingredients to order")
    def add_basic_order_ingredients(self):
        self.add_ingredient_to_order(IngredientIds.BUN)
        self.add_ingredient_to_order(IngredientIds.SAUCE)

    @allure.step("Set auth tokens in localStorage")
    def set_auth_tokens(self, access_token, refresh_token):
        self.open(CONSTRUCTOR_URL)
        self.driver.execute_script(
            "localStorage.setItem('accessToken', arguments[0]);"
            "localStorage.setItem('refreshToken', arguments[1]);",
            access_token,
            refresh_token,
        )
        self.driver.refresh()
        self.wait_constructor_loaded()

    @allure.step("Create order")
    def create_order(self):
        self.click(MainPageLocators.ORDER_BUTTON)
        self.wait_present(MainPageLocators.MODAL_OPENED, timeout=90)
        self.wait_visible(MainPageLocators.MODAL_CONTAINER, timeout=90)
        self.wait_until(
            lambda _: self.is_created_order_modal_ready(),
            timeout=90,
        )
        return self.get_created_order_number()

    @allure.step("Get created order number")
    def get_created_order_number(self):
        modal_text = self.get_visible_modal_text()
        return extract_order_number(modal_text)

    def get_visible_modal_text(self):
        for modal in self.find_elements(MainPageLocators.MODAL_CONTAINER):
            if modal.is_displayed():
                return modal.text
        return ""

    def is_created_order_modal_ready(self):
        modal_text = self.get_visible_modal_text()
        if "Ваш заказ начали готовить" not in modal_text:
            return False
        try:
            return extract_order_number(modal_text) != "9999"
        except ValueError:
            return False