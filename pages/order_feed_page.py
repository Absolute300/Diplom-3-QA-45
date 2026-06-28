import allure
from selenium.common.exceptions import TimeoutException

from helpers import normalize_order_number, parse_int
from locators.order_feed_locators import OrderFeedLocators
from pages.base_page import BasePage
from urls import ORDER_FEED_URL


class OrderFeedPage(BasePage):
    @allure.step("Open order feed")
    def open_order_feed(self):
        self.open(ORDER_FEED_URL)
        self.wait_feed_loaded_with_retry()

    @allure.step("Wait for order feed content")
    def wait_feed_loaded_with_retry(self):
        for attempt in range(2):
            try:
                self.wait_visible(OrderFeedLocators.ORDER_FEED_ROOT, timeout=90)
                self.wait_visible(OrderFeedLocators.ORDERS_DATA, timeout=90)
                self.wait_visible(OrderFeedLocators.TOTAL_COUNTER, timeout=90)
                return
            except TimeoutException:
                if attempt == 1:
                    raise
                self.driver.refresh()

    @allure.step("Get total orders count")
    def get_total_orders_count(self):
        return parse_int(self.get_text(OrderFeedLocators.TOTAL_COUNTER))

    @allure.step("Get today orders count")
    def get_today_orders_count(self):
        return parse_int(self.get_text(OrderFeedLocators.TODAY_COUNTER))

    @allure.step("Get orders in progress")
    def get_orders_in_progress(self):
        orders = []
        for order in self.find_elements(OrderFeedLocators.IN_PROGRESS_ORDERS):
            text = order.text.strip()
            if any(char.isdigit() for char in text):
                orders.append(normalize_order_number(text))
        return orders

    @allure.step("Check order number is in progress")
    def is_order_number_in_progress(self, order_number):
        return normalize_order_number(order_number) in self.get_orders_in_progress()

    @allure.step("Wait total orders counter increased")
    def wait_total_counter_increased(self, old_value):
        return self.wait_until(lambda _: self.get_total_orders_count() > old_value, 90)

    @allure.step("Wait today orders counter increased")
    def wait_today_counter_increased(self, old_value):
        return self.wait_until(lambda _: self.get_today_orders_count() > old_value, 90)

    @allure.step("Wait order appears in progress")
    def wait_order_in_progress(self, order_number):
        return self.wait_until(
            lambda _: self.is_order_number_in_progress(order_number),
            timeout=90,
        )