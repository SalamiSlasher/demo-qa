#!/usr/bin/env python
# -*- coding: utf-8 -*-
import allure
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

    @allure.parent_suite('demo-qa')
    @allure.suite('Selenium-Web')
    @allure.title('Успешная отправка формы')
    def test_greenway(self):
        test_data = RandomFormData()
        allure.attach(str(test_data), 'test-data', allure.attachment_type.JSON)

        page = AutomationPracticePage(self.driver) \
            .input_first_name(test_data.first_name) \
            .input_last_name(test_data.last_name) \
            .input_user_email(test_data.email) \
            .input_user_number(test_data.mobile_phone) \
            .click_label_gender(test_data.gender) \
            .click_hobbies_checkbox(test_data.hobbies) \
            .input_textarea_current_address(test_data.current_address) \
            .click_submit_btn()

        with allure.step('проверка соответствия полей'):
            submitted_info = page.get_submit_matrix()
            for key, val in submitted_info.items():
                if key in test_data.to_dict():
                    expected_value = test_data.to_dict()[key]
                    with allure.step(
                            f'Проверка, что поле "{key}" с значением "{val}" совпадает с введенным "{expected_value}"'):
                        assert str(expected_value) == str(submitted_info[key])

    @allure.parent_suite('demo-qa')
    @allure.suite('Selenium-Web')
    @allure.title('Валидация обязательных полей при нажатии на Submit')
    def test_validation_error(self):
        page = AutomationPracticePage(self.driver).click_submit_btn()
        with allure.step('Проверяем, что не форма не отправилась'):
            x = self.driver.find_elements(*page.success_submit_title)
            assert not self.driver.find_elements(*page.success_submit_title)

    @allure.parent_suite('demo-qa')
    @allure.suite('Selenium-Web')
    @allure.title('Неуспешная отправка форма с невалидным email')
    def test_validation_email(self):
        test_data = RandomFormData()
        test_data.email = test_data.email.replace('@', '')

        allure.attach(str(test_data), 'test-data', allure.attachment_type.JSON)

        page = AutomationPracticePage(self.driver) \
            .input_first_name(test_data.first_name) \
            .input_last_name(test_data.last_name) \
            .input_user_email(test_data.email) \
            .input_user_number(test_data.mobile_phone) \
            .click_label_gender(test_data.gender) \
            .click_hobbies_checkbox(test_data.hobbies) \
            .input_textarea_current_address(test_data.current_address) \
            .click_submit_btn()

        with allure.step('Проверяем, что не форма не отправилась'):
            assert not self.driver.find_elements(*page.success_submit_title)

    @allure.parent_suite('demo-qa')
    @allure.suite('Selenium-Web')
    @allure.title('Неуспешная отправка формы с невалидным номером телефона')
    def test_validation_phone(self):
        test_data = RandomFormData()
        test_data.mobile_phone = "12345 6789"

        allure.attach(str(test_data), 'test-data', allure.attachment_type.JSON)

        page = AutomationPracticePage(self.driver) \
            .input_first_name(test_data.first_name) \
            .input_last_name(test_data.last_name) \
            .input_user_email(test_data.email) \
            .input_user_number(test_data.mobile_phone) \
            .click_label_gender(test_data.gender) \
            .click_hobbies_checkbox(test_data.hobbies) \
            .input_textarea_current_address(test_data.current_address) \
            .click_submit_btn()

        with allure.step('Проверяем, что не форма не отправилась'):
            assert not self.driver.find_elements(*page.success_submit_title)

    @allure.parent_suite('demo-qa')
    @allure.suite('Selenium-Web')
    @allure.title('Загрузка файла')
    @pytest.mark.parametrize(
        'file_path', [__file__]
    )
    def test_file_upload(self, file_path):
        test_data = RandomFormData()
        allure.attach(str(test_data), 'test-data', allure.attachment_type.JSON)

        page = AutomationPracticePage(self.driver) \
            .input_first_name(test_data.first_name) \
            .input_last_name(test_data.last_name) \
            .input_user_email(test_data.email) \
            .input_user_number(test_data.mobile_phone) \
            .click_label_gender(test_data.gender) \
            .click_hobbies_checkbox(test_data.hobbies) \
            .input_textarea_current_address(test_data.current_address) \
            .upload_photo(file_path) \
            .click_submit_btn()

        with allure.step('поля Picture совпадают в поле submit'):
            submitted_info = page.get_submit_matrix()
            assert submitted_info['Picture'] in file_path


if __name__ == '__main__':
    pass

