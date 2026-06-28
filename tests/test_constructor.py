# test_constructor.py

import allure
from pages.main_page import MainPage
from pages.register_page import RegisterPage
from pages.order_feed_page import OrderFeedPage
from config import config


@allure.feature("Основной функционал")
class TestConstructor:
    @allure.title("Переход в конструктор по клику на 'Конструктор'")
    def test_navigate_to_constructor_from_register_page(self, driver):
        register_page = RegisterPage(driver)
        main_page = MainPage(driver)

        with allure.step("1. Открыть страницу регистрации"):
            register_page.open()
            assert register_page.get_current_page_url().rstrip('/') == config.REGISTER_URL.rstrip('/')

        with allure.step("2. Нажать на ссылку 'Конструктор' в хедере"):
            register_page.click_constructor_link()

        with allure.step("3. Проверить переход на главную страницу"):
            assert main_page.get_current_page_url().rstrip('/') == config.MAIN_PAGE_URL.rstrip('/')
            assert main_page.is_ingredients_section_visible()

    @allure.title("Переход в ленту заказов по клику на 'Лента заказов'")
    def test_navigate_to_order_feed(self, driver):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)

        with allure.step("1. Открыть главную страницу"):
            main_page.open()
            assert main_page.get_current_page_url().rstrip('/') == config.MAIN_PAGE_URL.rstrip('/')

        with allure.step("2. Нажать на ссылку 'Лента заказов'"):
            main_page.navigate_to_order_feed()

        with allure.step("3. Проверить переход в ленту заказов"):
            assert order_feed_page.get_current_page_url().rstrip('/') == config.ORDER_FEED_URL.rstrip('/')
            assert order_feed_page.is_page_header_visible()  # Используем метод страницы

    @allure.title("Открытие модального окна с деталями ингредиента")
    def test_ingredient_modal_open(self, driver):
        main_page = MainPage(driver)

        with allure.step("1. Открыть главную страницу"):
            main_page.open()

        with allure.step("2. Кликнуть на ингредиент"):
            main_page.click_ingredient()

        with allure.step("3. Проверить открытие модального окна"):
            assert main_page.is_ingredient_modal_visible()

    @allure.title("Закрытие модального окна с деталями ингредиента")
    def test_ingredient_modal_close(self, driver):
        main_page = MainPage(driver)

        with allure.step("1. Открыть главную страницу"):
            main_page.open()

        with allure.step("2. Кликнуть на ингредиент"):
            main_page.click_ingredient()

        with allure.step("3. Проверить открытие модального окна"):
            assert main_page.is_ingredient_modal_visible()

        with allure.step("4. Закрыть модальное окно"):
            main_page.close_ingredient_modal()

        with allure.step("5. Проверить закрытие модального окна"):
            assert not main_page.is_ingredient_modal_visible()

    @allure.title("Увеличение счетчика ингредиента при добавлении")
    def test_ingredient_counter_increase(self, driver):
        main_page = MainPage(driver)

        with allure.step("1. Открыть главную страницу"):
            main_page.open()

        with allure.step("2. Получить начальное значение счетчика"):
            initial_counter = main_page.get_ingredient_counter_value()

        with allure.step("3. Увеличить счетчик ингредиентов"):
            main_page.increase_ingredient_counter()

        with allure.step("4. Проверить увеличение счетчика"):
            assert main_page.get_ingredient_counter_value() == initial_counter + 2

    @allure.title("Оформление заказа авторизованным пользователем")
    def test_make_order_authenticated(self, driver, authenticated_user, main_page):

        with allure.step("1. Открыть главную страницу"):
            main_page.open()

        with allure.step("2. Добавить ингредиент в конструктор"):
            main_page.add_ingredient_to_constructor()  # Используем метод страницы

        with allure.step("3. Оформить заказ"):
            order_number = main_page.make_order()

        with allure.step("4. Проверить наличие номера заказа"):
            assert order_number.isdigit(), "Номер заказа должен быть числом"