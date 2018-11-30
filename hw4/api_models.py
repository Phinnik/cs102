from typing import List, Optional
from pydantic import BaseModel


class BaseUser(BaseModel):
    """ Модель пользователя с базовыми полями """
    id: int
    first_name: str
    last_name: str
    online: int
    deactivated: Optional[str]


class User(BaseUser):
    """ Модель пользователя с необязательным полем дата рождения """
    bdate: Optional[str]
    is_closed: Optional[bool]


class Message(BaseModel):
    """ Модель сообщения """
    unix_time: int
    from_id: int
    text: Optional[str]
