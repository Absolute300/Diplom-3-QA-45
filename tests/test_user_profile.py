# test_user_profile.py

import allure
from pages.main_page import MainPage
from pages.profile_page import ProfilePage
from pages.login_page import LoginPage
from config import config


@allure.feature("Личный кабинет")
class TestUserProfile:
    @allure.title("Переход в личный кабинет")
    def test_navigate_to_personal_account(self, driver, authenticated_user):
        main_page = MainPage(driver)
        profile_page = ProfilePage(driver)

        with allure.step("Переход в личный кабинет с главной страницы"):
            main_page.go_to_personal_account()

        with allure.step("Проверка загрузки страницы профиля"):
            assert profile_page.is_profile_form_visible(), "Форма профиля не отображается"
            assert profile_page.get_current_url() == config.PROFILE_URL, "URL не соответствует странице профиля"

    @allure.title("Переход в историю заказов")
    def test_navigate_to_order_history(self, driver, authenticated_user):
        main_page = MainPage(driver)
        profile_page = ProfilePage(driver)

        with allure.step("Переход в личный кабинет с главной страницы"):
            main_page.go_to_personal_account()

        with allure.step("Переход в историю заказов"):
            profile_page.click_order_history_link()

        with allure.step("Проверка перехода на страницу истории"):
            assert profile_page.get_current_url() == config.ORDER_HISTORY_URL, \
                "URL не соответствует странице истории заказов"

    @allure.title("Выход из аккаунта")
    def test_logout(self, driver, authenticated_user):
        main_page = MainPage(driver)
        profile_page = ProfilePage(driver)
        login_page = LoginPage(driver)

        with allure.step("Переход в личный кабинет с главной страницы"):
            main_page.go_to_personal_account()

        with allure.step("Выход из аккаунта"):
            profile_page.logout()

        with allure.step("Проверка перехода на страницу входа"):
            assert login_page.get_current_url() == config.LOGIN_URL, "URL не соответствует странице входа"
            assert login_page.is_login_form_visible(), "Форма входа не отображается"