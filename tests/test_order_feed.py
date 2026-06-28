import allure

from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from config import Config


class TestOrderFeed:
    """
    Тесты для ленты заказов
    """

    @allure.title("Счетчик 'Выполнено за всё время' увеличивается при новом заказе")
    def test_total_orders_counter_increases(self, driver):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)

        with allure.step("1. Получаем изначальное значение счетчика"):
            order_feed_page.open_order_feed()
            order_feed_page.wait_for_total_counter_visible()
            total_before = order_feed_page.get_total_orders_count()

        with allure.step("2. Создаем заказ (авторизация и ингредиенты)"):
            main_page.open("/")
            main_page.click_login_button()
            main_page.login(Config.TEST_EMAIL, Config.TEST_PASSWORD)
            assert main_page.is_authorized(), "Авторизация не прошла"

            main_page.build_order_bun_and_sauce()

            added_count = main_page.get_added_ingredients_count()
            assert added_count >= 2, f"Ингредиенты не добавлены. Добавлено: {added_count}"

            main_page.create_order()

        with allure.step("3. Дождаться модального окна с номером заказа"):
            main_page.wait_for_order_creation(timeout=15)
            order_number = main_page.wait_for_real_order_number(timeout=30)
            assert order_number != "9999", f"Заказ не создан. Номер: {order_number}"

            main_page.close_order_modal()
            main_page.wait_for_order_modal_hidden(timeout=5)

        with allure.step("4. Дождаться обновления счетчика и проверить увеличение"):
            order_feed_page.open_order_feed()
            order_feed_page.wait_for_total_counter_visible()
            order_feed_page.wait_for_counters_update(previous_total_count=total_before, timeout=30)

            total_after = order_feed_page.get_total_orders_count()
            assert total_after > total_before, (
                f"Счетчик не увеличился: было {total_before}, стало {total_after}"
            )

    @allure.title("Счетчик 'Выполнено за сегодня' увеличивается при новом заказе")
    def test_today_orders_counter_increases(self, driver):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)

        with allure.step("1. Получаем начальное значение счетчика"):
            order_feed_page.open_order_feed()
            order_feed_page.wait_for_today_counter_visible()
            today_before = order_feed_page.get_today_orders_count()

        with allure.step("2. Создаем заказ (авторизация и ингредиенты)"):
            main_page.open("/")
            main_page.click_login_button()
            main_page.login(Config.TEST_EMAIL, Config.TEST_PASSWORD)
            assert main_page.is_authorized(), "Авторизация не прошла"

            main_page.build_order_bun_and_sauce()
            main_page.create_order()

        with allure.step("3. Дождаться номера заказа"):
            main_page.wait_for_order_creation(timeout=15)
            order_number = main_page.wait_for_real_order_number(timeout=30)
            assert order_number != "9999", f"Заказ не создан. Номер: {order_number}"

            main_page.close_order_modal()
            main_page.wait_for_order_modal_hidden(timeout=5)

        with allure.step("4. Дождаться обновления счетчика за сегодня и проверить увеличение"):
            order_feed_page.open_order_feed()
            order_feed_page.wait_for_today_counter_visible()

            order_feed_page.wait_for_condition(
                lambda d: order_feed_page.get_today_orders_count() > today_before,
                timeout=30,
                condition_name="увеличение счетчика 'Выполнено за сегодня'",
            )

            today_after = order_feed_page.get_today_orders_count()
            assert today_after > today_before, (
                f"Счетчик не увеличился: было {today_before}, стало {today_after}"
            )

    @allure.title("Новый заказ отражается в разделе 'В работе'")
    def test_order_appears_in_progress_section(self, driver):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)

        with allure.step("1. Получаем текущие заказы в работе"):
            order_feed_page.open_order_feed()
            order_feed_page.wait_for_in_progress_section_visible()
            existing_orders = order_feed_page.get_orders_in_progress_numbers()

        with allure.step("2. Создаем заказ"):
            main_page.open("/")
            main_page.click_login_button()
            main_page.login(Config.TEST_EMAIL, Config.TEST_PASSWORD)
            assert main_page.is_authorized(), "Авторизация не прошла"

            main_page.build_order_bun_and_sauce()
            main_page.create_order()

        with allure.step("3. Дождаться номера заказа"):
            main_page.wait_for_order_creation(timeout=15)
            order_number = main_page.wait_for_real_order_number(timeout=30)
            assert order_number != "9999", f"Заказ не создан. Номер: {order_number}"

            main_page.close_order_modal()
            main_page.wait_for_order_modal_hidden(timeout=5)

        with allure.step("4. Проверяем что заказ появился в 'В работе'"):
            order_feed_page.open_order_feed()
            order_feed_page.wait_for_in_progress_section_visible()

            current_orders = order_feed_page.get_orders_in_progress_numbers()

            order_num_clean = order_number.lstrip("0")
            current_orders_clean = [order.lstrip("0") for order in current_orders]

            assert order_num_clean in current_orders_clean, (
                f"Заказ {order_number} не найден в 'В работе'. "
                f"Было: {existing_orders}, стало: {current_orders}"
            )