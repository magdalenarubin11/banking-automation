from selenium.webdriver.common.by import By
from src.utils.helpers import BasePage

class ManagerPage(BasePage):
    FNAME = (By.XPATH, "//input[@ng-model='fName']")
    LNAME = (By.XPATH, "//input[@ng-model='lName']")
    POST  = (By.XPATH, "//input[@ng-model='postCd']")
    ADD_BTN = (By.XPATH, "//button[@type='submit' and normalize-space()='Add Customer']")

    OA_CUSTOMER = (By.XPATH, "//select[@ng-model='custId']")
    OA_CURRENCY = (By.XPATH, "//select[@ng-model='currency']")
    OA_PROCESS  = (By.XPATH, "//button[normalize-space()='Process']")

    def open_add_customer(self):
        self.click_tab_by_text("Add Customer")
        return self

    def add_customer(self, first: str, last: str, post: str):
        self.open_add_customer()
        self.type(*self.FNAME, value=first)
        self.type(*self.LNAME, value=last)
        self.type(*self.POST,  value=post)
        self.find(*self.ADD_BTN).click()
        return self.accept_alert_and_get_text()

    def open_open_account(self):
        self.click_tab_by_text("Open Account")
        return self

    def open_account(self, customer_display_name: str, currency: str = "Dollar"):
        self.open_open_account()
        # Select newly created customer and currency, then process
        self.select_by_visible_text(*self.OA_CUSTOMER, visible_text=customer_display_name)
        self.select_by_visible_text(*self.OA_CURRENCY, visible_text=currency)
        self.find(*self.OA_PROCESS).click()
        return self.accept_alert_and_get_text()

    def go_home(self):
        self.click_button_by_text("Home")
        return self
