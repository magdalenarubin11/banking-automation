import os, time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

DEFAULT_TIMEOUT = 15

def _get_slowmo_seconds():
    """Built-in slow-mo: default 600ms; can override with SLOWMO_MS env."""
    import os
    try:
        ms = int(os.getenv("SLOWMO_MS", "600"))  # DEFAULT: 600ms
    except ValueError:
        ms = 600
    return max(ms, 0) / 1000.0

class BasePage:
    def __init__(self, driver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self._slowmo = _get_slowmo_seconds()

    def _after_action_pause(self):
        if self._slowmo > 0:
            time.sleep(self._slowmo)

    def click_button_by_text(self, text: str):
        locator = (By.XPATH, f"//button[normalize-space()='{text}']")
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        self._after_action_pause()
        return self

    def click_tab_by_text(self, text: str):
        return self.click_button_by_text(text)

    def type(self, by, selector, value: str, clear: bool = True):
        el = self.wait.until(EC.visibility_of_element_located((by, selector)))
        if clear:
            el.clear()
        self._after_action_pause()
        el.send_keys(value)
        self._after_action_pause()
        return el

    def select_by_visible_text(self, by, selector, visible_text: str):
        el = self.wait.until(EC.visibility_of_element_located((by, selector)))
        Select(el).select_by_visible_text(visible_text)
        self._after_action_pause()
        return el

    def accept_alert_and_get_text(self):
        try:
            alert = self.wait.until(EC.alert_is_present())
            text = alert.text
            alert.accept()
            self._after_action_pause()
            return text
        except TimeoutException:
            return None

    def find(self, by, selector):
        el = self.wait.until(EC.visibility_of_element_located((by, selector)))
        return el

    def find_all(self, by, selector):
        self.wait.until(EC.presence_of_element_located((by, selector)))
        return self.driver.find_elements(by, selector)

def wait_for_text(driver, locator, text, timeout: int = DEFAULT_TIMEOUT):
    WebDriverWait(driver, timeout).until(EC.text_to_be_present_in_element(locator, text))

def wait_for_any_text(driver, locator, substrings, timeout: int = DEFAULT_TIMEOUT):
    """Wait until an element located by locator contains ANY of the provided substrings.
    Returns the final text of the element.
    """
    end_time = time.monotonic() + timeout
    last = ""
    while time.monotonic() < end_time:
        try:
            el = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(locator))
            last = el.text or ""
            if any(s in last for s in substrings):
                return last
        except TimeoutException:
            pass
        time.sleep(0.25)
    raise TimeoutException(f"Text not found in element. Expected any of {substrings}, last seen: '{last}'")

def wait_for_balance_value(driver, expected_value: int, timeout: int = DEFAULT_TIMEOUT):
    """Wait until page shows 'Balance : <expected_value>' anywhere (tolerates spaces/nbsp)."""
    import re, time
    body = (By.TAG_NAME, "body")
    patt = re.compile(rf"Balance\s*:?[\s\u00A0]*{expected_value}\b", flags=re.IGNORECASE)
    end = time.monotonic() + timeout
    last = ""
    while time.monotonic() < end:
        try:
            el = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(body))
            last = el.text or ""
            if patt.search(last):
                return True
        except TimeoutException:
            pass
        time.sleep(0.2)
    raise TimeoutException(f"Balance did not reach expected value {expected_value}. Last seen snippet: '{last[:80]}'")
