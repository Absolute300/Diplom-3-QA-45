# main_page.py

import allure
import logging
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from .base_page import BasePage
from locators.main_page_locators import MainPageLocators
from locators.modal_locators import ModalLocators
from config import config

logger = logging.getLogger(__name__)


class MainPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver, url_suffix="")
        self.locators = MainPageLocators()
        self.modal_locators = ModalLocators()
        self.logger = logging.getLogger(__name__)

    @allure.step("Открыть главную страницу")
    def open(self) -> None:
        """Открывает главную страницу и проверяет её загрузку."""
        super().open()
        self._verify_page_loaded()

    def _verify_page_loaded(self) -> None:
        """Внутренний метод для проверки загрузки страницы."""
        self.wait_until_visible(self.locators.INGREDIENTS_SECTION)
        self.wait_until_visible(self.locators.CONSTRUCTOR_AREA)

    @allure.step("Проверить видимость раздела ингредиентов")
    def is_ingredients_section_visible(self) -> bool:
        """Проверяет видимость секции с ингредиентами."""
        return self.is_visible(self.locators.INGREDIENTS_SECTION)

    @allure.step("Кликнуть на ингредиент")
    def click_ingredient(self) -> None:
        """Кликает на первый доступный ингредиент."""
        self.click(self.locators.INGREDIENT_ITEM)
        self.wait_until_visible(self.modal_locators.MODAL_WINDOW)

    @allure.step("Проверить, что пользователь авторизован")
    def is_user_logged_in(self, timeout=None) -> bool:
        """Проверяет, что пользователь авторизован."""
        timeout = timeout or self.timeout
        try:
            return self.is_visible(self.locators.CREATE_ORDER_BTN, timeout=timeout)
        except TimeoutException:
            return False

    @allure.step("Проверить состояние модального окна")
    def is_modal_visible(self, timeout=None) -> bool:
        """Проверяет видимость модального окна."""
        timeout = timeout or self.timeout
        return self.is_visible(self.modal_locators.MODAL_WINDOW, timeout=timeout)

    @allure.step("Закрыть модальное окно")
    def close_modal(self, timeout=None) -> None:
        """Закрывает модальное окно."""
        timeout = timeout or self.timeout
        if self.is_modal_visible(timeout=timeout):
            self.click(self.modal_locators.MODAL_CLOSE_BUTTON, timeout=timeout)
            self.wait_until_not_visible(self.modal_locators.MODAL_WINDOW, timeout=timeout)

    @allure.step("Перейти в конструктор")
    def navigate_to_constructor(self) -> None:
        """Переходит в раздел конструктора."""
        self.click(self.locators.CONSTRUCTOR_BTN)
        self.wait_until_url_contains(config.BASE_URL)

    @allure.step("Перейти в ленту заказов")
    def navigate_to_order_feed(self) -> None:
        """Кликает на ссылку ленты заказов"""
        logger.info(f"Current URL before click: {self.driver.current_url}")
        self.click(self.locators.ORDER_FEED_BUTTON)
        logger.info(f"Current URL after click: {self.driver.current_url}")
        self.wait_until_url_contains("/feed")

    @allure.step("Оформить заказ")
    def make_order(self) -> str:
        """Оформляет заказ."""
        self.click(self.locators.MAKE_ORDER_BTN)
        self.wait_until_visible(self.locators.ORDER_MODAL)
        return self.wait_until_text_changes(
            locator=self.locators.ORDER_NUMBER,
            old_text="9999",
            timeout=15
        )

    @allure.step("Добавить ингредиент в конструктор")
    def add_ingredient_to_constructor(self) -> None:
        """Добавляет ингредиент в конструктор бургера."""
        source = self.wait_until_visible(self.locators.INGREDIENT_ITEM)
        target = self.wait_until_visible(self.locators.CONSTRUCTOR_AREA)
        self._execute_drag_and_drop_js(source, target)

    @allure.step("Перейти в личный кабинет")
    def go_to_personal_account(self) -> None:
        """Переходит в личный кабинет пользователя."""
        self.click(self.locators.PERSONAL_ACCOUNT_BTN)
        self.wait_until_url_contains("account/profile")

    @allure.step("Получить значение счетчика ингредиента")
    def get_ingredient_counter_value(self) -> int:
        """Возвращает значение счетчика ингредиента."""
        try:
            counter_text = self.get_text(self.locators.INGREDIENT_COUNTER)
            return int(counter_text)
        except (NoSuchElementException, ValueError):
            return 0

    @allure.step("Проверить наличие кнопки оформления заказа")
    def is_order_button_visible(self) -> bool:
        """Проверяет видимость кнопки оформления заказа."""
        return self.is_visible(self.locators.MAKE_ORDER_BTN)

    @allure.step("Перетащить ингредиент в конструктор (JavaScript)")
    def drag_and_drop_ingredient(self) -> None:
        """Перетаскивает ингредиент в конструктор, используя JavaScript."""
        source = self.wait_until_visible(self.locators.INGREDIENT_ITEM)
        target = self.wait_until_visible(self.locators.CONSTRUCTOR_AREA)
        self._execute_drag_and_drop_js(source, target) # Используем метод из BasePage

    @allure.step("Увеличить счетчик ингредиентов")
    def increase_ingredient_counter(self) -> None:
        """Увеличивает счетчик ингредиентов путем перетаскивания ингредиента."""
        self.drag_and_drop_ingredient()

    @allure.step("Получить текущий URL")
    def get_current_page_url(self) -> str:
        """Возвращает текущий URL страницы."""
        return self.get_current_url()

    @allure.step("Проверить видимость модального окна")
    def is_ingredient_modal_visible(self) -> bool:
        """Проверяет видимость модального окна с ингредиентом."""
        return self.is_modal_visible()

    @allure.step("Закрыть модальное окно ингредиента")
    def close_ingredient_modal(self) -> None:
        """Закрывает модальное окно с ингредиентом."""
        self.close_modal()

    @allure.step("Создает тестовый заказ и возвращает его номер")
    def create_test_order(self) -> str:
        """Создает тестовый заказ и возвращает его номер"""
        self.add_ingredient_to_constructor()
        order_number = self.make_order()
        self.close_modal()
        return order_number