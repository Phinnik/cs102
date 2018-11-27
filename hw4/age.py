from datetime import datetime
from statistics import median
from typing import Optional, List
from api_models import User
from api import get_friends


def age_predict(user_id: int) -> Optional[int]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    friends = get_friends(user_id, fields='bdate,', count=1000)
    friends = select_friends(friends)
    today_datetime = datetime.today()
    days = 0
    for fr in friends:
        bday_datetime = datetime.strptime(fr.bdate, '%d.%m.%Y')
        days += (today_datetime - bday_datetime).days
    return days // len(friends) // 365.25


def select_friends(friends: List[User]) -> List[User]:
    """ Выборка друзей с полной датой рождения """
    good_friends = []
    for fr in friends:
        if fr.bdate is not None:
            if len(fr.bdate) >= 8:
                good_friends.append(fr)
    return good_friends


def main():
    age = age_predict(434463725)
    print(age)


if __name__ == '__main__':
    main()