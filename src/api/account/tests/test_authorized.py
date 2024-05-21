import allure
import pytest
from jsonschema import validate

from src import user_name, password
from ..account_api import AccountApi


@allure.parent_suite('demo-qa')
@allure.suite('API')
@allure.sub_suite('/Authorized')
@allure.title('Неавторизованный пользователь 200')
def test_unauthorized_user_200(recreate_user):
    account_api = AccountApi(user_name, password)
    with allure.step('Отправка запроса'):
        response = account_api.authorized()
    with allure.step('проверка на статус-код 200'):
        assert response.status_code == 200
    with allure.step('Проверка на ответ False в ответе'):
        assert response.json() is False


@allure.parent_suite('demo-qa')
@allure.suite('API')
@allure.sub_suite('/Authorized')
@allure.title('User not found 404')
@pytest.mark.parametrize('username,password_', [
    ('aboba', 'aboba'),
    (user_name, 'aboba'),
    ('aboba', 'aboba' * 300),
])
def test_unauthorized_user_404(username, password_, user_not_found_404):
    account_api = AccountApi(user_name, password_)
    with allure.step('Отправка запроса'):
        response = account_api.authorized()
    with allure.step('проверка на статус-код 404'):
        assert response.status_code == 404
    with allure.step('Проверка схемы ответа'):
        validate(instance=response.json(), schema=user_not_found_404)


@allure.parent_suite('demo-qa')
@allure.suite('API')
@allure.sub_suite('/Authorized')
@allure.title('Bad request invalid username or password 400')
@pytest.mark.parametrize('username,password_', [
    ('', ''),
    ('aboba', ''),
])
def test_unauthorized_user_400(username, password_, bad_request_400):
    account_api = AccountApi(user_name, password_)
    with allure.step('Отправка запроса'):
        response = account_api.authorized()
    with allure.step('проверка на статус-код 400'):
        assert response.status_code == 400
    with allure.step('Проверка схемы ответа'):
        validate(instance=response.json(), schema=bad_request_400)


@allure.parent_suite('demo-qa')
@allure.suite('API')
@allure.sub_suite('/Authorized')
@allure.title('Авторизованный пользователь')
def test_authorized_user_200(recreate_user):
    account_api = AccountApi(user_name, password)
    account_api.generate_token()
    with allure.step('Отправка запроса'):
        response = account_api.authorized()
    with allure.step('проверка на статус-код 200'):
        assert response.status_code == 200
    with allure.step('Проверка на ответ True в ответе'):
        assert response.json() is True


@allure.parent_suite('demo-qa')
@allure.suite('API')
@allure.sub_suite('/Authorized')
@allure.title('Bad request invalid body form 400')
@pytest.mark.parametrize('body', [
    {},
    {'aboba': 2},
    {'userName': 'noPassword'},
    {'password': 'noName'}
])
def test_authorized_user_invalid_body_400(body, bad_request_400):
    account_api = AccountApi(user_name, password)
    with allure.step('Отправка запроса'):
        response = account_api.authorized(body)
    with allure.step('проверка на статус-код 400'):
        assert response.status_code == 400
    with allure.step('Проверка схемы ответа'):
        validate(instance=response.json(), schema=bad_request_400)


if __name__ == '__main__':
    pass
