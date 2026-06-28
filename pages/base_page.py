import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from config import Config


class BasePage:
    @allure.step("Инициировать BasePage")
    def __init__(self, driver):
        self.driver = driver
        self.base_url = Config.BASE_URL
        self.wait = WebDriverWait(driver, Config.DEFAULT_TIMEOUT)

    @allure.step("Открыть URL: {url}")
    def open(self, url=""):
        full_url = f"{self.base_url}{url}"
        self.driver.get(full_url)

    @allure.step("Найти элемент по локатору: {locator}")
    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Найти все элементы по локатору: {locator}")
    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    @allure.step("Кликнуть на элемент: {locator}")
    def click_element(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.execute_script(
            """
            document.querySelectorAll('.Modal_modal_overlay__x2ZCr').forEach(el => {
                if (el) el.remove();
            });
            """
        )
        self.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.execute_script("arguments[0].click();", element)

    @allure.step("Кликнуть на элемент через JavaScript")
    def click_element_via_js(self, element):
        """Клик на элемент через JavaScript (если обычный клик не работает)"""
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Ввести текст '{text}' в элемент: {locator}")
    def input_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Получить текст элемента: {locator}")
    def get_element_text(self, locator):
        element = self.find_element(locator)
        return element.text

    @allure.step("Получить текст элемента без ожидания")
    def get_element_text_no_wait(self, locator):
        element = self.driver.find_element(*locator)
        return element.text

    @allure.step("Проверить видимость элемента: {locator}")
    def is_element_visible(self, locator):
        try:
            self.find_element(locator)
            return True
        except TimeoutException:
            return False

    @allure.step("Ожидаем невидимость элемента: {locator}")
    def wait_element_invisible(self, locator, timeout=None):
        wait = WebDriverWait(self.driver, timeout or self.wait._timeout)
        wait.until(EC.invisibility_of_element_located(locator))

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        return self.driver.current_url

    @allure.step("Дождаться загрузки страницы")
    def wait_for_page_load(self):
        self.wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    @allure.step("Перетащить элемент из {source_locator} в {target_locator}")
    def drag_and_drop(self, source_locator, target_locator):
        source_element = self.find_element(source_locator)
        target_element = self.find_element(target_locator)

        action_chains = ActionChains(self.driver)
        action_chains.drag_and_drop(source_element, target_element).perform()

    @allure.step("Проверить что элемент не виден: {locator}")
    def is_element_not_visible(self, locator, timeout=None):
        try:
            wait = WebDriverWait(self.driver, timeout or self.wait._timeout)
            wait.until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    @allure.step("перетаскивание элемента")
    def drag_and_drop_react(self, source_element, target_element):
        self.driver.execute_script("arguments[0].scrollIntoView();", source_element)
        self.driver.execute_script("arguments[0].scrollIntoView();", target_element)

        js = """
            const src = arguments[0];
            const tgt = arguments[1];
            const dataTransfer = new DataTransfer();
            function fire(el, type, dt){
                const e = new DragEvent(type, {
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: dt
                });
                el.dispatchEvent(e);
            }
            fire(src, 'dragstart', dataTransfer);
            fire(tgt, 'dragenter', dataTransfer);
            fire(tgt, 'dragover', dataTransfer);
            fire(tgt, 'drop', dataTransfer);
            fire(src, 'dragend', dataTransfer);
        """
        try:
            self.driver.execute_script(js, source_element, target_element)
        except Exception:
            actions = ActionChains(self.driver)
            actions.click_and_hold(source_element).move_to_element(target_element).release().perform()

    @allure.step("Получаем заголовок страницы")
    def get_page_title(self):
        return self.driver.title

    @allure.step("Выполнить JavaScript: {script}")
    def execute_script(self, script, *args):
        """Выполнить JavaScript код"""
        return self.driver.execute_script(script, *args)

    @allure.step("Дождаться кликабельности элемента: {locator}")
    def wait_for_element_clickable(self, locator, timeout=None):
        """Ожидание кликабельности элемента"""
        wait = WebDriverWait(self.driver, timeout or self.wait._timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    @allure.step("Дождаться видимости элемента: {locator}")
    def wait_for_element_visible(self, locator, timeout=None):
        """Ожидание видимости элемента"""
        wait = WebDriverWait(self.driver, timeout or self.wait._timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Дождаться появления элемента: {locator}")
    def wait_for_element_present(self, locator, timeout=None):
        """Ожидание присутствия элемента в DOM"""
        wait = WebDriverWait(self.driver, timeout or self.wait._timeout)
        return wait.until(EC.presence_of_element_located(locator))

    @allure.step("Дождаться условия: {condition_name}")
    def wait_for_condition(self, condition, timeout=None, condition_name="custom condition"):
        """Ожидание кастомного условия"""
        wait = WebDriverWait(self.driver, timeout or self.wait._timeout)
        return wait.until(condition)

    @allure.step("Найти элемент без ожидания")
    def find_element_no_wait(self, locator):
        """Найти элемент без явного ожидания"""
        return self.driver.find_element(*locator)