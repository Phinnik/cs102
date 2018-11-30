from datetime import datetime
from typing import Optional, List
from api_models import User
from api import get_friends


def select_friends(friends: List[User]) -> List[User]:
    # Choosing users with full bdate
    good_friends = []
    for fr in friends:
        if fr.bdate is not None:
            if len(fr.bdate) >= 8:
                good_friends.append(fr)
    return good_friends


def age_predict(user_id: int) -> Optional[int]:
    # Counts median in ages of user friends
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


def main():
    # Predicting age of Dementiy
    age = age_predict(817934)
    print(age)


if __name__ == '__main__':
    main()
