# register_page_locators.py

from selenium.webdriver.common.by import By

class RegisterPageLocators:
    REGISTER_FORM = (By.CSS_SELECTOR, "form.Auth_form__3qKeq")
    NAME_INPUT = (By.CSS_SELECTOR, "input[name='name']")
    EMAIL_INPUT = (By.CSS_SELECTOR,
                   "fieldset.Auth_fieldset__1QzWN:nth-of-type(2) input")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "button.button_button__33qZ0")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "p.input__error")
    LOGIN_LINK = (By.XPATH, "//a[contains(@href, 'login')]")
    CONSTRUCTOR_LINK = (By.XPATH, "//a[contains(@href, '/') and contains(@class, 'AppHeader_header__link')]")