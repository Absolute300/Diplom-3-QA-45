# main_page_locators.py

from selenium.webdriver.common.by import By

class MainPageLocators:
    # Кнопки навигации
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']/..")
    ORDER_FEED_BUTTON = (By.XPATH, "//a[@href='/feed']")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//p[text()='Личный Кабинет']/..")
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Выход')]")

    # Разделы ингредиентов
    INGREDIENTS_SECTION = (By.XPATH, "//section[contains(@class, 'BurgerIngredients_ingredients')]")
    BUN_SECTION = (By.XPATH, "//h2[text()='Булки']/..")
    SAUCE_SECTION = (By.XPATH, "//h2[text()='Соусы']/..")
    MAIN_SECTION = (By.XPATH, "//h2[text()='Начинки']/..")

    # Элементы ингредиентов
    INGREDIENT_ITEM = (By.XPATH, "//div[contains(@class, 'BurgerIngredient_ingredient')]")
    INGREDIENT_COUNTER = (By.CSS_SELECTOR, "p.counter_counter__num__3nue1")

    # Конструктор
    CONSTRUCTOR_AREA = (By.XPATH, "//section[contains(@class, 'BurgerConstructor_basket')]")
    CONSTRUCTOR_SECTION = (By.XPATH, "//section[contains(@class, 'BurgerConstructor_container')]")
    MAKE_ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")

    # Заказ
    ORDER_NUMBER = (By.XPATH, "//h2[contains(@class, 'text_type_digits-large')]")

    # Прочие элементы
    LOADER = (By.XPATH, "//div[contains(@class, 'loader')]")
    CONSTRUCTOR_BTN = (By.XPATH, "//a[@href='/']")
    ORDER_FEED_BTN = (By.XPATH, "//a[@href='/feed']")
    PERSONAL_ACCOUNT_BTN = (By.XPATH, "//a[@href='/account']")
    MAKE_ORDER_BTN = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    CREATE_ORDER_BTN = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    ORDER_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal')]")
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")