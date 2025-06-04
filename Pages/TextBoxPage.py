import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from Config.config import TestData
from Pages.BasePage import BasePage


class TextBoxPage(BasePage):
    SUBMIT_BUTTON = (By.ID, "submit")
    NAME_FIELD = (By.ID, "userName")
    EMAIL_FIELD = (By.ID, "userEmail")
    CURRENT_ADDRESS_FIELD = (By.ID, "currentAddress")
    PERMANENT_ADDRESS_FIELD = (By.ID, "permanentAddress")
    OUTPUT_FIELD = (By.ID, "output")
    NAME_OUTPUT = (By.ID, "name")
    EMAIL_OUTPUT = (By.ID, "email")
    FORM_TTTLE = (By.CLASS_NAME, "text-center")

    def get_form_title(self) -> bool:
        title: bool = self.is_visible(self.FORM_TTTLE)
        return title

    def scroll_to_form(self):
        self.do_scroll_from_element_by_amount(self.NAME_FIELD)

    def fill_in_form(self) -> dict | None:
        self.do_send_keys(self.NAME_FIELD, TestData.username)
        self.do_send_keys(self.EMAIL_FIELD, TestData.user_email)
        self.do_send_keys(self.CURRENT_ADDRESS_FIELD, TestData.current_address)
        self.do_send_keys(self.PERMANENT_ADDRESS_FIELD, TestData.permanent_address)
        self.do_click(self.SUBMIT_BUTTON)
        time.sleep(0.1)
        name_output = self.get_element_text(self.NAME_OUTPUT)
        time.sleep(0.1)
        email_output = self.get_element_text(self.EMAIL_OUTPUT)
        time.sleep(0.1)
        cur_addr = self.get_element_text(self.CURRENT_ADDRESS_FIELD)
        time.sleep(0.1)
        perm_addr = self.get_element_text(self.PERMANENT_ADDRESS_FIELD)
        return dict(name=name_output, email=email_output, current_address=cur_addr, permenant_address=perm_addr)

    def fill_in_email_field(self, email):
        self.do_send_keys(self.EMAIL_FIELD, email)
        self.do_click(self.SUBMIT_BUTTON)
        el: WebElement = self.get_element(self.EMAIL_FIELD)
        return el.get_attribute('class')
