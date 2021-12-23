# SigmaNet Auth client

## Installation

### pip
Run `pip install git+https://github.com/tdybda17/django-sigmanetauth-client.git`
The package can also be freezed.

### download
Clone master and run `python setup.py sdist` from inside the `django_sigmanetauth_client` folder
This will make a new folder `dist` with the zipped `tar.gz` file.

## Setup

### (REQUIRED) settings variables
Add the following variables to your `settings.py` file:
``` python
SIGMANET_AUTH_CLIENT_SECRET = '' # Obtain from the auth server
SIGMANET_AUTH_CLIENT_ID = '' # Obtain from the auth server
SIGMANET_CLIENT_LOGIN_PATH = '' # The client path to where the user should log in from. Ex. /login/
SIGMANET_CLIENT_AUTHENTICATE_PATH = '' # The client path to where the auth server should redirect the authenticated user back to the client.
SIGMANET_AUTH_BASE_URL = '' # The base url for the auth server. Ex. http://127.0.0.1:8001 or https://auth.examplesite.com
```

### (RECOMMENDED) state middware usage
The state middware ensures cross-site request forgery. If the require_csrf boolean is checked for the client, make sure to add this middleware. This is highly recommended.

Add the `SigmaNetOAuthValidateStateMiddleware` 

``` python
MIDDLEWARE = [
    ...
    'django.middleware.csrf.CsrfViewMiddleware',
    'sigmanetauth.client.middleware.oauth.SigmaNetOAuthValidateStateMiddleware',  # <---
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    ...
]
```


## Usage

### Obtain login uri
You can obtain the login url for the login page by:

``` python
from sigmanetauth.client.client import SigmaNetOAuthClient
client = SigmaNetOAuthClient(require_csrf=True)
login_url = client.get_authorize_url(request)
```

This url should be placed somewhere on the login template.

### Authenticate authorized users
When the auth server has successfully authenticated the user, the server redirects the user back to the client. You can validate the user by:

``` python
client = SigmaNetOAuthClient()
response, token = client.get_token(request)
if response.status_code >= 300:
    # error: The user was not authenticated
    pass
```

You can get the users info by:

``` python
response, user_info = client.get_userinfo(token.access_token)
if response.status_code >= 300:
    # error: The user was not authenticated
```


## Reference

### client.get_authorize_url()
return type: `str`

### client.get_token(request)
arg0: `WSGIRequest`

return type:
1. if successfully obtained returns `(response, Token)` (See [Token](https://github.com/tdybda17/django-sigmanetauth-client/blob/master/sigmanetauth/client/factory/models.py))
2. if `response.status_code` >= 300 returns `(response, None)`

### client.get_userinfo(access_token)
arg0: access token `str`

return type:
1. if successfully obtained returns `(response, UserInfo)` (See [UserInfo](https://github.com/tdybda17/django-sigmanetauth-client/blob/master/sigmanetauth/client/factory/models.py))
2. if `response.status_code` >= 300 returns `(response, None)`
