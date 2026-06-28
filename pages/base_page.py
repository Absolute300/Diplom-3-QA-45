import allure
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    DEFAULT_TIMEOUT = 60

    def __init__(self, driver):
        self.driver = driver

    @allure.step("Open page: {url}")
    def open(self, url):
        self.driver.get(url)

    def find_element(self, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located(locator)
        )

    def wait_present(self, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located(locator)
        )

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    @allure.step("Click element")
    def click(self, locator, timeout=DEFAULT_TIMEOUT):
        self.wait_clickable(locator, timeout).click()

    def wait_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            ec.visibility_of_element_located(locator)
        )

    def wait_clickable(self, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            ec.element_to_be_clickable(locator)
        )

    def wait_invisible(self, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            ec.invisibility_of_element_located(locator)
        )

    def get_text(self, locator, timeout=DEFAULT_TIMEOUT):
        return self.wait_visible(locator, timeout).text

    def get_current_url(self):
        return self.driver.current_url

    def wait_until(self, condition, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(condition)

    def scroll_to_element(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            element,
        )

    @allure.step("Drag element to target")
    def drag_and_drop(self, source, target):
        self.scroll_to_element(source)
        ActionChains(self.driver).move_to_element(source).click_and_hold(source).pause(
            0.2
        ).move_to_element(target).pause(0.2).release(target).perform()

    @allure.step("Drag element to target with JavaScript fallback")
    def drag_and_drop_js(self, source, target):
        self.driver.execute_script(
            """
            const source = arguments[0];
            const target = arguments[1];
            const dataTransfer = {
                data: {},
                dropEffect: 'move',
                effectAllowed: 'all',
                files: [],
                items: [],
                types: [],
                setData(format, data) {
                    this.data[format] = data;
                    this.types = Object.keys(this.data);
                },
                getData(format) {
                    return this.data[format];
                },
                clearData(format) {
                    if (format) {
                        delete this.data[format];
                    } else {
                        this.data = {};
                    }
                    this.types = Object.keys(this.data);
                }
            };

            function dispatch(element, name) {
                const event = new Event(name, {bubbles: true, cancelable: true});
                Object.defineProperty(event, 'dataTransfer', {value: dataTransfer});
                element.dispatchEvent(event);
            }

            dispatch(source, 'dragstart');
            dispatch(target, 'dragenter');
            dispatch(target, 'dragover');
            dispatch(target, 'drop');
            dispatch(source, 'dragend');
            """,
            source,
            target,
        )

    def wait_counter_increased(self, counter_locator, old_value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            lambda _: int(self.find_element(counter_locator, timeout=2).text) > old_value
        )

    def wait_counter_increased_with_fallback(
        self, source, target, counter_locator, old_value
    ):
        try:
            self.drag_and_drop(source, target)
            self.wait_counter_increased(counter_locator, old_value)
        except (TimeoutException, WebDriverException):
            self.drag_and_drop_js(source, target)
            self.wait_counter_increased(counter_locator, old_value)