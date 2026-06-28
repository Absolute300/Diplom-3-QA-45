# conftest.py

import logging
import random
import uuid
import pytest
import requests
import json
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
    ElementNotInteractableException
)
from config import config

logger = logging.getLogger(__name__)

@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param
    driver = None

    try:
        if browser == "chrome":
            options = uc.ChromeOptions()
            options.add_argument("--disable-popup-blocking")
            options.add_experimental_option("prefs", {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "translate": {"enabled": False},
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_setting_values.geolocation": 2,
            })
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-translate")
            options.add_argument("--disable-save-password-bubble")
            options.add_argument("--disable-single-click-autofill")
            options.add_argument("--disable-features=TranslateUI")

            driver = uc.Chrome(options=options, version_main=None)

        elif browser == "firefox":
            options = FirefoxOptions()
            options.set_preference("signon.rememberSignons", False)
            options.set_preference("signon.autofillForms", False)
            options.set_preference("browser.translation.detectLanguage", False)
            options.set_preference("intl.accept_languages", "en-US")

            driver = webdriver.Firefox(options=options)

        driver.set_window_position(0, 0)
        driver.maximize_window()
        driver.implicitly_wait(5)
        yield driver

    finally:
        if driver:
            try:
                logger.debug(f"Closing driver, session id: {driver.session_id}")
                driver.quit()
            except WebDriverException as e:
                logger.warning(f"Expected error during driver quit: {str(e)}")
            except OSError as e:
                if "Неверный дескриптор" not in str(e):
                    logger.error(f"OS error during driver quit: {str(e)}")
                    raise


@pytest.fixture(scope="session")
def api_client():
    """Фикстура для HTTP-клиента"""
    session = requests.Session()
    session.headers = {"Content-Type": "application/json"}
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def test_user():
    """Фикстура генерирует тестовые данные пользователя"""
    return {
        "email": f"test_{uuid.uuid4().hex[:8]}@example.com",
        "password": f"P@ssw0rd_{uuid.uuid4().hex[:4]}",
        "name": f"User_{uuid.uuid4().hex[:4]}"
    }


@pytest.fixture
def authenticated_user(driver, test_user, api_client, login_page):
    """Фикстура авторизованного пользователя с безопасной очисткой"""
    access_token = None
    refresh_token = None

    # Регистрация пользователя
    try:
        response = api_client.post(
            f"{config.BASE_URL}{config.API_AUTH_REGISTER}",
            json=test_user,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        tokens = response.json()
        access_token = tokens.get("accessToken")
        refresh_token = tokens.get("refreshToken")

        if not access_token:
            pytest.fail("Токен доступа не получен при регистрации")

    except requests.exceptions.HTTPError as e:
        pytest.fail(f"HTTP ошибка при регистрации ({e.response.status_code}): {e.response.text}")
    except requests.exceptions.ConnectionError as e:
        pytest.fail(f"Ошибка подключения: {str(e)}")
    except requests.exceptions.Timeout as e:
        pytest.fail(f"Таймаут запроса: {str(e)}")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Ошибка сети: {str(e)}")
    except (ValueError, KeyError, json.JSONDecodeError) as e:
        pytest.fail(f"Ошибка формата ответа: {str(e)}")

    # Авторизация через UI
    try:
        login_page.open()

        email_field = login_page.wait_until_visible(login_page.locators.EMAIL_INPUT, timeout=20)
        email_field.clear()
        email_field.send_keys(test_user["email"])

        password_field = login_page.wait_until_visible(login_page.locators.PASSWORD_INPUT, timeout=20)
        password_field.clear()
        password_field.send_keys(test_user["password"])

        login_button = login_page.wait_until_clickable(login_page.locators.LOGIN_BUTTON, timeout=20)
        login_button.click()

        if not login_page.wait_until_url_contains(config.MAIN_PAGE_URL, timeout=25):
            raise TimeoutException("Не произошёл переход на главную страницу")

    except TimeoutException as e:
        driver.save_screenshot("ui_login_timeout.png")
        pytest.fail(f"Таймаут при авторизации: {str(e)}")
    except NoSuchElementException as e:
        driver.save_screenshot("ui_login_element_missing.png")
        pytest.fail(f"Элемент не найден: {str(e)}")
    except ElementNotInteractableException as e:
        driver.save_screenshot("ui_login_element_not_interactable.png")
        pytest.fail(f"Элемент недоступен: {str(e)}")
    except WebDriverException as e:
        driver.save_screenshot("ui_login_webdriver_error.png")
        pytest.fail(f"Ошибка WebDriver: {str(e)}")

    yield {
        'user': test_user,
        'access_token': access_token,
        'refresh_token': refresh_token
    }

    # Безопасная очистка
    if access_token:
        # 1. Выход из системы (если есть refresh_token)
        if refresh_token:
            try:
                logout_resp = api_client.post(
                    f"{config.BASE_URL}{config.API_AUTH_LOGOUT}",
                    json={"token": refresh_token},
                    timeout=3
                )
                if logout_resp.status_code != 200:
                    logger.warning(f"Неудачный логаут: {logout_resp.status_code}")
            except requests.exceptions.HTTPError as e:
                logger.warning(f"HTTP ошибка при логауте: {e.response.status_code}")
            except requests.exceptions.RequestException as e:
                logger.warning(f"Ошибка сети при логауте: {str(e)}")

        # 2. Удаление пользователя
        try:
            del_resp = api_client.delete(
                f"{config.BASE_URL}{config.API_AUTH_USER}",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=5
            )

            if del_resp.status_code == 403:
                logger.warning("Удаление пользователя запрещено (403 Forbidden)")
            elif del_resp.status_code != 200:
                logger.warning(f"Неожиданный код ответа при удалении: {del_resp.status_code}")

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP ошибка удаления: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка сети при удалении: {str(e)}")
        except Exception as critical_error:
            logger.critical(f"Критическая ошибка при очистке: {str(critical_error)}")
            raise  # Пробрасываем критические ошибки


@pytest.fixture(scope="module")
def registered_user(api_client):
    """Фикстура регистрации пользователя через API (1 раз на файл тестов)"""
    user_data = {
        "email": f"user_{random.randint(1000, 9999)}@test.com",
        "password": "Password123",
        "name": "Test User"
    }

    # Регистрация
    response = api_client.post(
        config.api_register_url,
        json=user_data,
        timeout=5
    )
    assert response.status_code == 200, "Не удалось зарегистрировать пользователя"

    yield user_data

    # Удаление пользователя через API
    try:
        auth_response = api_client.post(
            config.api_login_url,
            json={"email": user_data["email"], "password": user_data["password"]},
            timeout=5
        )
        if auth_response.status_code == 200:
            api_client.delete(
                config.api_user_url,
                headers={"Authorization": f"Bearer {auth_response.json()['accessToken']}"},
                timeout=5
            )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Ошибка при удалении пользователя: {type(e).__name__}")


@pytest.fixture
def clean_orders(api_client, authenticated_user):
    """Фикстура для очистки заказов после выполнения теста"""
    yield  # Здесь выполняется тест

    try:
        token = api_client.cookies.get("accessToken")
        if token:
            response = api_client.post(
                f"{config.BASE_URL}/api/orders/clear",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200, "Не удалось очистить заказы"
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при очистке заказов: {e}")


# Фикстуры страниц
@pytest.fixture
def main_page(driver):
    from pages.main_page import MainPage
    return MainPage(driver)


@pytest.fixture
def order_feed_page(driver):
    from pages.order_feed_page import OrderFeedPage
    return OrderFeedPage(driver)


@pytest.fixture
def profile_page(driver):
    from pages.profile_page import ProfilePage
    return ProfilePage(driver)


@pytest.fixture
def login_page(driver):
    from pages.login_page import LoginPage
    return LoginPage(driver)


@pytest.fixture
def register_page(driver):
    """Фикстура для страницы регистрации"""
    from pages.register_page import RegisterPage
    return RegisterPage(driver)


@pytest.fixture
def password_restore_page(driver):
    from pages.password_restore_page import PasswordRestorePage
    return PasswordRestorePage(driver)