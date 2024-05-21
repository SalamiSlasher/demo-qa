import allure
import pytest

from src import user_name, password
from src.api.account.account_api import AccountApi


@pytest.fixture()
def delete_user():
    account_api = AccountApi(user_name, password)
    with allure.step('Проверка на существование пользователя'):
        is_exists = account_api.authorized().status_code == 200
        allure.attach(f'user exists == {is_exists}')

        if not is_exists:
            return

        with allure.step('Удаление пользователя'):
            user_id = account_api.login().json()['userId']
            token = account_api.generate_token().json()['token']
            account_api.delete_by_uuid(user_id, token)


@pytest.fixture()
def recreate_user():
    account_api = AccountApi(user_name, password)
    with allure.step('Проверка на существование пользователя'):
        is_exists = account_api.authorized().status_code == 200
        allure.attach(f'user exists == {is_exists}')

        if is_exists:
            with allure.step('Удаление пользователя'):
                user_id = account_api.login().json()['userId']
                token = account_api.generate_token().json()['token']
                account_api.delete_by_uuid(user_id, token)

        with allure.step('Регистрация пользователя'):
            account_api.user()


@pytest.fixture
def user_not_found_404():
    return {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "const": "1207"
            },
            "message": {
                "type": "string",
                "const": "User not found!"
            }
        },
        "required": ["code", "message"],
    }


@pytest.fixture
def bad_request_400():
    return {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "const": "1200"
            },
            "message": {
                "type": "string",
                "const": "UserName and Password required."
            }
        },
        "required": ["code", "message"],
    }


@pytest.fixture
def user_created_201():
    return {
        "type": "object",
        "properties": {
            "userID": {
                "type": "string",
            },
            "username": {
                "type": "string",
            },
            "books": {
                "type": "array",
                "items": {}
            }
        },
        "required": ["userID", "username", "books"],
    }


@pytest.fixture
def user_already_exists_406():
    return {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "const": "1204"
            },
            "message": {
                "type": "string",
                "const": "User exists!"
            }
        },
        "required": ["code", "message"],
    }


@pytest.fixture
def password_validation_400():
    return {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "const": "1300"
            },
            "message": {
                "type": "string",
                "const": "Passwords must have at least one non alphanumeric character, one digit ('0'-'9'), "
                         "one uppercase ('A'-'Z'), one lowercase ('a'-'z'), one special character and Password must "
                         "be eight characters or longer."
            }
        },
        "required": ["code", "message"],
    }
