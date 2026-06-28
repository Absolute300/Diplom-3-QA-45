# profile_page.py

import allure
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from .base_page import BasePage
from locators.profile_page_locators import ProfilePageLocators
from config import config
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException
)

logger = logging.getLogger(__name__)

class ProfilePage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver, config.PROFILE_URL)
        self.locators = ProfilePageLocators()
        self.logger = logging.getLogger(__name__)

    @allure.step("Открыть страницу профиля")
    def open(self) -> None:
        """Открывает страницу профиля и проверяет её загрузку."""
        super().open()
        self._verify_page_loaded()

    def _verify_page_loaded(self) -> None:
        """Внутренняя проверка загрузки страницы"""
        self.wait_until_visible(self.locators.PROFILE_FORM)
        self.url_should_contain("account/profile")

    @allure.step("Нажать на ссылку истории заказов")
    def click_order_history_link(self) -> None:
        """Кликает на ссылку истории заказов без ожидания раздела"""
        self.click(self.locators.ORDER_HISTORY_LINK)
        self.wait_until_url_contains("order-history")

    @allure.step("Выйти из аккаунта")
    def logout(self) -> None:
        """Выполняет выход из аккаунта."""
        self.click(self.locators.LOGOUT_BUTTON)
        self.wait_until_url_contains("login")

    @allure.step("Проверить видимость формы профиля")
    def is_profile_form_visible(self) -> bool:
        """Проверяет видимость формы профиля."""
        return self.is_visible(self.locators.PROFILE_FORM)

    @allure.step("Проверить видимость истории заказов")
    def is_order_history_visible(self) -> bool:
        """Проверяет видимость раздела истории заказов."""
        return self.is_visible(self.locators.ORDER_HISTORY_SECTION)

    @allure.step("Получить все номера заказов")
    def get_all_order_numbers(self) -> list[str]:
        """Возвращает список всех номеров заказов в истории"""
        try:
            orders = self.find_elements(*self.locators.ORDERS)
            order_numbers = []
            for order in orders:
                number_element = order.find_element(
                    *self.locators.ORDER_NUMBER)
                order_numbers.append(number_element.text)
            return order_numbers

        except NoSuchElementException as e:
            self.logger.warning(f"Не найден элемент заказа: {str(e)}")
            return []
        except StaleElementReferenceException as e:
            self.logger.warning(f"Элемент заказа устарел: {str(e)}")
            return []
        except TimeoutException as e:
            self.logger.warning(f"Таймаут при поиске заказов: {str(e)}")
            return []
        except WebDriverException as e:
            self.logger.error(f"Ошибка WebDriver при получении заказов: {str(e)}")
            raise  # Пробрасываем критическую ошибку дальше

    @allure.step("Дождаться появления заказа в истории")
    def wait_for_order_in_history(self, order_number: str, timeout=10):
        """Ожидает появления указанного номера заказа в истории"""

        def order_present(_):
            try:
                orders = self.get_all_order_numbers()
                return any(order_number in num for num in orders)
            except (NoSuchElementException, StaleElementReferenceException):
                return False

        try:
            return self.get_wait(timeout).until(
                order_present,
                message=f"Заказ {order_number} не появился в истории"
            )
        except TimeoutException as e:
            self.logger.error(f"Заказ не появился в истории: {str(e)}")
            raise