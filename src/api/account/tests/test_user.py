import allure
import pytest
from jsonschema import validate

from src import user_name, password
from src.api.account.account_api import AccountApi


@allure.parent_suite('demo-qa')
@allure.suite('API')
@allure.sub_suite('/User')
@allure.title('Успешная регистрация пользователя 200')
def test_user_registration_200(user_created_201, delete_user):
    account_api = AccountApi(user_name, password)
    with allure.step('Отправка запроса'):
        response = account_api.user()
    with allure.step('Проверка статус-кода 201'):
        assert response.status_code == 201
    with allure.step('Проверка схемы ответа'):
        validate(instance=response.json(), schema=user_created_201)


@allure.parent_suite('demo-qa')
@allure.suite('API')
@allure.sub_suite('/User')
@allure.title('Регистрация уже зарегистрированного пользователя')
def test_existed_user_registration_406(user_already_exists_406):
    account_api = AccountApi(user_name, password)
    with allure.step('Отправка запроса на регистрацию пользователя'):
        account_api.user()
    with allure.step('Отправка запроса на повторную регистрацию пользователя'):
        response = account_api.user()
    with allure.step('Проверка статус-кода 406'):
        assert response.status_code == 406
    with allure.step('Проверка схемы ответа'):
        validate(instance=response.json(), schema=user_already_exists_406)


@allure.parent_suite('demo-qa')
@allure.suite('API')
@allure.sub_suite('/User')
@allure.title('Валидация требований к паролю')
@pytest.mark.parametrize('description,password_', [
    ('Invalid: less than 8 characters', 'short1!'),
    ('Invalid: no letters', '12345678!'),
    ('Invalid: no nu,bers', 'ABCDEFGH!'),
])
def test_password_validation_406(description, password_, password_validation_400):
    account_api = AccountApi(user_name, password_)
    with allure.step('Отправка запроса на регистрацию пользователя'):
        response = account_api.user()
    with allure.step('Проверка статус-кода 400'):
        assert response.status_code == 400
    with allure.step('Проверка схемы ответа'):
        validate(instance=response.json(), schema=password_validation_400)


@allure.parent_suite('demo-qa')
@allure.suite('API')
@allure.sub_suite('/User')
@allure.title('Bad request invalid body form 400')
@pytest.mark.parametrize('body', [
    {},
    {'aboba': 2},
    {'userName': 'noPassword'},
    {'password': 'noName'}
])
def test_invalid_body(body, bad_request_400):
    account_api = AccountApi(user_name, password)
    with allure.step('Отправка запроса на регистрацию пользователя'):
        response = account_api.user(body)
    with allure.step('Проверка статус-кода 400'):
        assert response.status_code == 400
    with allure.step('Проверка схемы ответа'):
        validate(instance=response.json(), schema=bad_request_400)


if __name__ == '__main__':
    pass
