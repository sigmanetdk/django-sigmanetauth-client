import json

import requests
from django.conf import settings

from client.factory.models import Token, UserInfo
from client.middleware.oauth import get_oauth_state_token


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SigmaNetOAuthClient(metaclass=Singleton):

    def __init__(self, require_csrf=True) -> None:
        self.require_csrf = require_csrf
        super().__init__()

    def get_authorize_url(self, request, response_type='code'):
        if self.require_csrf:
            self._ensure_oauth_state_token(request)

        state = get_oauth_state_token(request)
        return f'{settings.SIGMANET_AUTH_BASE_URL}/oauth2/authorize/' \
               f'?client_id={settings.SIGMANET_AUTH_CLIENT_ID}' \
               f'&state={state}' \
               f'&response_type={response_type}'

    def get_token(self, request, grant_type='authorization_code'):
        response = requests.post(f'{settings.SIGMANET_AUTH_BASE_URL}/oauth/token/', data={
            'authorization_code': request.GET.get('authorization_code', None),
            'grant_type': grant_type,
            'client_id': settings.SIGMANET_AUTH_CLIENT_ID,
            'client_secret': settings.SIGMANET_AUTH_CLIENT_SECRET
        })
        if response.status_code >= 300:
            return response, None
        return response, Token.from_response(self._decode(response))

    def get_userinfo(self, token):
        response = requests.get('https://auth.sigmanet.dk/oauth/userinfo/', headers={
            'Authorization': f'Bearer {token}'
        })
        if response.status_code >= 300:
            return response, None
        return response, UserInfo.from_response(self._decode(response))

    def _ensure_oauth_state_token(self, request):
        if request.session.get('_oauth_state_token', None) is None:
            raise ValueError('The session did not contain any _oauth_state_token which is required '
                             'for the request to be processed. Ensure that SIGMANET_CLIENT_LOGIN_PATH is set '
                             'correctly and OAuthValidateStateMiddleware middleware is placed in settings.MIDDLEWARE')

    def _decode(self, response):
        return json.loads(response.content.decode('utf8'))
