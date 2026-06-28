from selenium.webdriver.common.by import By


class MainPageLocators:
    """Локаторы для главной страницы"""
    
    # Навигация
    CONSTRUCTOR_TAB = (By.XPATH, "//p[text()='Конструктор']/parent::a")
    ORDER_FEED_TAB = (By.XPATH, "//p[text()='Лента Заказов']/parent::a")
    
    # Разделы конструктора
    BUN_TAB = (By.XPATH, "//span[text()='Булки']/parent::div")
    SAUCE_TAB = (By.XPATH, "//span[text()='Соусы']/parent::div")
    FILLING_TAB = (By.XPATH, "//span[text()='Начинки']/parent::div")
    
    # Ингредиенты
    TRADITIONAL_GALACTIC_SAUCE = (By.XPATH, "//p[text()='Соус традиционный галактический']")
    BUN_STELLAR_CRUST = (By.XPATH, "//p[text()='Краторная булка N-200i']")
    BUN_FLUORESCENT_RICE = (By.XPATH, "//p[text()='Флюоресцентная булка R2-D3']")
    BUN_BY_TEXT = (By.XPATH, "//p[contains(text(), 'булка')]")
    
    # Счетчики ингредиентов
    TRADITIONAL_SAUCE_COUNTER = (By.XPATH, "//p[text()='Соус традиционный галактический']/../div[1]/p")
    
    # Модальное окно ингредиента
    MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal__contentBox__sCy8X')]")
    MODAL_CLOSE = (By.XPATH, "//button[contains(@class, 'Modal_modal__close_modified__3V5XS')]")
    MODAL_TITLE = (By.XPATH, "//div[contains(@class, 'Modal_modal__contentBox__sCy8X')]//h2")
    MODAL_INGREDIENT_NAME = (By.XPATH, "//div[contains(@class, 'Modal_modal__contentBox__sCy8X')]//p")
    
    # Конструктор заказа
    #BASKET = (By.XPATH, "//*[contains(text(), 'Перетяните булочку сюда')]/ancestor::ul")
    BASKET = (By.CSS_SELECTOR, "section[class*='BurgerConstructor_basket'] > ul")
    CONSTRUCTOR_ELEMENT = (By.CSS_SELECTOR, ".constructor-element")
    ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    
    # Авторизация
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти в аккаунт']")
    EMAIL_INPUT = (By.NAME, "name")
    PASSWORD_INPUT = (By.NAME, "Пароль")
    LOGIN_SUBMIT = (By.XPATH, "//button[text()='Войти']")
    
    # Модальное окно Идентификатор заказа
    ORDER_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal__container__Wo2l_')]")
    ORDER_MODAL_CLOSE = (By.XPATH, "//div[contains(@class, 'Modal_modal__container__Wo2l_')]//button[contains(@class, 'Modal_modal__close_modified__3V5XS')]")
    ORDER_MODAL_NUMBER = (By.XPATH, "//div[contains(@class, 'Modal_modal__container__Wo2l_')]//h2[contains(@class, 'Modal_modal__title__2L34m')]")