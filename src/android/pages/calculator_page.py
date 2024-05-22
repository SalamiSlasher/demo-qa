import functools

import allure
import appium.webdriver.extensions.android.nativekey as native_key
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver


def allure_screenshot_step(step_name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            driver = args[0].driver

            with allure.step(step_name):
                # Перед выполнением метода
                allure.attach(driver.get_screenshot_as_png(), name="before", attachment_type=allure.attachment_type.PNG)

                result = func(*args, **kwargs)

                # После выполнения метода
                allure.attach(driver.get_screenshot_as_png(), name="after", attachment_type=allure.attachment_type.PNG)

                return result

        return wrapper

    return decorator


class CalculatorPage:
    digit_id_btn = 'com.google.android.calculator:id/digit_'
    equal_btn = 'com.google.android.calculator:id/eq'
    add_btn = 'com.google.android.calculator:id/op_add'
    sub_btn = 'com.google.android.calculator:id/op_sub'
    multiply_btn = 'com.google.android.calculator:id/op_mul'
    divide_btn = 'com.google.android.calculator:id/op_div'
    percent_btn = 'com.google.android.calculator:id/op_pct'
    factorial_btn = 'com.google.android.calculator:id/op_fact'
    calc_edit_text = 'com.google.android.calculator:id/formula'
    calc_final_view = 'com.google.android.calculator:id/result_final'
    result_preview = 'com.google.android.calculator:id/result_preview'

    def __init__(self, driver: WebDriver):
        self.driver: WebDriver = driver

    @allure_screenshot_step('Нажимаем на цифру')
    def click_digit_button(self, digit):
        self.driver.find_element(AppiumBy.ID, f'{self.digit_id_btn}{digit}').click()

    @allure_screenshot_step('Нажимаем на =')
    def click_equal_button(self):
        self.driver.find_element(AppiumBy.ID, self.equal_btn).click()

    @allure_screenshot_step('Просмотр результата ввода чисел')
    def get_editable_result(self) -> str:
        return self.driver.find_element(AppiumBy.ID, self.calc_edit_text).text

    @allure_screenshot_step('Ввод символов без использования кнопок')
    def edit_result(self, value: str):
        android_keys = native_key.AndroidKey
        for symbol in value.upper():
            symbol = f'DIGIT_{symbol}' if symbol.isdigit() else symbol
            symbol = 'MINUS' if symbol == '-' else symbol

            keycode = android_keys.__dict__[symbol]
            self.driver.execute_script('mobile: pressKey', {"keycode": keycode})

    @allure_screenshot_step('Просмотр результата вычислений')
    def get_result_view(self) -> str:
        return self.driver.find_element(AppiumBy.ID, self.calc_final_view).text

    @allure_screenshot_step('Просмотр превью вычислений')
    def get_result_preview(self) -> str:
        return self.driver.find_element(AppiumBy.ID, self.result_preview).text

    @allure_screenshot_step('Нажимаем на +')
    def click_add_button(self):
        return self.driver.find_element(AppiumBy.ID, self.add_btn).click()

    @allure_screenshot_step('Нажимаем на -')
    def click_sub_button(self):
        return self.driver.find_element(AppiumBy.ID, self.sub_btn).click()

    @allure_screenshot_step('Нажимаем на ×')
    def click_multiply_button(self):
        return self.driver.find_element(AppiumBy.ID, self.multiply_btn).click()

    @allure_screenshot_step('Нажимаем на ÷')
    def click_divide_button(self):
        return self.driver.find_element(AppiumBy.ID, self.divide_btn).click()
