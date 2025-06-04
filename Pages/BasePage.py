from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

"""This class is a parent class of all pages"""
"""it contains all the generic methods and utilities for all the pages"""


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def do_click(self, by_locator: tuple[str, str]) -> "Clicks a button":
        try:
            WebDriverWait(self.driver, timeout=10, poll_frequency=2, ignored_exceptions=[NoSuchElementException]).until(EC.element_to_be_clickable(by_locator)).click()
        except TimeoutException:
            print("Element is not clickable, something went wrong with external or internal server")
            return None
        except StaleElementReferenceException:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(by_locator)).click()

    def do_send_keys(self, by_locator, text):
        try:
            WebDriverWait(self.driver,timeout=10, poll_frequency=2, ignored_exceptions=[NoSuchElementException]).until(EC.visibility_of_element_located(by_locator)).send_keys(text)
        except TimeoutException:
            print("Element is not visible, something went wrong with external or internal server")
            return None
        except StaleElementReferenceException:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(by_locator)).click()

    def press_enter(self, by_locator):
        try:
            WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(by_locator)).send_keys(Keys.RETURN)
        except TimeoutException:
            print("Element is not visible, something went wrong with external or internal server")
            return None
        except StaleElementReferenceException:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(by_locator)).click()

    def get_element_text(self, by_locator) -> str | None:
        try:
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
            if element.text:
                return element.text
            return element.get_attribute('value')
        except TimeoutException:
            print("Element text not found, something went wrong with external or internal server")
            return None
        except StaleElementReferenceException:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(by_locator)).click()

    def get_element(self, by_locator) -> WebElement | None:
        try:
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
            return element
        except TimeoutException:
            print("Element text not found, something went wrong with external or internal server")
            return None

    def get_element_text_sign_out(self, by_locator) -> str | None:
        try:
            element = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(by_locator))
            if element.text:
                return element.text
            return element.get_attribute('value')
        except TimeoutException:
            print("Element text not found, something went wrong with external or internal server")
            return None

    def is_visible(self, by_locator):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
            return bool(element)
        except TimeoutException:
            print("Element is not visible, something went wrong with external or internal server")
            return None

    def is_visible_sign_out(self, by_locator):
        try:
            element = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(by_locator))
            return bool(element)
        except TimeoutException:
            print("Element is not visible, something went wrong with external or internal server")
            return None

    def get_title(self, title):
        try:
            WebDriverWait(self.driver, 15).until(EC.title_is(title))
            return self.driver.title
        except TimeoutException:
            print("Title not found, something went wrong with external or internal server")
            return None

    def get_element_link(self, by_locator):
        try:
            element_link = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(by_locator)). \
                get_attribute("href")
            return element_link
        except TimeoutException:
            print("Element link not found, something went wrong with external or internal server")
            return None

    def select_by_visible_text(self, by_locator: tuple[str, str], text: str) -> object:
        try:
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
            sel = Select(element)
            sel.select_by_visible_text(text)
            print("Item has been selected")
            return sel
        except TimeoutException:
            print("Element link not found, something went wrong with external or internal server")
            return None

    def select_by_index(self, by_locator: tuple[str, str], index: int) -> object:
        try:
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
            sel = Select(element)
            sel.select_by_index(index)
            print("Item has been selected")
            return sel
        except TimeoutException:
            print("Element link not found, something went wrong with external or internal server")
            return None

    def accept_alert(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + \
                                                'confirmation popup to appear.').switch_to.alert.accept()
        except TimeoutException:
            print("no alert")

    def cancel_alert(self):
        try:
            WebDriverWait(self.driver, timeout=10, poll_frequency=2, ignored_exceptions=[NoSuchElementException]).until(
                EC.alert_is_present(), 'Timed out waiting for PA creation ' + \
                'confirmation popup to appear.').switch_to.alert.cancel()
        except TimeoutException:
            print("no alert")

    def do_click_element_by_link_text(self, by_locator):
        try:
            WebDriverWait(self.driver, timeout=10, poll_frequency=2, ignored_exceptions=[NoSuchElementException]).until(
                EC.element_to_be_clickable(by_locator)).click()
        except TimeoutException:
            print("Element link not found, something went wrong with external or internal server")
            return None

    def do_execute_script(self, by_locator):
        try:
            elem = WebDriverWait(self.driver, timeout=10, poll_frequency=2,
                                 ignored_exceptions=[NoSuchElementException]).until(
                EC.element_to_be_clickable(by_locator))
            self.driver.execute_script("arguments[0].click()", elem)
        except TimeoutException:
            print("Element link not found, something went wrong with external or internal server")
            return None

    def do_scroll_to_element(self, by_locator):
        try:
            elem = WebDriverWait(self.driver, timeout=10, poll_frequency=2,
                                 ignored_exceptions=[NoSuchElementException]).until(
                EC.element_to_be_clickable(by_locator))
            ActionChains(self.driver) \
                .scroll_to_element(elem) \
                .perform()
        except TimeoutException:
            print("Element link not found, something went wrong with external or internal server")
            return None

    def do_scroll_from_element_by_amount(self, by_locator):
        try:
            elem = WebDriverWait(self.driver, timeout=10, poll_frequency=2, ignored_exceptions=[NoSuchElementException]).until(EC.element_to_be_clickable(by_locator))
            delta_y = elem.rect['y']
            ActionChains(self.driver).scroll_by_amount(0, delta_y).perform()
        except TimeoutException:
            print("Element link not found, something went wrong with external or internal server")
            return None
