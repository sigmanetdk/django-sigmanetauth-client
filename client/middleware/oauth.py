import secrets
from threading import Lock

from django.middleware.csrf import RejectRequest
from django.conf import settings

MAX_TOKEN_LIST_SIZE = 20
lock = Lock()


class SigmaNetOAuthValidateStateMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.path[:len(settings.SIGMANET_CLIENT_LOGIN_PATH)] == settings.SIGMANET_CLIENT_LOGIN_PATH:
            state_token = secrets.token_urlsafe(nbytes=32)
            try:
                lock.acquire()
                tokens = request.session.get('_oauth_state_token', [])
                while len(tokens) >= MAX_TOKEN_LIST_SIZE:
                    tokens.pop(0)
                tokens.append(state_token)
                request.session['_oauth_state_token'] = tokens
            finally:
                lock.release()

        if request.path[:len(settings.SIGMANET_CLIENT_AUTHENTICATE_PATH)] == settings.SIGMANET_CLIENT_AUTHENTICATE_PATH:
            state = request.GET.get('state', None)
            if state is None or state not in request.session.get('_oauth_state_token', []):
                raise RejectRequest('Your request was rejected due to invalid STATE token.')

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response


def get_oauth_state_token(request):
    state_tokens = request.session['_oauth_state_token']
    return state_tokens[len(state_tokens) - 1]
