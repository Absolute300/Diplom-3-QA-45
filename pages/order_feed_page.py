import allure
from .base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators


class OrderFeedPage(BasePage):
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/feed"
    
    @allure.step("Открыть страницу ленты заказов")
    def open_order_feed(self):
        self.open(self.url)
    
    @allure.step("Получить счетчик 'Выполнено за всё время'")
    def get_total_orders_count(self):
        count_text = self.get_element_text(OrderFeedLocators.TOTAL_ORDERS_COUNT)
        return int(count_text)
    
    @allure.step("Получить счетчик 'Выполнено за сегодня'")
    def get_today_orders_count(self):
        count_text = self.get_element_text(OrderFeedLocators.TODAY_ORDERS_COUNT)
        return int(count_text)
    
    @allure.step("Проверить есть ли заказы в работе")
    def has_orders_in_progress(self):
        elements = self.find_elements(OrderFeedLocators.ORDER_NUMBERS_IN_PROGRESS)
        if not elements:
            return False

        text = elements[0].text.strip()

        if "Все текущие заказы готовы" in text:
            return False

        return text.isdigit()
    
    @allure.step("Получить количество заказов в работе")
    def get_orders_in_progress_count(self):
        if not self.has_orders_in_progress():
            return 0
        
        elements = self.find_elements(OrderFeedLocators.ORDER_NUMBERS_IN_PROGRESS)
        count = 0
        for element in elements:
            if element.text.strip().isdigit():
                count += 1
        return count
    
    @allure.step("Получить номера заказов в работе")
    def get_orders_in_progress_numbers(self):
        if not self.has_orders_in_progress():
            return []
        
        elements = self.find_elements(OrderFeedLocators.ORDER_NUMBERS_IN_PROGRESS)
        orders = []
        for element in elements:
            text = element.text.strip()
            if text.isdigit():
                orders.append(text)
        return orders
    
    @allure.step("Проверить что раздел 'В работе' отображается")
    def is_orders_in_progress_visible(self):
        return self.is_element_visible(OrderFeedLocators.ORDERS_IN_PROGRESS_SECTION)
    
    @allure.step("Дождаться обновления счетчиков")
    def wait_for_counters_update(self, previous_total_count, timeout=30):
        """Ожидает пока счетчики обновятся"""
        condition = lambda driver: self.get_total_orders_count() > previous_total_count
        return self.wait_for_condition(condition, timeout, "обновления счетчиков")
    
    @allure.step("Дождаться видимости счетчика 'Выполнено за всё время'")
    def wait_for_total_counter_visible(self, timeout=10):
        self.wait_for_element_visible(OrderFeedLocators.TOTAL_ORDERS_COUNT, timeout)
    
    @allure.step("Дождаться видимости счетчика 'Выполнено за сегодня'")
    def wait_for_today_counter_visible(self, timeout=10):
        self.wait_for_element_visible(OrderFeedLocators.TODAY_ORDERS_COUNT, timeout)
    
    @allure.step("Дождаться видимости раздела 'В работе'")
    def wait_for_in_progress_section_visible(self, timeout=10):
        self.wait_for_element_visible((OrderFeedLocators.ORDERS_IN_PROGRESS_SECTION), timeout)
    
    @allure.step("Получить текст элемента 'В работе:'")
    def get_in_progress_section_text(self):
        return self.get_element_text(OrderFeedLocators.ORDERS_IN_PROGRESS_SECTION)