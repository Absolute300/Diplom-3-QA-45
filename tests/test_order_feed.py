# test_order_feed.py

import allure
import logging

logger = logging.getLogger(__name__)

@allure.feature("Лента заказов")
class TestOrderFeed:
    @allure.title("Открытие деталей заказа из ленты")
    def test_open_order_details_modal(self, authenticated_user, main_page, order_feed_page):
        with allure.step("Подготовка: создать тестовый заказ"):
            main_page.add_ingredient_to_constructor()
            main_page.make_order()
            main_page.close_modal()

        with allure.step("Действие: перейти в ленту заказов и открыть детали"):
            main_page.navigate_to_order_feed()
            order_feed_page.click_first_order()

        with allure.step("Проверка: модальное окно с деталями отображается"):
            assert order_feed_page.is_order_modal_visible()

    @allure.title("Заказ отображается в истории заказов")
    def test_order_appears_in_history(self, authenticated_user, main_page, profile_page):
        with allure.step("Подготовка: создать тестовый заказ"):
            main_page.add_ingredient_to_constructor()
            order_number = main_page.make_order()
            main_page.close_modal()
            assert order_number, "Номер заказа не получен"

        with allure.step("Действие: перейти в историю заказов"):
            main_page.go_to_personal_account()
            profile_page.click_order_history_link()

        with allure.step("Проверка: заказ есть в истории"):
            assert profile_page.wait_for_order_in_history(order_number), \
                f"Заказ {order_number} не найден в истории"

    @allure.title("Счетчик 'Выполнено за все время' увеличивается")
    def test_total_orders_counter_increases(self, authenticated_user, main_page, order_feed_page):
        with allure.step("1. Получить начальное значение счетчика 'Выполнено за все время'"):
            order_feed_page.open()
            initial_count = order_feed_page.get_validated_counter_value()

        with allure.step("2. Открыть страницу конструктора и убедиться в авторизации"):
            main_page.open()
            assert main_page.is_user_logged_in(), "Пользователь не авторизован или страница не готова"

        with allure.step("3. Создать тестовый заказ"):
            order_number = main_page.create_test_order()
            assert order_number, "Номер заказа не получен"

        with allure.step(
                "4. Обновить страницу ленты заказов и получить новое значение счетчика 'Выполнено за все время'"):
            order_feed_page.open()  # Обновляем страницу, чтобы обновить счетчик
            new_count = order_feed_page.get_validated_counter_value()

        with allure.step("5. Проверить, что счетчик 'Выполнено за все время' увеличился"):
            assert new_count > initial_count, f"Счетчик 'Выполнено за все время' не увеличился: \
            было {initial_count}, стало {new_count}"

    @allure.title("Счетчик 'Выполнено за сегодня' увеличивается")
    def test_today_orders_counter_increases(self, authenticated_user, main_page, order_feed_page):
        with allure.step("1. Получить начальное значение счетчика 'Выполнено за сегодня'"):
            order_feed_page.open()
            initial_today = order_feed_page.get_today_orders_count()

        with allure.step("2. Открыть страницу конструктора и убедиться в авторизации"):
            main_page.open()
            assert main_page.is_user_logged_in(), "Пользователь не авторизован или страница не готова"

        with allure.step("3. Создать новый заказ"):
            order_number = main_page.create_test_order()
            assert order_number, "Номер заказа не получен"

        with allure.step(
                "4. Обновить страницу ленты заказов и получить новое значение счетчика 'Выполнено за сегодня'"):
            order_feed_page.open()
            new_today = order_feed_page.get_today_orders_count()

        with allure.step("5. Проверить, что счетчик 'Выполнено за сегодня' увеличился"):
            assert new_today > initial_today, f"Счетчик 'Выполнено за сегодня' не увеличился: \
            было {initial_today}, стало {new_today}"

    @allure.title("Заказ появляется в разделе 'В работе'")
    def test_order_appears_in_progress(self, authenticated_user, main_page, order_feed_page):
        with allure.step("1. Создать новый тестовый заказ"):
            order_number = main_page.create_test_order()
            allure.attach(f"Номер созданного заказа: {order_number}", name="Order Number")
            assert order_number, "Не удалось получить номер заказа"

        with allure.step("2. Перейти в ленту заказов"):
            order_feed_page.open()

        with allure.step("3. Проверить появление заказа в системе"):
            assert order_feed_page.is_order_in_system(order_number), \
                f"Заказ {order_number} не отображается в системе"

        with allure.step("4. Проверить статус заказа"):
            assert order_feed_page.is_order_in_progress(order_number), \
                f"Заказ {order_number} не появился в разделе 'В работе'"