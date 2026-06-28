# register_page.py

import allure
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from .base_page import BasePage
from locators.register_page_locators import RegisterPageLocators

logger = logging.getLogger(__name__)

class RegisterPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver, "register")
        self.locators = RegisterPageLocators()

    def _verify_page_loaded(self):
        """Проверка загрузки страницы регистрации"""
        self.wait_until_visible(self.locators.REGISTER_FORM)
        self.wait_until_visible(self.locators.NAME_INPUT)
        self.wait_until_visible(self.locators.EMAIL_INPUT)
        self.wait_until_visible(self.locators.PASSWORD_INPUT)

    @allure.step("Открыть страницу регистрации")
    def open(self) -> None:
        """Открывает страницу регистрации и проверяет её загрузку."""
        super().open()

    def register(self, name: str, email: str, password: str):
        self.type_text(self.locators.NAME_INPUT, name)
        self.type_text(self.locators.EMAIL_INPUT, email)
        self.type_text(self.locators.PASSWORD_INPUT, password)
        self.click(self.locators.REGISTER_BUTTON)

        # Добавляем явное ожидание
        try:
            self.wait_until_url_contains("login", timeout=15)
        except TimeoutException:
            current_url = self.driver.current_url
            if "register" in current_url:
                error = self.get_text(self.locators.ERROR_MESSAGE)
                raise AssertionError(f"Регистрация не удалась. Ошибка: {error}")
            raise

    @allure.step("Проверить сообщение об ошибке")
    def is_error_message_displayed(self, expected_message: str) -> bool:
        """Проверить сообщение об ошибке."""
        try:
            error_text = self.get_text(self.locators.ERROR_MESSAGE)
            return expected_message in error_text
        except NoSuchElementException:
            logger.debug("Элемент с сообщением об ошибке не найден")
            return False
        except TimeoutException:
            logger.debug("Таймаут при ожидании сообщения об ошибке")
            return False

    @allure.step("Перейти на страницу входа")
    def go_to_login_page(self) -> None:
        """Переходит на страницу входа в систему."""
        self.click(self.locators.LOGIN_LINK)
        self.wait_until_url_contains("login")

    @allure.step("Нажать на ссылку 'Конструктор'")
    def click_constructor_link(self):
        """Кликает на ссылку 'Конструктор' в хедере"""
        self.click(self.locators.CONSTRUCTOR_LINK)

    @allure.step("Проверить, что мы на странице регистрации")
    def is_register_page(self) -> bool:
        """Проверить, что мы на странице регистрации."""
        return self.url_should_contain("register") and self.is_visible(self.locators.REGISTER_FORM)

    @allure.step("Получить текущий URL")
    def get_current_page_url(self) -> str:
        """Возвращает текущий URL страницы."""
        return self.get_current_url()