# modal_locators.py

from selenium.webdriver.common.by import By

class ModalLocators:
    # Общие для всех страниц модальные окна
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_overlay')]")
    MODAL_WINDOW = (By.XPATH, "//div[contains(@class, 'Modal_modal__container')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
    ORDER_DETAILS_MODAL = (By.XPATH, "//div[contains(@class, 'OrderDetails_modal')]")