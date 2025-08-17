import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def base_url():
    return "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/"

@pytest.fixture(scope="session")
def driver():
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    keep_open = os.getenv("KEEP_BROWSER_OPEN", "true").lower() != "false"

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,900")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-allow-origins=*")

    if keep_open and not headless:
        options.add_experimental_option("detach", True)

    drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    drv.implicitly_wait(0)

    try:
        yield drv
    finally:
        if keep_open and not headless:
            return
        try:
            drv.quit()
        except Exception:
            pass
