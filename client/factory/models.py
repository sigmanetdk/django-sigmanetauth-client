from dataclasses import dataclass
from datetime import datetime


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
    date_joined: datetime


@dataclass
class Token:
    type: str
    expire_in: int
    access_token: str
    refresh_token: str
