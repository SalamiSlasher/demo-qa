import functools
from enum import Enum

import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Genders(Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3


class Hobbies(Enum):
    SPORTS = 1
    READING = 2
    MUSIC = 3


def allure_screenshot_step(step_name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            driver: WebDriver = args[0].driver
            with allure.step(step_name):
                # Перед выполнением метода
                allure.attach(driver.get_screenshot_as_png(), name="before", attachment_type=allure.attachment_type.PNG)

                result = func(*args, **kwargs)

                # После выполнения метода
                allure.attach(driver.get_screenshot_as_png(), name="after", attachment_type=allure.attachment_type.PNG)

                return result

        return wrapper

    return decorator


# page_url = https://demoqa.com/automation-practice-form
class AutomationPracticePage:
    firstname_input_locator = (By.ID, "firstName")
    lastname_input_locator = (By.ID, "lastName")
    email_input_locator = (By.ID, "userEmail")
    subjects_input_locator = (By.ID, "subjectsInput")
    address_input_locator = (By.ID, "currentAddress")
    gender_input_locator_i = (By.XPATH, "//label[@for='gender-radio-{}']")
    hobbies_checkbox_locator_i = (
    By.XPATH, "//div[contains(@class, 'custom-control')][.//*[@id='hobbies-checkbox-{}']]")
    mobile_input_locator = (By.ID, "userNumber")
    submit_btn_locator = (By.ID, "submit")
    birthday_input_locator = (By.XPATH, "//*[@id='dateOfBirthInput']")
    birthdate_day_locator = (By.XPATH, "//div[@aria-label='Choose Monday, May 13th, 2024']")
    close_btn_locator = (By.ID, "closeLargeModal")
    success_submit_title = (By.ID, "example-modal-sizes-title-lg")
    state_locator = (By.ID, "state")
    upload_file_locator = (By.ID, "uploadPicture")

    def __init__(self, driver):
        self.driver: WebDriver = driver

    @allure_screenshot_step("Ввод имени")
    def input_first_name(self, firstname: str):
        self.driver.find_element(*self.firstname_input_locator).send_keys(firstname)
        return self

    @allure_screenshot_step("Ввод фамилии")
    def input_last_name(self, lastname: str):
        self.driver.find_element(*self.lastname_input_locator).send_keys(lastname)
        return self

    @allure_screenshot_step("Ввод email")
    def input_user_email(self, email: str):
        self.driver.find_element(*self.email_input_locator).send_keys(email)
        return self

    @allure_screenshot_step("Ввод предмета")
    def input_subject(self, subject: str):
        self.driver.find_element(*self.subjects_input_locator).send_keys(subject)
        return self

    @allure_screenshot_step("Ввод адреса")
    def input_textarea_current_address(self, address: str):
        self.driver.find_element(*self.address_input_locator).send_keys(address)
        return self

    @allure_screenshot_step("Выбор гендера")
    def click_label_gender(self, gender: Genders):
        locator_type, locator_value = self.gender_input_locator_i
        locator_value = locator_value.format(gender.value)

        self.driver.find_element(locator_type, locator_value).click()
        return self

    @allure_screenshot_step("Ввод номера телефона")
    def input_user_number(self, number: str):
        self.driver.find_element(*self.mobile_input_locator).send_keys(number)
        return self

    @allure_screenshot_step("Выбор хобби")
    def click_hobbies_checkbox(self, hobbies: list[Hobbies]):
        locator_type, locator_value = self.hobbies_checkbox_locator_i
        for hobbie in hobbies:
            el = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((locator_type, locator_value.format(hobbie.value)))
            )
            ActionChains(self.driver) \
                .scroll_to_element(el) \
                .perform()
            ActionChains(self.driver) \
                .scroll_by_amount(0, 100) \
                .perform()
            el.click()
        return self

    @allure_screenshot_step("Нажать на Submit")
    def click_submit_btn(self):
        submit_btn = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.submit_btn_locator)
        )
        ActionChains(self.driver).scroll_to_element(submit_btn).perform()
        ActionChains(self.driver).scroll_by_amount(0, 1000).perform()
        submit_btn.click()
        return self

    @allure_screenshot_step("Нажать на дату рождения")
    def click_birthdate(self, birthdate: str):
        self.driver.find_element(*self.birthday_input_locator).click()
        self.driver.find_element(*self.birthday_input_locator).clear()
        self.driver.find_element(*self.birthday_input_locator).send_keys(birthdate)
        return self

    @allure_screenshot_step("Полученние данных с таблицы")
    def get_submit_matrix(self) -> dict[str, str]:
        elements = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//tr'))
        )

        d = {}
        for i in range(1, len(elements)):
            key, val = [el.text for el in elements[i].find_elements(By.XPATH, 'td')]
            d[key] = val
        return d

    @allure_screenshot_step("Загрузка файла")
    def upload_photo(self, file_path: str):
        upload_file_el = self.driver.find_element(*self.upload_file_locator)
        upload_file_el.send_keys(file_path)
        return self
