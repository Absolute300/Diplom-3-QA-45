from selenium.webdriver.common.by import By


class MainPageLocators:
    CONSTRUCTOR_LINK = (
        By.XPATH,
        "//a[@href='/' and .//p[normalize-space()='Конструктор']]",
    )
    ORDER_FEED_LINK = (
        By.XPATH,
        "//a[@href='/feed' and .//p[normalize-space()='Лента Заказов']]",
    )
    CONSTRUCTOR_TITLE = (By.XPATH, "//h1[normalize-space()='Соберите бургер']")
    INGREDIENTS_SECTION = (By.CSS_SELECTOR, "section[class*='BurgerIngredients_ingredients']")
    INGREDIENTS_MENU = (By.CSS_SELECTOR, "div[class*='BurgerIngredients_ingredients__menuContainer']")
    CONSTRUCTOR_BASKET = (By.CSS_SELECTOR, "section[class*='BurgerConstructor_basket']")
    CONSTRUCTOR_DROP_TARGET = (
        By.CSS_SELECTOR,
        "section[class*='BurgerConstructor_basket'] ul[class*='BurgerConstructor_basket__list']",
    )
    ORDER_BUTTON = (By.XPATH, "//button[contains(., 'Оформить заказ')]")

    MODAL_OPENED = (By.CSS_SELECTOR, "*[class*='Modal_modal_opened']")
    MODAL_CONTAINER = (
        By.CSS_SELECTOR,
        "*[class*='Modal_modal_opened'] div[class*='Modal_modal__container']",
    )
    MODAL_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        "*[class*='Modal_modal_opened'] button[class*='Modal_modal__close']",
    )
    INGREDIENT_DETAILS_TITLE = (
        By.XPATH,
        "//*[contains(@class,'Modal_modal_opened')]//div[contains(@class,'Modal_modal__container')]//h2[normalize-space()='Детали ингредиента']",
    )

    @staticmethod
    def ingredient_card(ingredient_id):
        return By.CSS_SELECTOR, f"a[href*='{ingredient_id}']"

    @staticmethod
    def ingredient_counter(ingredient_id):
        return (
            By.XPATH,
            f"//a[contains(@href,'{ingredient_id}')]//p[contains(@class,'counter_counter__num')]",
        )

    @staticmethod
    def ingredient_counter_in_card(ingredient_id):
        return (
            By.XPATH,
            f"//a[contains(@href,'{ingredient_id}')]//p[contains(@class,'counter_counter__num')]",
        )

    @staticmethod
    def modal_text(text):
        return (
            By.XPATH,
            f"//*[contains(@class,'Modal_modal_opened')]//div[contains(@class,'Modal_modal__container')]//*[normalize-space()='{text}']",
        )