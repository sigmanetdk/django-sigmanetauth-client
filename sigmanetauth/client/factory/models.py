from dataclasses import dataclass


@dataclass
class UserInfo:
    first_name: str
    last_name: str
    email: str
    username: str
    phone_number: str
    id: str
    is_staff: bool
    is_active: bool
    is_superuser: bool
    date_joined: str

    @staticmethod
    def from_response(response):
        return UserInfo(
            first_name=response['first_name'],
            last_name=response['last_name'],
            email=response['email'],
            username=response['username'],
            phone_number=response['phone_number'],
            id=response['id'],
            is_staff=response['is_staff'],
            is_active=response['is_active'],
            is_superuser=response['is_superuser'],
            date_joined=response['date_joined']
        )


@dataclass
class Token:
    type: str
    expire_in: int
    access_token: str
    refresh_token: str

    @staticmethod
    def from_response(response):
        return Token(
            type=response['type'],
            expire_in=response['expire_in'],
            access_token=response['access_token'],
            refresh_token=response['refresh_token']
        )
