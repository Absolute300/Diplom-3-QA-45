# config.py

class Config:
    """Конфигурация тестового окружения и URL приложения."""

    @classmethod
    def build_url(cls, url_part: str = "") -> str:
        """
        Строит полный URL на основе части пути.
        Умеет обрабатывать:
        - Пустые значения
        - Относительные пути (login, register)
        - Полные URL (если вдруг переданы)
        - Удаляет лишние слеши
        """
        if not url_part:
            return cls.BASE_URL.rstrip('/')

        url_part = url_part.strip('/')

        # Если уже передан полный URL, просто нормализуем его
        if url_part.startswith('http'):
            return url_part.rstrip('/')

        # Собираем URL из базового и переданной части
        return f"{cls.BASE_URL.rstrip('/')}/{url_part}"


    # Базовые настройки
    BASE_URL = "https://stellarburgers.nomoreparties.site"
    DEFAULT_TIMEOUT = 10
    FIREFOX_TIMEOUT = 15
    BROWSER_WINDOW_SIZE = "1920x1080"

    # Основные URL страниц
    LOGIN_URL = f"{BASE_URL}/login"
    REGISTER_URL = f"{BASE_URL}/register"
    FORGOT_PASSWORD_URL = f"{BASE_URL}/forgot-password"
    RESET_PASSWORD_URL = f"{BASE_URL}/reset-password"
    PROFILE_URL = f"{BASE_URL}/account/profile"
    ORDER_FEED_URL = f"{BASE_URL}/feed"
    ORDER_HISTORY_URL = f"{BASE_URL}/account/order-history"
    MAIN_PAGE_URL = BASE_URL

    # API Endpoints
    API_BASE = "/api"
    API_AUTH_REGISTER = f"{API_BASE}/auth/register"
    API_AUTH_LOGIN = f"{API_BASE}/auth/login"
    API_AUTH_USER = f"{API_BASE}/auth/user"
    API_AUTH_LOGOUT = f"{API_BASE}/auth/logout"
    API_ORDERS = f"{API_BASE}/orders"
    API_INGREDIENTS = f"{API_BASE}/ingredients"


    # Тестовые данные пользователя
    class TestData:
        DEFAULT_PASSWORD = "Password123"
        DEFAULT_NAME = "Test User"

        @staticmethod
        def generate_email():
            import uuid
            return f"user_{uuid.uuid4().hex[:8]}@example.com"

    # Настройки отчетов
    ALLURE_RESULTS_DIR = "allure-results"

# Экземпляр конфигурации для использования в проекте
config = Config()