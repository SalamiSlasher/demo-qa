#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import add, sub, mul
from random import randint

import allure
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from src import appium_url
from src.android.pages.calculator_page import CalculatorPage
from src.android.utils.file_utils import get_file_path

capabilities = {
    'platformName': 'Android',
    'appium:automationName': 'uiautomator2',
    'deviceName': 'Android',
    'app': get_file_path('Google_Calculator_8.6.apk', __file__),
}


class TestDemoQa:
    @pytest.fixture(autouse=True)
    def driver_setup(self):
        options = UiAutomator2Options().load_capabilities(capabilities)
        self.driver = webdriver.Remote(appium_url, options=options)
        self.driver.implicitly_wait(3)

        self.calculator_page = CalculatorPage(self.driver)

        # Начинаем запись видео
        self.driver.start_recording_screen()

        yield

        # Останавливаем запись и сохраняем видео
        video_raw = self.driver.stop_recording_screen()

        # Прикрепляем видео к отчету
        allure.attach(video_raw, name="test_video.mp4", attachment_type=allure.attachment_type.MP4)

        self.driver.quit()

    @allure.parent_suite('demo-qa')
    @allure.suite('Appium-Android')
    @allure.title('Ввод цифр от 0 до 9')
    def test_digits_btn(self):
        for i in range(10):
            self.calculator_page.click_digit_button(i)
        assert self.calculator_page.get_editable_result() == '0123456789'

    @allure.parent_suite('demo-qa')
    @allure.suite('Appium-Android')
    @allure.title('Выполнение арифметических операций над положительными числами')
    @pytest.mark.parametrize('op_symbol, operation, page_method', [
        ('+', add, CalculatorPage.click_add_button),
        ('-', sub, CalculatorPage.click_sub_button),
        ('×', mul, CalculatorPage.click_multiply_button),
    ])
    def test_math_operations(self, op_symbol, operation, page_method):
        with allure.step('Генерируем случайные числа'):
            a = randint(0, 100)
            b = randint(0, 100)
            allure.attach(str(a), 'Число а', allure.attachment_type.TEXT)
            allure.attach(str(b), 'Число b', allure.attachment_type.TEXT)
        with allure.step(f'Выполняем операцию {a} {op_symbol} {b}'):
            res_python = operation(a, b)
            allure.attach(str(res_python), 'Результат питона', allure.attachment_type.TEXT)

        with allure.step('Ввод числа а в приложение'):
            for i in str(a):
                self.calculator_page.click_digit_button(i)

        with allure.step(f'Ввод {op_symbol} в приложении'):
            page_method(self.calculator_page)

        with allure.step('Ввод числа b в приложение'):
            for i in str(b):
                self.calculator_page.click_digit_button(i)

        with allure.step('Ввод = в приложении'):
            self.calculator_page.click_equal_button()

        with allure.step('Просмотр результата в приложении'):
            res_app = int(self.calculator_page.get_result_view().replace('−', '-'))

            allure.attach(str(res_python), 'Результат приложения', allure.attachment_type.TEXT)

        with allure.step('Сравнение питонического результата с приллой'):
            assert res_python == res_app

    @allure.parent_suite('demo-qa')
    @allure.suite('Appium-Android')
    @allure.title('Деление на 0')
    def test_divide_by_zero(self):
        self.calculator_page.click_digit_button(1)
        self.calculator_page.click_divide_button()
        self.calculator_page.click_digit_button(0)
        self.calculator_page.click_equal_button()
        assert self.calculator_page.get_result_preview() == "Can't divide by 0"

    @allure.parent_suite('demo-qa')
    @allure.suite('Appium-Android')
    @allure.title('Ввод цифр в EditText вручную (не используя кнопки приложения)')
    @pytest.mark.parametrize('num', [
        str(randint(0, 100)),
        str(randint(-100, -1)),
    ])
    def test_keyboard_input_digits(self, num):
        with allure.step("Генерация случайного числа"):
            allure.attach(num, 'число', allure.attachment_type.TEXT)
        with allure.step("Ввод числа"):
            self.calculator_page.get_editable_result()
            self.calculator_page.edit_result(num)
        with allure.step("Проверка на корректность введенного числа"):
            assert self.calculator_page.get_editable_result() == num.replace('-', '−')

    @allure.parent_suite('demo-qa')
    @allure.suite('Appium-Android')
    @allure.title('Ввод невалидных символов в EditText вручную (не используя кнопки приложения)')
    def test_invalid_keyboard_input(self):
        with allure.step("Ввод невалидных символов 'aboba'"):
            self.calculator_page.edit_result('aboba')

        self.calculator_page.click_equal_button()

        with allure.step("Проверка на отображение 'format error'"):
            assert self.calculator_page.get_result_preview() == 'Format error'


if __name__ == '__main__':
    pass
