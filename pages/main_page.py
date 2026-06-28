import allure
from selenium.common.exceptions import TimeoutException

from .base_page import BasePage
from locators.main_page_locators import MainPageLocators


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Клик на вкладку 'Конструктор'")
    def click_constructor_tab(self):
        self.click_element(MainPageLocators.CONSTRUCTOR_TAB)

    @allure.step("Клик на вкладку 'Лента заказов'")
    def click_order_feed_tab(self):
        self.click_element(MainPageLocators.ORDER_FEED_TAB)

    @allure.step("Клик на ингредиент: {ingredient_name}")
    def click_ingredient(self, ingredient_name):
        if ingredient_name == "traditional_sauce":
            self.click_element(MainPageLocators.TRADITIONAL_GALACTIC_SAUCE)

    @allure.step("Закрыть модальное окно ингредиента")
    def close_modal(self):
        self.click_element(MainPageLocators.MODAL_CLOSE)

    @allure.step("Проверить видимость модального окна ингредиента")
    def is_modal_visible(self):
        return self.is_element_visible(MainPageLocators.MODAL)

    @allure.step("Проверить закрытие модального окна ингредиента")
    def is_modal_closed(self):
        return self.is_element_not_visible(MainPageLocators.MODAL)

    @allure.step("Получить текст заголовка модального окна ингредиента")
    def get_modal_title(self):
        return self.get_element_text(MainPageLocators.MODAL_TITLE)

    @allure.step("Получить название ингредиента в модальном окне")
    def get_modal_ingredient_name(self):
        return self.get_element_text(MainPageLocators.MODAL_INGREDIENT_NAME)

    @allure.step("Получить значение счетчика ингредиента")
    def get_ingredient_counter_value(self, ingredient_name="traditional_sauce"):
        if ingredient_name == "traditional_sauce":
            counter_text = self.get_element_text_no_wait(MainPageLocators.TRADITIONAL_SAUCE_COUNTER)
            return int(counter_text) if counter_text else 0
        return 0

    @allure.step("Кликнуть на кнопку 'Войти в аккаунт'")
    def click_login_button(self):
         
        element = self.wait_for_element_clickable(MainPageLocators.LOGIN_BUTTON, timeout=15)
        self.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element = self.wait_for_element_clickable(MainPageLocators.LOGIN_BUTTON, timeout=15)
        self.execute_script("arguments[0].click();", element)

    @allure.step("Авторизоваться с email: {email}")
    def login(self, email, password):
        self.wait_for_element_visible(MainPageLocators.EMAIL_INPUT)
        self.input_text(MainPageLocators.EMAIL_INPUT, email)
        self.input_text(MainPageLocators.PASSWORD_INPUT, password)
        self.click_element(MainPageLocators.LOGIN_SUBMIT)

    @allure.step("Переключиться на раздел 'Соусы'")
    def switch_to_sauces_section(self):
        element = self.wait_for_element_clickable(MainPageLocators.SAUCE_TAB)
        self.click_element_via_js(element)

    @allure.step("Переключиться на раздел 'Булки'")
    def switch_to_buns_section(self):
        element = self.wait_for_element_clickable(MainPageLocators.BUN_TAB)
        self.click_element_via_js(element)

    @allure.step("Перетащить ингредиент в конструктор")
    def drag_ingredient_to_constructor(self, ingredient_name):
        if ingredient_name == "traditional_sauce":
            source_element = self.find_element_no_wait(MainPageLocators.TRADITIONAL_GALACTIC_SAUCE)
            target_element = self.find_element_no_wait(MainPageLocators.BASKET)
            self.drag_and_drop_react(source_element, target_element)

    @allure.step("Получить количество добавленных ингредиентов")
    def get_added_ingredients_count(self):
        elements = self.find_elements(MainPageLocators.CONSTRUCTOR_ELEMENT)
        return len(elements)

    @allure.step("Оформить заказ")
    def create_order(self):
        element = self.wait_for_element_clickable(MainPageLocators.ORDER_BUTTON)
        self.click_element_via_js(element)

    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self):
        """Закрытие модального окна заказа через JS клик для Firefox"""
        element = self.wait_for_element_clickable(MainPageLocators.ORDER_MODAL_CLOSE, timeout=10)
        self.click_element_via_js(element)

    @allure.step("Проверить видимость модального окна заказа")
    def is_order_modal_visible(self):
        return self.is_element_visible(MainPageLocators.ORDER_MODAL)

    @allure.step("Дождаться оформления заказа")
    def wait_for_order_creation(self, timeout=15):
        self.wait_for_element_visible(MainPageLocators.ORDER_MODAL, timeout)

    @allure.step("Проверить что пользователь авторизован")
    def is_authorized(self):
        return self.is_element_visible(MainPageLocators.ORDER_BUTTON)

    @allure.step("Получить номер заказа из модального окна")
    def get_order_number_from_modal(self):
        return self.get_element_text(MainPageLocators.ORDER_MODAL_NUMBER)

    @allure.step("Дождаться реального номера заказа")
    def wait_for_real_order_number(self, timeout=30):
        """Ожидает когда 9999 сменится на реальный номер"""
        condition = lambda driver: (
            self.get_order_number_from_modal() != "9999"
            and self.get_order_number_from_modal().isdigit()
            and len(self.get_order_number_from_modal()) > 3
        )

        try:
            self.wait_for_condition(condition, timeout, "реальный номер заказа")
            return self.get_order_number_from_modal()
        except TimeoutException:
            return self.get_order_number_from_modal()

    @allure.step("Дождаться скрытия модального окна заказа")
    def wait_for_order_modal_hidden(self, timeout=5):
        self.wait_element_invisible(MainPageLocators.ORDER_MODAL, timeout)

    @allure.step("Дождаться увеличения счетчика ингредиента")
    def wait_for_ingredient_counter_increase(self, ingredient_name, initial_value, timeout=10):
        """Ожидает увеличения счетчика ингредиента"""
        condition = lambda driver: (self.get_ingredient_counter_value(ingredient_name) > initial_value)
        self.wait_for_condition(condition, timeout, f"увеличения счетчика {ingredient_name}")

    @allure.step("Дождаться добавления ингредиентов")
    def wait_for_ingredients_added(self, min_count=1, timeout=10):
        """Ожидает добавления минимум min_count ингредиентов"""
        condition = lambda driver: (self.get_added_ingredients_count() >= min_count)
        self.wait_for_condition(condition, timeout, f"добавления минимум {min_count} ингредиентов")

    @allure.step("Получить элемент булки по тексту")
    def get_bun_element_by_text(self, text="булка"):
        """Находит элемент булки по тексту (для динамических локаторов)"""
        from selenium.webdriver.common.by import By

        xpath = f"//p[contains(text(), '{text}')]"
        return self.driver.find_element(By.XPATH, xpath)

    @allure.step("Дождаться полного закрытия модалки (фикс для Firefox)")
    def wait_for_modal_completely_hidden_for_firefox(self, timeout=10):
        """Ожидает пока overlay модального окна полностью скроется (для Firefox)"""
        self.wait_element_invisible(MainPageLocators.MODAL, timeout)

    @allure.step("Добавить булку в конструктор (краторная)")
    def add_bun_to_constructor(self):
        bun = self.wait_for_element_visible(MainPageLocators.BUN_STELLAR_CRUST, timeout=15)
        basket = self.wait_for_element_visible(MainPageLocators.BASKET, timeout=15)
        self.drag_and_drop_react(bun, basket)

    @allure.step("Добавить соус в конструктор (традиционный)")
    def add_traditional_sauce_to_constructor(self):
        sauce = self.wait_for_element_visible(MainPageLocators.TRADITIONAL_GALACTIC_SAUCE, timeout=15)
        basket = self.wait_for_element_visible(MainPageLocators.BASKET, timeout=15)
        self.drag_and_drop_react(sauce, basket)

    @allure.step("Собрать заказ (булка + соус)")
    def build_order_bun_and_sauce(self):
        self.add_bun_to_constructor()
        self.add_traditional_sauce_to_constructor()
        self.wait_for_ingredients_added(min_count=2, timeout=15)