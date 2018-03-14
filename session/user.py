import boto3
import requests
from base64 import b64encode
from util.exceptions import NotAuthorizedException


class User:
    def __init__(self, app_client_id, app_client_secret, cognito_region):
        self.client = boto3.DEFAULT_SESSION.client("cognito-idp", region_name=cognito_region)
        self.app_client_id = app_client_id
        self.app_client_secret = app_client_secret
        self.user_session = {}

    def verify(self, access_token):
        try:
            self.client.get_user(
                AccessToken=access_token
            )
        except Exception as e:
            raise NotAuthorizedException

    def start_session(self, request_url, code, redirect_url, code_verifier):
        form_data = self.data(code, redirect_url, code_verifier)
        response  = requests.post(request_url, data=form_data, headers=self.headers)
        self.user_session = self._is_authorized(response)

    @property
    def access_token(self):
        return self.user_session.get('access_token', '')

    @staticmethod
    def _is_authorized(response):
        if not response.ok:
            raise NotAuthorizedException
        return response.json()

    @property
    def headers(self):
        return {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {self.basic_auth.decode()}"
        }

    @property
    def basic_auth(self):
        return b64encode(f"{self.app_client_id}:{self.app_client_secret}".encode())

    def data(self, code, redirect_url, code_verifier):
        return {
            "grant_type": "authorization_code",
            "client_id": self.app_client_id,
            "code": code,
            "redirect_uri": redirect_url,
            "code_verifier": code_verifier
        }

