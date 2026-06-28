# password_restore_page.py

import allure
from .base_page import BasePage
from locators.password_restore_locators import PasswordRestoreLocators


class PasswordRestorePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, url_suffix="forgot-password")
        self.locators = PasswordRestoreLocators()

    def _verify_page_loaded(self) -> None:
        """Проверка загрузки страницы восстановления"""
        self.url_should_contain("forgot-password")
        self.wait_until_visible(self.locators.PAGE_HEADER)
        self.wait_until_visible(self.locators.EMAIL_INPUT)

    @allure.step("Ввести email {email}")
    def enter_email(self, email: str) -> None:
        """Вводит email в поле восстановления пароля"""
        self.type_text(self.locators.EMAIL_INPUT, email)

    @allure.step("Нажать кнопку восстановления")
    def click_restore_button(self) -> None:
        """Кликает на кнопку восстановления пароля"""
        self.click(self.locators.RESTORE_BUTTON)

    @allure.step("Проверить активность кнопки восстановления")
    def is_restore_button_active(self) -> bool:
        """Проверяет, активна ли кнопка восстановления"""
        return self.is_clickable(self.locators.RESTORE_BUTTON)