import os
from dataclasses import dataclass

@dataclass
class Config:
    """Конфигурация тестового окружения"""
    
    # Base URLs
    BASE_URL: str = os.getenv("BASE_URL", "https://stellarburgers.education-services.ru")
    
    # Timeouts
    DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "15"))
    IMPLICIT_TIMEOUT: int = int(os.getenv("IMPLICIT_TIMEOUT", "0"))
    
    # Browser settings
    BROWSER: str = os.getenv("BROWSER", "chrome")
    HEADLESS: bool = os.getenv("HEADLESS", "False").lower() in ("true", "1", "yes", "y")
    WINDOW_SIZE: str = os.getenv("WINDOW_SIZE", "1920,1080")
    
    # Test data
    TEST_EMAIL: str = os.getenv("TEST_EMAIL", "nika_test@mail.ru")
    TEST_PASSWORD: str = os.getenv("TEST_PASSWORD", "12z12z")
    
    # Allure
    ALLURE_RESULTS_DIR: str = os.getenv("ALLURE_RESULTS_DIR", "./allure-results")