# base_page.py

import allure
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
    WebDriverException
)
from typing import Tuple, Any, Callable, Optional
from config import config

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver: WebDriver, url_suffix: str = "", timeout: int = None):
        self.driver = driver
        self.timeout = timeout or 10
        self.logger = logging.getLogger(__name__)
        self.url = config.build_url(url_suffix)

    @property
    def wait(self) -> WebDriverWait:
        """Возвращает экземпляр WebDriverWait с default_timeout"""
        return WebDriverWait(self.driver, self.timeout)

    def get_wait(self, timeout: float | None = None) -> WebDriverWait:
        """Возвращает WebDriverWait с заданным таймаутом или default_timeout, если таймаут не указан"""
        return WebDriverWait(self.driver, timeout or self.timeout)

    # ==================== Основные методы взаимодействия ====================

    def open(self):
        """Открывает страницу с корректным URL"""
        self.logger.info(f"Opening URL: {self.url}")
        self.driver.get(self.url)
        self._verify_page_loaded()

    @allure.step("Клик по элементу {locator}")
    def click(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> None:
        element = self.wait_until_clickable(locator, timeout)
        try:
            element.click()
        except ElementClickInterceptedException:
            self._click_via_js(element)

    @allure.step("Ввод текста '{text}' в элемент {locator}")
    def type_text(self, locator: Tuple[str, str], text: str, clear: bool = True) -> None:
        element = self.wait_until_visible(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    # ==================== Методы получения данных ====================

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        """Возвращает текущий URL страницы."""
        return self.driver.current_url

    @allure.step("Получение текста элемента {locator}")
    def get_text(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> str:
        element = self.wait_until_visible(locator, timeout)
        return element.text.strip()

    @allure.step("Получить атрибут элемента")
    def get_attribute(self, locator: Tuple[str, str], attribute: str) -> str:
        try:
            element = self.wait_until_present(locator)
            return element.get_attribute(attribute) or ""
        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"Не удалось получить атрибут: {str(e)}")
            raise

    @allure.step("Простой поиск одного элемента без ожидания")
    def find_element(self, *locator: Tuple[str, str]) -> WebElement:
        """Простой поиск одного элемента без ожидания"""
        return self.driver.find_element(*locator)

    @allure.step("Простой поиск нескольких элементов без ожидания")
    def find_elements(self, *locator: Tuple[str, str]) -> list[WebElement]:
        """Простой поиск нескольких элементов без ожидания"""
        return self.driver.find_elements(*locator)

    @allure.step("Получить числовое значение элемента")
    def get_numeric_value(self, locator: Tuple[str, str]) -> int:
        """
        Безопасное получение числа из элемента
        :raises ValueError: Если элемент не найден или текст не преобразуется в число
        """
        try:
            text = self.get_text(locator)
            try:
                return int(text)
            except ValueError as e:
                raise ValueError(f"Невозможно преобразовать текст элемента в число: '{text}'") from e
        except NoSuchElementException as e:
            raise ValueError(f"Элемент {locator} не найден на странице") from e

    # ==================== Методы ожидания ====================

    @allure.step("Ожидание выполнения условия")
    def wait_for_condition(self, condition: Callable[[], bool],
                           timeout: Optional[int] = None,
                           poll_frequency: float = 0.5,  # Добавляем параметр с дефолтным значением
                           message: str = "") -> bool:
        wait_timeout = timeout or self.timeout
        try:
            return WebDriverWait(
                self.driver,
                wait_timeout,
                poll_frequency=poll_frequency  # Передаем параметр в WebDriverWait
            ).until(
                lambda _: condition(),
                message=message or f"Условие не выполнено за {wait_timeout} секунд"
            )
        except TimeoutException as e:
            logger.error(f"Timeout waiting for condition: {str(e)}")
            raise

    @allure.step("Ожидание присутствия элемента в DOM")
    def wait_until_present(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
         return self._wait_until(
            EC.presence_of_element_located(locator),
            timeout=timeout,
            message=f"Элемент {locator} не найден в DOM"
        )

    @allure.step("Ожидание видимости элемента {locator}")
    def wait_until_visible(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        return self._wait_until(
            EC.visibility_of_element_located(locator),
            timeout=timeout,
            message=f"Элемент {locator} не стал видимым"
        )

    @allure.step("Ожидание кликабельности элемента {locator}")
    def wait_until_clickable(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        return self._wait_until(
            EC.element_to_be_clickable(locator),
            timeout=timeout,
            message=f"Элемент {locator} не стал кликабельным"
        )

    @allure.step("Ожидание загрузки страницы")
    def wait_for_page_loaded(self, timeout: Optional[int] = None) -> None:
        wait_timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, wait_timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException as e:
            logger.error(f"Страница не загрузилась за {wait_timeout} секунд")
            raise

    @allure.step("Ожидание URL содержащего '{expected_part}'")
    def wait_until_url_contains(self, expected_part: str, timeout: Optional[int] = None) -> bool:
        return self._wait_until(
            EC.url_contains(expected_part),
            timeout=timeout,
            message=f"URL не содержит '{expected_part}'"
        )

    @allure.step("Ожидание исчезновения элемента")
    def wait_until_not_visible(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        return self._wait_until(
            EC.invisibility_of_element_located(locator),
            timeout=timeout,
            message=f"Элемент {locator} не исчез"
        )

    @allure.step("Ожидание появления текста в элементе")
    def wait_until_text_present(self, locator: Tuple[str, str], text: str, timeout: Optional[int] = None) -> bool:
        return self._wait_until(
            EC.text_to_be_present_in_element(locator, text),
            timeout=timeout,
            message=f"Текст '{text}' не появился в элементе {locator}"
        )

    @allure.step("Дождаться изменения текста элемента")
    def wait_until_text_changes(self, locator: tuple, old_text: str, timeout: int = 10) -> str:
        def text_changed(driver):
            try:
                element = driver.find_element(*locator)
                current_text = element.text
                return current_text if current_text != old_text else False
            except NoSuchElementException:
                return False

        try:
            return self.get_wait(timeout).until(
                text_changed,
                message=f"Текст элемента {locator} не изменился с '{old_text}'"
            )
        except TimeoutException as e:
            self.logger.error(f"Timeout waiting for text change: {str(e)}")
            raise

    # ==================== Проверки состояния ====================

    @allure.step("Проверка что URL содержит '{expected_part}'")
    def url_should_contain(self, expected_part: str) -> None:
        current_url = self.get_current_url()
        if expected_part.lower() not in current_url.lower():
            raise AssertionError(f"URL '{current_url}' не содержит '{expected_part}'")

    @allure.step("Проверка видимости элемента {locator}")
    def is_visible(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        try:
            return self.wait_until_visible(locator, timeout) is not None
        except TimeoutException:
            return False

    @allure.step("Проверка присутствия элемента {locator}")
    def is_present(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        try:
            self.wait_until_present(locator, timeout)
            return True
        except TimeoutException:
            return False

    @allure.step("Проверить кликабельность элемента {locator}")
    def is_clickable(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        try:
            self.wait_until_clickable(locator, timeout)
            return True
        except TimeoutException:
            return False

    # ==================== Внутренние методы ====================

    def _wait_until(self, condition: Callable[[WebDriver], Any],
                    timeout: Optional[int] = None,
                    message: str = "") -> Any:
        wait_timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, wait_timeout).until(
                condition,
                message=message
            )
        except TimeoutException as e:
            logger.error(f"Timeout waiting for condition: {message}")
            raise
        except WebDriverException as e:
            logger.error(f"WebDriver error while waiting: {str(e)}")
            raise

    @allure.step("Клик через JavaScript")
    def _click_via_js(self, element: WebElement) -> None:
        """Выполняет клик через JavaScript."""
        try:
            self.driver.execute_script("arguments[0].click();", element)
        except WebDriverException as e:
            logger.error(f"JavaScript click failed: {str(e)}")
            raise

    def _verify_page_loaded(self) -> None:
        """Абстрактный метод для проверки загрузки страницы (должен быть реализован в дочерних классах)."""
        raise NotImplementedError("Метод должен быть реализован в дочернем классе")

    @allure.step("Выполнение перетаскивания через JavaScript")
    def _execute_drag_and_drop_js(self, source: WebElement, target: WebElement) -> None:
        """Внутренний метод для выполнения drag-and-drop через JS."""
        script = """
        function simulateDragDrop(sourceNode, targetNode) {
            // Создаем и инициируем событие dragstart
            const dragStartEvent = new DragEvent('dragstart', {
                bubbles: true,
                cancelable: true,
                dataTransfer: new DataTransfer()
            });
            sourceNode.dispatchEvent(dragStartEvent);

            // Создаем и инициируем событие dragover
            const dragOverEvent = new DragEvent('dragover', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dragStartEvent.dataTransfer
            });
            targetNode.dispatchEvent(dragOverEvent);

            // Создаем и инициируем событие drop
            const dropEvent = new DragEvent('drop', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dragStartEvent.dataTransfer
            });
            targetNode.dispatchEvent(dropEvent);

            // Завершаем процесс событием dragend
            const dragEndEvent = new DragEvent('dragend', {
                bubbles: true,
                cancelable: true
            });
            sourceNode.dispatchEvent(dragEndEvent);
        }
        simulateDragDrop(arguments[0], arguments[1]);
        """
        self.driver.execute_script(script, source, target)

    @allure.step("Прокрутка к элементу")
    def _scroll_to_element(self, element: WebElement) -> None:
        """Прокручивает страницу к указанному элементу."""
        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                element
            )
        except WebDriverException as e:
            logger.warning(f"Не удалось прокрутить к элементу: {str(e)}")

    # ==================== Методы для динамических счетчиков ====================

    @allure.step("Ожидание увеличения числового значения")
    def wait_for_value_increase(self, get_value_func: Callable[[], int],
                                initial_value: int,
                                timeout: int = 20) -> int:
        """
        Ожидает увеличения числового значения, возвращает новое значение
        :param get_value_func: Функция для получения текущего значения
        :param initial_value: Начальное значение для сравнения
        :param timeout: Максимальное время ожидания
        """

        def value_increased(_):
            current_value = get_value_func()
            return current_value if current_value > initial_value else False

        try:
            return self._wait_until(
                value_increased,
                timeout=timeout,
                message=f"Значение не увеличилось от {initial_value} за {timeout} сек"
            )
        except TimeoutException:
            final_value = get_value_func()
            raise TimeoutError(
                f"Счетчик не увеличился. Исходное: {initial_value}, текущее: {final_value}"
            )

    @allure.step("Ожидание изменения числового значения")
    def wait_for_value_change(self, get_value_func: Callable[[], int],
                              initial_value: int,
                              timeout: int = 20) -> int:
        """
        Ожидает любого изменения числового значения
        :param get_value_func: Функция для получения текущего значения
        :param initial_value: Начальное значение для сравнения
        :param timeout: Максимальное время ожидания
        """

        def value_changed(_):
            current_value = get_value_func()
            return current_value if current_value != initial_value else False

        return self._wait_until(
            value_changed,
            timeout=timeout,
            message=f"Значение не изменилось от {initial_value} за {timeout} сек"
        )