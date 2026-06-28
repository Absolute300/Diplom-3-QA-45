from selenium.webdriver.common.by import By

class OrderFeedLocators:
    """Локаторы для страницы ленты заказов"""
    
    TOTAL_ORDERS_COUNT = (By.XPATH, "//p[contains(@class, 'digits-large')]")
    TODAY_ORDERS_COUNT = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня:')]/following-sibling::p")

    ORDERS_IN_PROGRESS_SECTION = (By.XPATH, "//p[contains(text(), 'В работе:')]/..")
    ORDER_NUMBERS_IN_PROGRESS = (By.XPATH, "//p[contains(text(), 'В работе:')]/../ul/li")

    ORDERS_READY_SECTION = (By.CSS_SELECTOR, ".OrderFeed_orderListReady__lYFem")
    ORDER_NUMBERS_READY = (By.XPATH, "//p[contains(text(), 'Готовы:')]/../ul/li")
    ORDER_NUMBERS_IN_PROGRESS = (By.XPATH, "//p[contains(text(), 'В работе:')]/following-sibling::ul/li")