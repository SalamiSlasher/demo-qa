import json

import allure
from requests import Session, Response

from src import base_url
from src.api.account.models.authorized_model import AuthorizedModel


def try_beautify(response: Response) -> str:
    try:
        return json.dumps(response.json(), indent=4, ensure_ascii=False)
    except:
        return response.text


class AccountApi:
    def __init__(self, user_name, password):
        self.session = Session()
        self.url = f'{base_url}/Account/v1'

        self.user_name = user_name
        self.password = password

        self.session.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        self.correct_auth_model = AuthorizedModel(**{
            'userName': self.user_name,
            'password': self.password
        }).dict()

    def authorized(self, body: AuthorizedModel = None) -> Response:
        endpoint = f'{self.url}/Authorized'
        body = self.correct_auth_model if body is None else body

        allure.attach(endpoint, 'endpoint', allure.attachment_type.TEXT)
        allure.attach(json.dumps(self.session.headers, indent=4, ensure_ascii=False), 'request headers',
                      allure.attachment_type.JSON)
        allure.attach(json.dumps(body, indent=4, ensure_ascii=False), 'request body', allure.attachment_type.JSON)

        response = self.session.post(endpoint, json=body)

        allure.attach(str(response.status_code), 'response status code', allure.attachment_type.TEXT)
        allure.attach(json.dumps(response.headers.__dict__, indent=4, ensure_ascii=False), 'response headers',
                      allure.attachment_type.JSON)
        allure.attach(try_beautify(response), 'response body', allure.attachment_type.JSON)

        return response

    def generate_token(self, body: AuthorizedModel = None) -> Response:
        endpoint = f'{self.url}/GenerateToken'
        body = self.correct_auth_model if body is None else body

        allure.attach(endpoint, 'endpoint', allure.attachment_type.TEXT)
        allure.attach(json.dumps(self.session.headers, indent=4, ensure_ascii=False), 'request headers',
                      allure.attachment_type.JSON)
        allure.attach(json.dumps(body, indent=4, ensure_ascii=False), 'request body', allure.attachment_type.JSON)

        response = self.session.post(endpoint, json=body)

        allure.attach(str(response.status_code), 'response status code', allure.attachment_type.TEXT)
        allure.attach(json.dumps(response.headers.__dict__, indent=4, ensure_ascii=False), 'response headers',
                      allure.attachment_type.JSON)
        allure.attach(try_beautify(response), 'response body', allure.attachment_type.JSON)

        return response

    def user(self, body: AuthorizedModel = None) -> Response:
        endpoint = f'{self.url}/User'
        body = self.correct_auth_model if body is None else body

        allure.attach(endpoint, 'endpoint', allure.attachment_type.TEXT)
        allure.attach(json.dumps(self.session.headers, indent=4, ensure_ascii=False), 'request headers',
                      allure.attachment_type.JSON)
        allure.attach(json.dumps(body, indent=4, ensure_ascii=False), 'request body', allure.attachment_type.JSON)

        response = self.session.post(endpoint, json=body)

        allure.attach(str(response.status_code), 'response status code', allure.attachment_type.TEXT)
        allure.attach(json.dumps(response.headers.__dict__, indent=4, ensure_ascii=False), 'response headers',
                      allure.attachment_type.JSON)
        allure.attach(try_beautify(response), 'response body', allure.attachment_type.JSON)

        return response

    def delete_by_uuid(self, uuid: str, token: str) -> Response:
        endpoint = f'{self.url}/User/{uuid}'
        headers = self.session.headers.copy()
        headers['Authorization'] = f'Bearer {token}'

        allure.attach(endpoint, 'endpoint', allure.attachment_type.TEXT)
        allure.attach(str(headers), 'request headers', allure.attachment_type.JSON)

        response = self.session.delete(endpoint, headers=headers)

        allure.attach(str(response.status_code), 'response status code', allure.attachment_type.TEXT)
        allure.attach(json.dumps(response.headers.__dict__, indent=4, ensure_ascii=False), 'response headers',
                      allure.attachment_type.JSON)
        allure.attach(try_beautify(response), 'response body', allure.attachment_type.JSON)

        return response

    def get_by_uuid(self, uuid: str) -> Response:
        endpoint = f'{self.url}/User/{uuid}'

        allure.attach(endpoint, 'endpoint', allure.attachment_type.TEXT)
        allure.attach(json.dumps(self.session.headers, indent=4, ensure_ascii=False), 'request headers',
                      allure.attachment_type.JSON)

        response = self.session.get(endpoint)

        allure.attach(str(response.status_code), 'response status code', allure.attachment_type.TEXT)
        allure.attach(json.dumps(response.headers.__dict__, indent=4, ensure_ascii=False), 'response headers',
                      allure.attachment_type.JSON)
        allure.attach(try_beautify(response), 'response body', allure.attachment_type.JSON)

        return response

    def login(self, body: AuthorizedModel = None) -> Response:
        endpoint = f'{self.url}/Login'
        body = self.correct_auth_model if body is None else body

        allure.attach(endpoint, 'endpoint', allure.attachment_type.TEXT)
        allure.attach(json.dumps(self.session.headers, indent=4, ensure_ascii=False), 'request headers',
                      allure.attachment_type.JSON)
        allure.attach(json.dumps(body, indent=4, ensure_ascii=False), 'request body', allure.attachment_type.JSON)

        response = self.session.post(endpoint, json=body)

        allure.attach(str(response.status_code), 'response status code', allure.attachment_type.TEXT)
        allure.attach(json.dumps(response.headers.__dict__, indent=4, ensure_ascii=False), 'response headers',
                      allure.attachment_type.JSON)
        allure.attach(try_beautify(response), 'response body', allure.attachment_type.JSON)

        return response
