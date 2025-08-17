from selenium.webdriver.common.by import By
from src.utils.helpers import BasePage

class CustomerLoginPage(BasePage):
    USER_SELECT = (By.ID, "userSelect")

    def login_as(self, customer_display_name: str):
        self.select_by_visible_text(*self.USER_SELECT, visible_text=customer_display_name)
        self.click_button_by_text("Login")
        from src.pages.account_page import AccountPage
        return AccountPage(self.driver)
