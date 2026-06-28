# order_feed_locators.py

from selenium.webdriver.common.by import By

class OrderFeedLocators:
    # Уникальные элементы ленты заказов
    PAGE_HEADER = (By.XPATH, "//h1[contains(@class, 'text_type_main-large') and contains(text(), 'Лента заказов')]")
    ORDER_ITEM = (By.XPATH, "//div[contains(@class, 'OrderHistory_link')]")
    ORDER_NUMBER = (By.XPATH, ".//p[contains(@class, 'text_type_digits-default')]")
    TOTAL_ORDERS_COUNT = (
        By.XPATH,
        "//div[p[text()='Выполнено за все время:']]/p[contains(@class, 'OrderFeed_number__2MbrQ')]"
    )

    TODAY_ORDERS_COUNT = (
        By.XPATH,
        "//div[p[text()='Выполнено за сегодня:']]/p[contains(@class, 'OrderFeed_number__2MbrQ')]"
    )
    ORDERS_IN_PROGRESS = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady')]/li")
    ORDER_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_orderBox')]")
    MODAL_ORDER_NUMBER = (By.XPATH, "//h2[contains(@class, 'text_type_digits-large')]")
    FIRST_ORDER_NUMBER = (By.CSS_SELECTOR, "a.OrderHistory_link__1iNby")

    ORDERS_IN_PROGRESS_SECTION = (By.XPATH, "//div[contains(text(), 'В работе:')]/..")
    ORDER_NUMBER_IN_PROGRESS = (By.CSS_SELECTOR, "ul.OrderFeed_orderListReady__1YFem li.text_type_digits-default")
    NO_ORDERS_MESSAGE = (By.CSS_SELECTOR, "ul.OrderFeed_orderListReady__1YFem li.text_type_main-small")

    IN_PROGRESS_SECTION = (By.XPATH, "//div[contains(text(), 'В работе:')]/following-sibling::ul")
    ALL_ORDERS_READY_TEXT = "Все текущие заказы готовы!"

    # Раздел "В работе"
    IN_PROGRESS_TITLE = (By.XPATH, ".//p[contains(@class, 'text_type_main-medium') and contains(text(), 'В работе:')]")
    IN_PROGRESS_CONTAINER = (By.CSS_SELECTOR, "ul.OrderFeed_orderListReady__1YFem")
    IN_PROGRESS_ORDER_NUMBERS = (
        By.XPATH,
        "//p[contains(text(), 'В работе:')]/following-sibling::ul[contains(@class, 'OrderFeed_orderListReady')]//li[contains(@class, 'text_type_digits-default')]"
    )
    ALL_ORDERS_READY_MSG = (
        By.XPATH,
        "//p[contains(text(), 'В работе:')]/following-sibling::ul[contains(@class, 'OrderFeed_orderListReady')]//li[contains(text(), 'Все текущие заказы готовы!')]"
    )
    ORDER_STATUS_BOX = (By.CSS_SELECTOR, "div.OrderFeed_orderStatusBox__1d4q2")
    IN_PROGRESS_LIST = (By.CSS_SELECTOR, "ul.OrderFeed_orderListReady__1YFem")