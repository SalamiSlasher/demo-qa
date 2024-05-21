import allure
from requests import Session

from src import base_url
from src.api.account.models.authorized_model import AuthorizedModel


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

    def authorized(self, body: AuthorizedModel = None):
        endpoint = f'{self.url}/Authorized'
        body = self.correct_auth_model if body is None else body

        allure.attach(endpoint, 'endpoint', allure.attachment_type.TEXT)
        allure.attach(str(self.session.headers), 'request headers', allure.attachment_type.JSON)
        allure.attach(str(body), 'request body', allure.attachment_type.JSON)

        response = self.session.post(endpoint, json=body)

        allure.attach(str(response.status_code), 'response status code', allure.attachment_type.TEXT)
        allure.attach(str(response.headers), 'response headers', allure.attachment_type.JSON)
        allure.attach(response.text, 'response body', allure.attachment_type.TEXT)

        return response

    def generate_token(self, body: AuthorizedModel = None):
        endpoint = f'{self.url}/GenerateToken'
        body = self.correct_auth_model if body is None else body

        allure.attach(endpoint, 'endpoint', allure.attachment_type.TEXT)
        allure.attach(str(self.session.headers), 'request headers', allure.attachment_type.JSON)
        allure.attach(str(body), 'request body', allure.attachment_type.JSON)

        response = self.session.post(endpoint, json=body)

        allure.attach(str(response.status_code), 'response status code', allure.attachment_type.TEXT)
        allure.attach(str(response.headers), 'response headers', allure.attachment_type.JSON)
        allure.attach(response.text, 'response body', allure.attachment_type.TEXT)

        return response

    def user(self, body: AuthorizedModel = None):
        endpoint = f'{self.url}/User'
        body = self.correct_auth_model if body is None else body

        allure.attach(endpoint, 'endpoint', allure.attachment_type.TEXT)
        allure.attach(str(self.session.headers), 'request headers', allure.attachment_type.JSON)
        allure.attach(str(body), 'request body', allure.attachment_type.JSON)

        response = self.session.post(endpoint, json=body)

        allure.attach(str(response.status_code), 'response status code', allure.attachment_type.TEXT)
        allure.attach(str(response.headers), 'response headers', allure.attachment_type.JSON)
        allure.attach(response.text, 'response body', allure.attachment_type.TEXT)

        return response

    def delete_by_uuid(self, uuid: str, token: str):
        endpoint = f'{self.url}/User/{uuid}'
        headers = self.session.headers.copy()
        headers['Authorization'] = f'Bearer {token}'

        allure.attach(endpoint, 'endpoint', allure.attachment_type.TEXT)
        allure.attach(str(headers), 'request headers', allure.attachment_type.JSON)

        response = self.session.delete(endpoint, headers=headers)

        allure.attach(str(response.status_code), 'response status code', allure.attachment_type.TEXT)
        allure.attach(str(response.headers), 'response headers', allure.attachment_type.JSON)
        allure.attach(response.text, 'response body', allure.attachment_type.TEXT)

        return response

    def get_by_uuid(self, uuid: str):
        endpoint = f'{self.url}/User/{uuid}'

        allure.attach(endpoint, 'endpoint', allure.attachment_type.TEXT)
        allure.attach(str(self.session.headers), 'request headers', allure.attachment_type.JSON)

        response = self.session.get(endpoint)

        allure.attach(str(response.status_code), 'response status code', allure.attachment_type.TEXT)
        allure.attach(str(response.headers), 'response headers', allure.attachment_type.JSON)
        allure.attach(response.text, 'response body', allure.attachment_type.TEXT)

        return response

    def login(self, body: AuthorizedModel = None):
        endpoint = f'{self.url}/Login'
        body = self.correct_auth_model if body is None else body

        allure.attach(endpoint, 'endpoint', allure.attachment_type.TEXT)
        allure.attach(str(self.session.headers), 'request headers', allure.attachment_type.JSON)
        allure.attach(str(body), 'request body', allure.attachment_type.JSON)

        response = self.session.post(endpoint, json=body)

        allure.attach(str(response.status_code), 'response status code', allure.attachment_type.TEXT)
        allure.attach(str(response.headers), 'response headers', allure.attachment_type.JSON)
        allure.attach(response.text, 'response body', allure.attachment_type.TEXT)

        return response
