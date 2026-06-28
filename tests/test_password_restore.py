# test_password_restore.py

import allure
from pages.login_page import LoginPage
from pages.password_restore_page import PasswordRestorePage
from config import config


@allure.feature("Восстановление пароля")
class TestPasswordRestore:
    @allure.title("Переход на страницу восстановления пароля")
    def test_go_to_password_restore_page(self, driver):
        login_page = LoginPage(driver)
        password_restore_page = PasswordRestorePage(driver)

        with allure.step("1. Открыть страницу входа"):
            login_page.open()
            assert login_page.get_current_url() == config.LOGIN_URL

        with allure.step("2. Перейти на страницу восстановления пароля"):
            login_page.click(login_page.locators.RESTORE_PASSWORD_LINK)

        with allure.step("3. Проверить загрузку страницы восстановления"):
            assert password_restore_page.get_current_url() == config.FORGOT_PASSWORD_URL
            assert password_restore_page.is_visible(password_restore_page.locators.PAGE_HEADER)

    @allure.title("Ввод почты и клик по кнопке 'Восстановить'")
    def test_restore_password_flow(self, driver, test_user):
        login_page = LoginPage(driver)
        password_restore_page = PasswordRestorePage(driver)

        with allure.step("Подготовка: открыть страницу восстановления"):
            login_page.open()
            login_page.click(login_page.locators.RESTORE_PASSWORD_LINK)

        with allure.step("Заполнить и отправить форму восстановления"):
            password_restore_page.type_text(
                password_restore_page.locators.EMAIL_INPUT,
                test_user["email"]
            )
            password_restore_page.click(
                password_restore_page.locators.RESTORE_BUTTON
            )

        with allure.step("Проверить переход на страницу сброса пароля"):
            password_restore_page.wait_until_url_contains("reset-password")
            assert password_restore_page.get_current_url() == config.RESET_PASSWORD_URL

    @allure.title("Проверка подсветки поля пароля")
    def test_password_field_highlight(self, driver):
        login_page = LoginPage(driver)

        with allure.step("Открыть страницу логина"):
            login_page.open()

        with allure.step("Проверить начальное состояние поля"):
            assert not login_page.is_password_field_highlighted()

        with allure.step("Нажать иконку видимости пароля"):
            login_page.click(login_page.locators.SHOW_PASSWORD_BUTTON)

        with allure.step("Проверить подсветку поля после клика"):
            assert login_page.is_password_field_highlighted()