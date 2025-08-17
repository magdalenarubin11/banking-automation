from selenium.webdriver.common.by import By
from src.utils.helpers import BasePage

class HomePage(BasePage):
    def open(self, base_url: str):
        self.driver.get(base_url)
        return self

    def go_manager(self):
        self.click_button_by_text("Bank Manager Login")
        return self

    def go_customer(self):
        self.click_button_by_text("Customer Login")
        return self

    def go_home(self):
        self.click_button_by_text("Home")
        return self
