import pytest
import os
import stat
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config import Config

def get_chrome_driver_path():
    """Получаем правильный путь к chromedriver, игнорируя файл с уведомлениями"""
    try:
        driver_path = ChromeDriverManager().install()
        driver_dir = os.path.dirname(driver_path)
        
        # Ищем файл chromedriver в директории
        for file in os.listdir(driver_dir):
            if file == "chromedriver" or file == "chromedriver.exe" or file.startswith("chromedriver-"):
                full_path = os.path.join(driver_dir, file)
                
                # Добавляем права на выполнение (для Linux/Mac)
                if os.name != 'nt':  # не для Windows
                    st = os.stat(full_path)
                    os.chmod(full_path, st.st_mode | stat.S_IEXEC)
                
                return full_path
        
        # Если не нашли, проверяем, не является ли сам driver_path исполняемым файлом
        if os.path.isfile(driver_path) and not driver_path.endswith('THIRD_PARTY_NOTICES.chromedriver'):
            if os.name != 'nt':
                st = os.stat(driver_path)
                os.chmod(driver_path, st.st_mode | stat.S_IEXEC)
            return driver_path
        
        # Если ничего не нашли, возвращаем путь, предполагая что это директория
        final_path = os.path.join(driver_path, "chromedriver") if os.path.isdir(driver_path) else driver_path
        if os.path.exists(final_path) and os.name != 'nt':
            st = os.stat(final_path)
            os.chmod(final_path, st.st_mode | stat.S_IEXEC)
        
        return final_path
        
    except Exception as e:
        pytest.fail(f"Ошибка при получении пути к драйверу: {e}")

@pytest.fixture(params=["chrome", "firefox"], scope="function")
def driver(request):
    """Фикстура для создания драйвера с параметризацией браузеров"""
    browser_name = request.param
    
    if browser_name == "chrome":
        options = ChromeOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--window-size={Config.WINDOW_SIZE}")
        
        # Получаем правильный путь к драйверу
        driver_path = get_chrome_driver_path()
        
        service = ChromeService(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)

    elif browser_name == "firefox":
        options = FirefoxOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")
        options.add_argument(f"--width={Config.WINDOW_SIZE.split(',')[0]}")
        options.add_argument(f"--height={Config.WINDOW_SIZE.split(',')[1]}")
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

    else:
        raise ValueError(f"Неподдерживаемый браузер: {browser_name}")

    driver.implicitly_wait(0)

    yield driver
    driver.quit()