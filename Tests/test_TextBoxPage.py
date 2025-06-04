from Config.config import TestData
from Pages.TextBoxPage import TextBoxPage
from Tests.test_base import BaseTest


class TestTextBoxPage(BaseTest):
    text_box_page = None

    def test_form_title_visibility(self):
        self.boilerplate()
        result = self.text_box_page.get_form_title()
        assert result, "Form title is not visible. Failed"
        print("Title is visible. Success")

    def test_text_box_form(self):
        self.boilerplate()
        result: dict = self.text_box_page.fill_in_form()
        for i in result.keys():
            if i == "name":
                assert TestData.username in result.get(i), "Incorrect name displayed in the output"
            if i == "email":
                assert TestData.user_email in result.get(i), "Incorrect email displayed in the output"
            if i == "current_address":
                assert TestData.current_address in result.get(i), "Incorrect current address displayed in the output"
            if i == "permanent_address":
                assert TestData.permanent_address in result.get(i), "Incorrect permanent address displayed in the output"
        print("Test is successful")

    def test_text_box_form_with_invalid_email(self):
        self.boilerplate()
        result: str = self.text_box_page.fill_in_email_field(TestData.invalid_email)
        assert "error" in result, "Inputting invalid email wasn't validated. Fail"
        print("Validation success")

    def boilerplate(self):
        if self.text_box_page:
            pass
        else:
            self.text_box_page = TextBoxPage(self.driver)
            self.text_box_page.scroll_to_form()

