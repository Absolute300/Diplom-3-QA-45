import allure
import pytest
from pages.main_page import MainPage
from data.test_data import TestData

class TestIngredientCounter:
    """
    Тесты для счетчиков ингредиентов
    """
    @allure.title("При добавлении ингредиента в заказ счётчик увеличивается")
    def test_ingredient_counter_increases(self, driver):
        """Проверяем что счетчик ингредиента увеличивается при добавлении"""
        main_page = MainPage(driver)
        main_page.open("/")
        
        with allure.step("Перейти в раздел соусов"):
            main_page.switch_to_sauces_section()
        
        with allure.step("Получить начальное значение счетчика"):
            initial_counter = main_page.get_ingredient_counter_value(TestData.INGREDIENT_TRADITIONAL_SAUCE)
        
        with allure.step("Перетащить ингредиент в конструктор"):
            main_page.drag_ingredient_to_constructor(TestData.INGREDIENT_TRADITIONAL_SAUCE)
        
        with allure.step("Дождаться увеличения счетчика"):
            main_page.wait_for_ingredient_counter_increase(
                TestData.INGREDIENT_TRADITIONAL_SAUCE, 
                initial_counter
            )
            final_counter = main_page.get_ingredient_counter_value(TestData.INGREDIENT_TRADITIONAL_SAUCE)
        
        with allure.step("Проверить что счетчик увеличился"):
            assert final_counter > initial_counter, (
                f"Счетчик не увеличился: было {initial_counter}, стало {final_counter}"
            )