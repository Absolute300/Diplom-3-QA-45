import allure
import pytest

from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage


def create_order_through_ui(driver, test_user):
    main_page = MainPage(driver)
    main_page.set_auth_tokens(test_user.access_token, test_user.refresh_token)
    main_page.add_basic_order_ingredients()
    return main_page.create_order()


@pytest.mark.ui
@allure.feature("Order feed")
class TestOrderFeed:
    @allure.story("Order counters")
    @allure.title("При создании заказа счетчик Выполнено за все время увеличивается")
    def test_total_orders_counter_increases_after_order_created(
        self, driver, test_user
    ):
        feed_page = OrderFeedPage(driver)
        feed_page.open_order_feed()
        old_total = feed_page.get_total_orders_count()

        create_order_through_ui(driver, test_user)
        feed_page.open_order_feed()

        assert feed_page.wait_total_counter_increased(old_total)

    @allure.story("Order counters")
    @allure.title("При создании заказа счетчик Выполнено за сегодня увеличивается")
    def test_today_orders_counter_increases_after_order_created(
        self, driver, test_user
    ):
        feed_page = OrderFeedPage(driver)
        feed_page.open_order_feed()
        old_today = feed_page.get_today_orders_count()

        create_order_through_ui(driver, test_user)
        feed_page.open_order_feed()

        assert feed_page.wait_today_counter_increased(old_today)

    @allure.feature("Order creation")
    @allure.story("Order status")
    @allure.title("После оформления заказа его номер появляется в разделе В работе")
    def test_created_order_number_appears_in_progress(self, driver, test_user):
        order_number = create_order_through_ui(driver, test_user)

        feed_page = OrderFeedPage(driver)
        feed_page.open_order_feed()

        assert feed_page.wait_order_in_progress(order_number)