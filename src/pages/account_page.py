import re, time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from src.utils.helpers import BasePage, wait_for_text, wait_for_any_text, wait_for_balance_value

class AccountPage(BasePage):
    AMOUNT_INPUT = (By.XPATH, "//form[.//input[@ng-model='amount']]//input[@ng-model='amount']")
    SUBMIT_DEPOSIT = (By.XPATH, "//form[.//input[@ng-model='amount']]//button[normalize-space()='Deposit']")
    SUBMIT_WITHDRAW = (By.XPATH, "//form[.//input[@ng-model='amount']]//button[normalize-space()='Withdraw']")
    MESSAGE = (By.XPATH, "//span[@ng-show='message' or @ng-show='errorMsg']")

    def go_transactions(self):
        self.click_tab_by_text("Transactions")
        time.sleep(0.2)
        from src.pages.transactions_page import TransactionsPage
        return TransactionsPage(self.driver)

    def go_deposit(self):
        self.click_tab_by_text("Deposit")
        time.sleep(0.2)
        return self

    def go_withdraw(self):
        self.click_tab_by_text("Withdrawl")
        time.sleep(0.2)
        return self

    def _robust_click(self, locator):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            el.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
            self.driver.execute_script("arguments[0].click();", el)
        self._after_action_pause()
        return el

    def _get_balance(self) -> int:
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        m = re.search(r"Balance\s*:?[\s\u00A0]*(\d+)", body_text, flags=re.IGNORECASE)
        if m:
            try:
                return int(m.group(1))
            except ValueError:
                pass
        return 0

    def deposit(self, amount: int):
        self.go_deposit()
        before = self._get_balance()
        self.type(*self.AMOUNT_INPUT, value=str(amount))
        self._robust_click(self.SUBMIT_DEPOSIT)
        expected = before + int(amount)
        wait_for_balance_value(self.driver, expected, timeout=20)
        return f"Deposit Successful (balance {before} -> {expected})"

    def withdraw(self, amount: int):
        self.go_withdraw()
        before = self._get_balance()
        self.type(*self.AMOUNT_INPUT, value=str(amount))
        self._robust_click(self.SUBMIT_WITHDRAW)
        expected = before - int(amount)
        wait_for_balance_value(self.driver, expected, timeout=20)
        return f"Transaction successful (balance {before} -> {expected})"
