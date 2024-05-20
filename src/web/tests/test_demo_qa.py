#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from os import getenv

from src import base_url


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

            self.browser = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                options=chrome_options
            )
        else:
            self.browser = webdriver.Chrome()

        self.browser.maximize_window()
        self.browser.implicitly_wait(10)
        self.browser.get(f'{base_url}/automation-practice-form')

        yield

        self.browser.close()
        self.browser.quit()

    def test_tools_menu(self):
       print("hello world!")
