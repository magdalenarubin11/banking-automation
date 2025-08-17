from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src.utils.helpers import BasePage
import time

class TransactionsPage(BasePage):
    TABLE = (By.CSS_SELECTOR, "table.table")
    ROWS = (By.CSS_SELECTOR, "table.table tbody tr")
    RESET_BTN = (By.XPATH, "//button[normalize-space()='Reset']")

    TYPE_CELL = ".//td[3]"
    AMOUNT_CELL = ".//td[2]"

    def _ensure_loaded(self):
        self.wait.until(EC.presence_of_element_located(self.TABLE))
        time.sleep(0.3)

    def get_transactions(self):
        self._ensure_loaded()
        rows = self.find_all(*self.ROWS)
        if not rows:
            try:
                self.find(*self.RESET_BTN).click()
                time.sleep(0.3)
                rows = self.find_all(*self.ROWS)
            except Exception:
                pass

        data = []
        for r in rows:
            typ = r.find_element("xpath", self.TYPE_CELL).text.strip()
            amt = r.find_element("xpath", self.AMOUNT_CELL).text.strip()
            try:
                amt_val = int(float(amt))
            except ValueError:
                amt_val = 0
            data.append({"type": typ, "amount": amt_val})
        return data
