import allure
import pytest

from data import IngredientIds, IngredientNames
from locators.main_page_locators import MainPageLocators
from locators.order_feed_locators import OrderFeedLocators
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage


@pytest.mark.ui
@allure.feature("Constructor")
class TestConstructor:
    @allure.story("Navigation")
    @allure.title("Переход по клику на раздел Конструктор")
    def test_click_constructor_opens_constructor_section(self, driver):
        feed_page = OrderFeedPage(driver)
        feed_page.open_order_feed()

        main_page = MainPage(driver)
        main_page.click_constructor()

        assert main_page.wait_visible(MainPageLocators.CONSTRUCTOR_TITLE).is_displayed()
        assert main_page.wait_visible(MainPageLocators.INGREDIENTS_MENU).is_displayed()
        assert main_page.wait_visible(MainPageLocators.CONSTRUCTOR_BASKET).is_displayed()

    @allure.story("Navigation")
    @allure.title("Переход по клику на раздел Лента Заказов")
    def test_click_order_feed_opens_order_feed_section(self, driver):
        main_page = MainPage(driver)
        main_page.open_constructor()

        main_page.go_to_order_feed()
        feed_page = OrderFeedPage(driver)
        feed_page.wait_feed_loaded_with_retry()

        assert "/feed" in feed_page.get_current_url()
        assert feed_page.wait_visible(OrderFeedLocators.ORDER_FEED_TITLE).is_displayed()
        assert feed_page.wait_visible(OrderFeedLocators.ORDERS_DATA).is_displayed()

    @allure.feature("Ingredient details")
    @allure.story("Ingredient modal")
    @allure.title("При клике на ингредиент появляется окно с деталями")
    def test_click_ingredient_opens_details_modal(self, driver):
        main_page = MainPage(driver)
        main_page.open_constructor()

        modal = main_page.open_ingredient_details(IngredientIds.SAUCE)

        assert main_page.is_ingredient_modal_opened()
        assert IngredientNames.SAUCE in modal.text
        assert "Калории,ккал" in modal.text
        assert "Белки, г" in modal.text
        assert main_page.wait_visible(MainPageLocators.MODAL_CLOSE_BUTTON).is_displayed()

    @allure.feature("Ingredient details")
    @allure.story("Ingredient modal")
    @allure.title("Всплывающее окно закрывается кликом по крестику")
    def test_ingredient_details_modal_closes_by_cross_click(self, driver):
        main_page = MainPage(driver)
        main_page.open_constructor()
        main_page.open_ingredient_details(IngredientIds.SAUCE)

        main_page.close_ingredient_modal()

        assert main_page.wait_visible(MainPageLocators.CONSTRUCTOR_TITLE).is_displayed()
        assert main_page.wait_visible(MainPageLocators.CONSTRUCTOR_BASKET).is_displayed()

    @allure.story("Ingredient counter")
    @allure.title("При добавлении ингредиента в заказ счетчик увеличивается")
    def test_add_ingredient_to_order_increases_counter(self, driver):
        main_page = MainPage(driver)
        main_page.open_constructor()
        old_counter = main_page.get_ingredient_counter(IngredientIds.BUN)

        main_page.add_ingredient_to_order(IngredientIds.BUN)
        new_counter = main_page.get_ingredient_counter(IngredientIds.BUN)

        assert new_counter > old_counter