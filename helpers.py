# helpers.py

import allure
import pytest
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import List, Union, Tuple
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementNotInteractableException
)
from pages.login_page import LoginPage
from pages.register_page import RegisterPage

logger = logging.getLogger(__name__)

@allure.step("Перетаскивание элемента на целевой элемент")
def drag_and_drop(driver: WebDriver, source: WebElement, target: WebElement) -> None:
    try:
        driver.execute_script("""
        function simulateDragDrop(sourceNode, targetNode) {
            const dragStart = new DragEvent('dragstart', {
                bubbles: true,
                cancelable: true,
                dataTransfer: new DataTransfer()
            });
            sourceNode.dispatchEvent(dragStart);

            const dragOver = new DragEvent('dragover', { bubbles: true });
            targetNode.dispatchEvent(dragOver);

            const drop = new DragEvent('drop', {
                bubbles: true,
                dataTransfer: dragStart.dataTransfer
            });
            targetNode.dispatchEvent(drop);
        }
        simulateDragDrop(arguments[0], arguments[1]);
        """, source, target)
    except (WebDriverException, StaleElementReferenceException) as e:
        logger.error(f"Ошибка при перетаскивании: {str(e)}")
        raise


@allure.step("Проверка наличия заказа в списке")
def is_order_in_list(order_numbers: List[Union[str, int]], order_number: Union[str, int]) -> bool:
    try:
        return str(order_number) in map(str, order_numbers)
    except (TypeError, ValueError) as e:
        logger.warning(f"Ошибка преобразования типа заказа: {str(e)}")
        return False


@allure.step("Ожидание появления текста в элементе")
def wait_for_text_in_element(
        driver: WebDriver,
        locator: Tuple[str, str],
        expected_text: str,
        timeout: int = 10
) -> bool:
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    try:
        return WebDriverWait(driver, timeout).until(
            EC.text_to_be_present_in_element(locator, expected_text))
    except TimeoutException:
        logger.debug(f"Текст '{expected_text}' не появился в элементе {locator}")
        return False
    except NoSuchElementException as e:
        logger.warning(f"Элемент не найден: {str(e)}")
        return False


@allure.step("Зарегистрировать нового пользователя")
def register_new_user(driver: WebDriver, user_data: dict) -> None:
    register_page = RegisterPage(driver)
    register_page.open()
    register_page.register(
        user_data["name"],
        user_data["email"],
        user_data["password"]
    )


@allure.step("Авторизовать пользователя")
def login_user(driver: WebDriver, email: str, password: str) -> None:
    if not isinstance(driver, WebDriver):
        raise TypeError("Параметр driver должен быть экземпляром WebDriver")

    if not email or not password:
        raise ValueError("Email и пароль обязательны для авторизации")

    login_page = LoginPage(driver)

    try:
        login_page.open()
    except TimeoutException as e:
        raise TimeoutError(f"Таймаут при открытии страницы логина: {str(e)}") from e

    try:
        login_page.type_text(login_page.locators.EMAIL_INPUT, email)
        login_page.type_text(login_page.locators.PASSWORD_INPUT, password)
        login_page.click(login_page.locators.LOGIN_BUTTON)
    except NoSuchElementException as e:
        raise LookupError(f"Не найден элемент для ввода данных: {str(e)}") from e
    except ElementNotInteractableException as e:
        raise RuntimeError(f"Элемент недоступен для взаимодействия: {str(e)}") from e
    except WebDriverException as e:
        raise RuntimeError(f"Ошибка WebDriver при авторизации: {str(e)}") from e


@allure.step("Полная регистрация и авторизация")
def full_register_and_login(driver: WebDriver, user_data: dict) -> None:
    if not isinstance(driver, WebDriver):
        raise TypeError("Параметр driver должен быть экземпляром WebDriver")

    required_fields = {'email', 'password', 'name'}
    if not required_fields.issubset(user_data.keys()):
        missing = required_fields - set(user_data.keys())
        raise ValueError(f"Отсутствуют обязательные поля: {missing}")

    try:
        register_new_user(driver, user_data)
        login_user(driver, user_data["email"], user_data["password"])
    except (ValueError, LookupError, RuntimeError, TimeoutError) as e:
        raise RuntimeError(f"Ошибка в процессе регистрации/авторизации: {str(e)}") from e

class CounterNotIncreasedError(Exception):
    def __init__(self, initial_value: int, current_value: int):
        self.initial_value = initial_value
        self.current_value = current_value
        super().__init__(f"Счетчик не увеличился. Было: {initial_value}, стало: {current_value}")

@allure.step("Проверить увеличение счетчика")
def verify_counter_increase(order_feed_page, initial_count: int) -> None:
    """Вспомогательная функция для проверки увеличения счетчика"""
    try:
        order_feed_page.verify_counter_increase(initial_count)
    except CounterNotIncreasedError as e:
        pytest.fail(str(e))
    except ValueError as e:
        pytest.fail(f"Ошибка значения счетчика: {str(e)}")
        