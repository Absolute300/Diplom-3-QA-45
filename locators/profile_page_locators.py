# profile_page_locators.py

from selenium.webdriver.common.by import By

class ProfilePageLocators:
    # Уникальные элементы профиля
    PROFILE_FORM = (By.XPATH, "//div[@class='Profile_profile__3dzvr']")
    NAME_INPUT = (By.XPATH, "//input[@name='name']")
    EMAIL_INPUT = (By.XPATH, "//input[@name='email']")
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(), 'Сохранить')]")
    ORDER_HISTORY_LINK = (By.XPATH, "//a[contains(@href, 'order-history')]")
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Выход')]")
    ORDER_HISTORY_SECTION = (By.XPATH, "//section[contains(@class, 'OrderHistory')]")
    ORDER_HISTORY_ITEM = (By.XPATH, "//div[contains(@class, 'OrderHistory_link')]")
    ORDER_HISTORY_NUMBER = (By.XPATH, ".//p[contains(@class, 'text_type_digits-default')]")
    # локатор всех заказов (ссылок)
    ORDERS = (By.CSS_SELECTOR, "a.OrderHistory_link__1iNby")
    # локатор номера заказа внутри одного заказа
    ORDER_NUMBER = (By.CSS_SELECTOR, "p.text_type_digits-default")