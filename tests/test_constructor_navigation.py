import allure
import pytest
from pages.main_page import MainPage
from selenium.webdriver.support import expected_conditions as EC

class TestConstructorNavigation:
    """
    Тесты для навигации в конструкторе
    """
    
    @allure.title("Переход по клику на 'Конструктор'")
    def test_click_constructor_tab(self, driver):
        """Проверяем переход на вкладку Конструктор"""
        main_page = MainPage(driver)
        main_page.open("/")
        
        main_page.click_constructor_tab()
        
        main_page.wait_for_condition(EC.url_contains("stellarburgers"), timeout=10, condition_name="url содержит stellarburgers")

        current_url = main_page.get_current_url()
        assert "stellarburgers" in current_url, f"Неверный URL после клика на конструктор: {current_url}"
    
    @allure.title("Переход по клику на 'Лента заказов'")
    def test_click_order_feed_tab(self, driver):
        """Проверяем переход на вкладку Лента заказов"""
        main_page = MainPage(driver)
        main_page.open("/")

        main_page.click_order_feed_tab()
        
        main_page.wait_for_condition(EC.url_contains("/feed"), timeout=10, condition_name="url содержит /feed")
        
        current_url = main_page.get_current_url()
        assert "feed" in current_url, f"Неверный URL после клика на ленту заказов: {current_url}"
        
        main_page.wait_for_condition(
            EC.any_of(EC.title_contains("Лента заказов"), EC.title_contains("Stellar Burgers")),
            timeout=10,
            condition_name="title содержит ожидаемый текст",
        )

        page_title = main_page.get_page_title()
        assert "Лента заказов" in page_title or "Stellar Burgers" in page_title, \
            f"Заголовок страницы не содержит ожидаемый текст: {page_title}"