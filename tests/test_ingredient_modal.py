import allure

from pages.main_page import MainPage
from data.test_data import TestData


class TestIngredientModal:
    """
    Тесты для модальных окон ингредиентов
    """

    @allure.title("Клик на ингредиент открывает модальное окно с деталями")
    def test_click_ingredient_opens_modal(self, driver):
        """Проверяем что клик на ингредиент открывает детали"""
        main_page = MainPage(driver)
        main_page.open("/")

        with allure.step("Кликнуть на ингредиент"):
            main_page.click_ingredient(TestData.INGREDIENT_TRADITIONAL_SAUCE)

        with allure.step("Проверить что модальное окно открылось"):
            assert main_page.is_modal_visible(), "Модальное окно не открылось"

        with allure.step("Проверить заголовок модального окна"):
            modal_title = main_page.get_modal_title()
            assert TestData.MODAL_TITLE_DETAILS in modal_title, (
                f"Заголовок модалки неверный: {modal_title}"
            )

        with allure.step("Проверить название ингредиента в модалке"):
            ingredient_name = main_page.get_modal_ingredient_name()
            assert TestData.INGREDIENT_NAME_TRADITIONAL_SAUCE in ingredient_name, (
                f"Название ингредиента неверное: {ingredient_name}"
            )

    @allure.title("Всплывающее окно закрывается кликом по крестику")
    def test_close_modal_by_cross(self, driver):
        """Проверяем закрытие модального окна"""
        main_page = MainPage(driver)
        main_page.open("/")

        with allure.step("Открыть модальное окно"):
            main_page.click_ingredient(TestData.INGREDIENT_TRADITIONAL_SAUCE)
            assert main_page.is_modal_visible(), "Модальное окно не открылось"

        with allure.step("Закрыть модальное окно"):
            main_page.close_modal()

        with allure.step("Проверить что модальное окно закрылось"):
            assert main_page.is_modal_closed(), "Модальное окно не закрылось"

        with allure.step("Дождаться полного закрытия модалки (фикс для Firefox)"):
            main_page.wait_for_modal_completely_hidden_for_firefox(10)