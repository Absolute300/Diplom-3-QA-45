from selenium.webdriver.common.by import By


class OrderFeedLocators:
    ORDER_FEED_ROOT = (By.CSS_SELECTOR, "div[class*='OrderFeed_orderFeed']")
    ORDER_FEED_TITLE = (By.XPATH, "//h1[normalize-space()='Лента заказов']")
    ORDER_CARDS = (By.CSS_SELECTOR, "ul[class*='OrderFeed_list'] li[class*='OrderHistory_listItem']")
    ORDERS_DATA = (By.CSS_SELECTOR, "div[class*='OrderFeed_ordersData']")
    TOTAL_COUNTER = (
        By.XPATH,
        "//p[normalize-space()='Выполнено за все время:']/following-sibling::p[contains(@class,'OrderFeed_number')]",
    )
    TODAY_COUNTER = (
        By.XPATH,
        "//p[normalize-space()='Выполнено за сегодня:']/following-sibling::p[contains(@class,'OrderFeed_number')]",
    )
    IN_PROGRESS_ORDERS = (By.CSS_SELECTOR, "ul[class*='OrderFeed_orderListReady'] li")