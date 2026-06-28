# order_feed_page.py

import allure
import logging
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
    StaleElementReferenceException
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import List, Tuple
from .base_page import BasePage
from locators.modal_locators import ModalLocators
from locators.order_feed_locators import OrderFeedLocators
from helpers import CounterNotIncreasedError
from config import config

logger = logging.getLogger(__name__)


class OrderFeedPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.locators = OrderFeedLocators()
        self.modal_locators = ModalLocators()
        self.modal_timeout = 5

    @allure.step("Открыть ленту заказов")
    def open(self) -> None:
        """Открывает страницу ленты заказов и проверяет её загрузку."""
        self.url = config.ORDER_FEED_URL
        self.logger.info(f"Открытие OrderFeedPage, URL: {self.url}")
        try:
            self.driver.get(self.url)
            self._verify_page_loaded()
        except WebDriverException as e:
            self.logger.error(f"Ошибка при открытии страницы: {str(e)}")
            raise

    @allure.step("Кликнуть на первый заказ в ленте")
    def click_first_order(self) -> None:
        """Кликает на первый заказ в ленте заказов"""
        self.click(self.locators.FIRST_ORDER_NUMBER)
        self.wait_until_visible(self.locators.ORDER_MODAL)

    @allure.step("Получить номер первого заказа")
    def get_first_order_number(self) -> str:
        """Возвращает номер первого заказа в ленте."""
        return self.get_text(self.locators.FIRST_ORDER_NUMBER)

    @allure.step("Получить номер заказа из модального окна")
    def get_modal_order_number(self) -> str:
        """Возвращает номер заказа из модального окна."""
        return self.get_text(self.locators.MODAL_ORDER_NUMBER, timeout=10)

    @allure.step("Проверить видимость модального окна заказа")
    def is_order_modal_visible(self) -> bool:
        """Проверяет видимость модального окна с деталями заказа."""
        return self.is_visible(self.locators.ORDER_MODAL)

    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self) -> None:
        """Закрывает модальное окно с деталями заказа."""
        if self.is_order_modal_visible():
            self.click(self.modal_locators.MODAL_CLOSE_BUTTON)
            self.wait_until_not_visible(self.locators.ORDER_MODAL, timeout=10)

    @allure.step("Получить общее количество заказов")
    def get_total_orders_count(self) -> int:
        """Возвращает общее количество выполненных заказов."""
        count_text = self.get_text(self.locators.TOTAL_ORDERS_COUNT)
        return self._parse_count_text(count_text)

    @allure.step("Получить количество заказов за сегодня")
    def get_today_orders_count(self) -> int:
        """Возвращает количество заказов за сегодня."""
        count_text = self.get_text(self.locators.TODAY_ORDERS_COUNT)
        return self._parse_count_text(count_text)

    @allure.step("Получить все номера заказов")
    def get_all_order_numbers(self) -> List[str]:
        """Возвращает список всех видимых номеров заказов."""
        elements = self._find_elements(self.locators.ORDER_ITEM)
        return [self._get_order_number(element) for element in elements]

    @allure.step("Извлекает номер заказа из элемента")
    def _get_order_number(self, order_element: WebElement) -> str:
        """Извлекает номер заказа из элемента."""
        try:
            return order_element.find_element(*self.locators.ORDER_NUMBER).text
        except NoSuchElementException:
            return ""

    @allure.step("Находит элементы по локатору или возвращает пустой список")
    def _find_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        """Находит элементы по локатору или возвращает пустой список."""
        try:
            return super().find_elements(*locator)
        except NoSuchElementException:
            return []

    @staticmethod
    @allure.step("Преобразует текст счетчика в число")
    def _parse_count_text(count_text: str) -> int:
        """Преобразует текст счетчика в число."""
        try:
            return int(count_text)
        except ValueError as e:
            logger.error(f"Ошибка преобразования счетчика: {count_text}")
            raise ValueError(f"Некорректное значение счетчика: {count_text}") from e

    @allure.step("Проверяет загрузку страницы ленты заказов")
    def _verify_page_loaded(self) -> None:
        """Проверяет загрузку страницы ленты заказов"""
        try:
            self.wait_until_visible(self.locators.PAGE_HEADER, timeout=30)
            self.wait_until_visible(self.locators.ORDER_STATUS_BOX, timeout=30)
        except TimeoutException as e:
            raise TimeoutException(f"Страница ленты заказов не загрузилась: {str(e)}")

    @allure.step("Проверяет видимость заголовка страницы 'Лента заказов'")
    def is_page_header_visible(self) -> bool:
        """Проверяет видимость заголовка страницы 'Лента заказов'."""
        return self.is_visible(self.locators.PAGE_HEADER)

    @allure.step("Получить текущий URL")
    def get_current_page_url(self) -> str:
        """Возвращает текущий URL страницы."""
        return self.get_current_url()

    def wait_for_order_in_progress(self, order_number: str, timeout: int = 30) -> bool:
        normalized_target = self.normalize_order_number(order_number)

        def is_order_visible() -> bool:
            current_orders = self.get_orders_in_progress()
            normalized_orders = [self.normalize_order_number(n) for n in current_orders]
            self.logger.debug(f"Текущие заказы в работе (нормализованные): {normalized_orders}")
            return normalized_target in normalized_orders

        try:
            return self.wait_for_condition(
                is_order_visible,
                timeout=timeout,
                message=f"Заказ {order_number} не появился в разделе 'В работе'"
            )
        except TimeoutException:
            return False

    @allure.step("Проверить загрузку страницы")
    def is_page_loaded(self) -> bool:
        """Проверяет, что страница ленты заказов полностью загружена"""
        try:
            return all([
                self.is_visible(self.locators.PAGE_HEADER),
                self.is_visible(self.locators.ORDERS_IN_PROGRESS_SECTION)
            ])
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(f"Элементы страницы не найдены: {str(e)}")
            return False
        except WebDriverException as e:
            self.logger.critical(f"Критическая ошибка WebDriver: {str(e)}")
            raise  # Пробрасываем критическое исключение выше

    @allure.step("Получить общее количество заказов")
    def get_total_orders_count(self) -> int:
        """Получает значение счетчика через безопасный метод"""
        return self.get_numeric_value(self.locators.TOTAL_ORDERS_COUNT)

    @allure.step("Ожидание увеличения счетчика")
    def wait_for_total_increase(self, initial_value: int, timeout: int = 20) -> bool:
        """Ожидает увеличения значения счетчика"""

        def is_increased() -> bool:
            try:
                return self.get_total_orders_count() > initial_value
            except ValueError:
                return False

        return self.wait_for_condition(
            is_increased,
            timeout=timeout,
            message=f"Счетчик не превысил {initial_value} за {timeout} сек"
        )

    @allure.step("Получить валидированное значение счетчика")
    def get_validated_counter_value(self) -> int:
        self.open()
        count = self.get_total_orders_count()

        if not isinstance(count, int) or count < 0:
            raise ValueError(f"Некорректное значение счетчика: {count}")

        self.logger.info(f"Начальное значение счетчика: {count}")
        return count

    @allure.step("Проверить увеличение счетчика")
    def verify_counter_increase(self, initial_value: int) -> None:
        current = self.get_total_orders_count()
        if current <= initial_value:
            raise CounterNotIncreasedError(initial_value, current)
        self.logger.info(f"Счетчик увеличился: {initial_value} → {current}")

    @allure.step("Проверить появление заказа в разделе 'В работе'")
    def is_order_in_progress(self, order_number: str, timeout: int = 30) -> bool:
        normalized_target = self.normalize_order_number(order_number)

        def check_order():
            if self.is_visible(self.locators.ALL_ORDERS_READY_MSG, timeout=1):
                self.logger.debug("Сообщение 'Все текущие заказы готовы!' отображается, ждем исчезновения")
                return False

            orders = self.get_orders_in_progress()
            normalized_orders = [self.normalize_order_number(n) for n in orders]
            self.logger.debug(f"Текущие заказы в работе (нормализованные): {normalized_orders}")
            return normalized_target in normalized_orders

        try:
            return self.wait_for_condition(
                check_order,
                timeout=timeout,
                message=f"Заказ {order_number} не появился в разделе 'В работе' за {timeout} секунд"
            )
        except TimeoutException:
            self.logger.warning(f"Заказ {order_number} не появился в разделе 'В работе' за {timeout} секунд")
            return False

    def get_orders_in_progress(self) -> list[str]:
        try:
            if self.is_visible(self.locators.ALL_ORDERS_READY_MSG, timeout=1):
                self.logger.info("Сообщение 'Все текущие заказы готовы!' отображается — заказы в работе отсутствуют")
                return []

            elements = self.find_elements(*self.locators.IN_PROGRESS_ORDER_NUMBERS)
            numbers = [el.text.strip() for el in elements if el.is_displayed() and el.text.strip()]
            self.logger.info(f"Номера заказов в работе: {numbers}")
            return numbers

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException) as e:
            self.logger.warning(f"Ожидаемая ошибка при получении заказов в работе: {e}")
            return []
        except WebDriverException as e:
            self.logger.error(f"Критическая ошибка WebDriver при получении заказов в работе: {e}")
            raise

    def is_order_in_system(self, order_number: str, timeout: int = 10) -> bool:
        normalized_target = self.normalize_order_number(order_number)
        try:
            return self.wait_for_condition(
                lambda: normalized_target in self.driver.page_source,
                timeout=timeout,
                message=f"Заказ {order_number} не появился в системе"
            )
        except TimeoutException:
            self.logger.warning(f"Заказ {order_number} не найден в системе за {timeout} сек")
            return False
        except WebDriverException as e:
            self.logger.error(f"Ошибка WebDriver при проверке заказа: {str(e)}")
            raise

    @allure.step("Получить текущий текст раздела 'В работе'")
    def _get_in_progress_text(self) -> str:
        """Внутренний метод для получения текста раздела"""
        return self.get_text(self.locators.IN_PROGRESS_SECTION)

    @allure.step("Проверить состояние раздела 'В работе'")
    def check_in_progress_section(self) -> str:
        """
        Возвращает текущее состояние раздела:
        - номер заказа, если есть активные заказы
        - текст 'Все текущие заказы готовы!', если нет активных
        """
        return self._get_in_progress_text()

    def was_order_in_progress(self, order_number: str, observation_time: int = 30) -> bool:
        normalized_target = self.normalize_order_number(order_number)

        def check_order() -> bool:
            current_text = self._get_in_progress_text()
            normalized_text = self.normalize_order_number(current_text)
            return normalized_target in normalized_text

        try:
            return self.wait_for_condition(
                check_order,
                timeout=observation_time,
                message=f"Заказ {order_number} не появился в разделе за {observation_time} сек"
            )
        except TimeoutException:
            return False

    @allure.step("Дождаться исчезновения сообщения 'Все текущие заказы готовы!'")
    def wait_until_all_orders_ready_msg_disappears(self, timeout: int = 5) -> bool:
        return self.wait_until_not_visible(self.locators.ALL_ORDERS_READY_MSG, timeout=timeout)

    @staticmethod
    @allure.step("Нормализовать номер заказа, убрав ведущие нули")
    def normalize_order_number(number: str) -> str:
        return number.lstrip('0')