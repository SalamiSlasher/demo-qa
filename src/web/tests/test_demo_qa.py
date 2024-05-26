#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver

from src import base_url
from src.web.pages.automation_practice_form import AutomationPracticePage
from src.web.utils.form_data_generator import RandomFormData


class TestDemoQa:
    # 1. Check browser configuration in browser_setup_and_teardown
    # 2. Run 'Selenium Tests' configuration
    # 3. Test report will be created in reports/ directory

    @pytest.fixture(autouse=True)
    def browser_setup_and_teardown(self):
        self.use_selenoid = True  # set to True to run tests with Selenoid
        if self.use_selenoid:
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--window-size=1920,1080")

            self.driver: WebDriver = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                options=chrome_options
            )
        else:
            self.driver: WebDriver = webdriver.Chrome()

        self.driver.maximize_window()
        self.driver.implicitly_wait(3)
        self.driver.get(f'{base_url}/automation-practice-form')

        yield

        self.driver.close()
        self.driver.quit()

    def test_greenway(self):
        test_data = RandomFormData()

        AutomationPracticePage(self.driver) \
            .input_first_name(test_data.first_name) \
            .input_last_name(test_data.last_name) \
            .input_user_email(test_data.email) \
            .click_label_gender(test_data.gender) \
            .input_user_number(test_data.mobile_phone) \
            .click_hobbies_checkbox(test_data.hobbies) \
            .input_textarea_current_address(test_data.current_address) \
            .click_submit_btn()


if __name__ == '__main__':
    pass
