import requests
from datetime import datetime
import time
#import plotly


config = {
    'VK_ACCESS_TOKEN': 'da2c13c7d22618fa1e7dcad0351f51ca630c127ba77203eca08125318fa7447b71d66cc2ffd2458f9f24a8',
    'PLOTLY_USERNAME': 'Имя пользователя Plot.ly',
    'PLOTLY_API_KEY': 'Ключ доступа Plot.ly'
}


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    r = requests.get(url, params)
    retries = 1
    request_status = r.status_code
    while (request_status != 200) and (retries < max_retries):
        time.sleep(timeout * backoff_factor * retries)
        r = requests.get(url, params)
        retries += 1
    return r.json()['response']


def get_friends(user_id, fields='', count=5):
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    url = "https://api.vk.com/method/friends.get"
    parameters = {
        'access_token': config['VK_ACCESS_TOKEN'],
        'user_id': user_id,
        'fields': fields,
        'count': count,
        'v': 5.87
    }
    friends = get(url, params=parameters)
    return friends


def select_friends(friends):
    """ Выборка друзей с полной датой рождения"""
    good_friends = []
    for fr in friends:
        if 'bdate' in fr:
            if len(fr['bdate']) == 9:
                good_friends.append(fr)
    return good_friends


def age_predict(user_id):
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    friends = get_friends(user_id, fields='bdate,', count=1000)['items']
    friends = select_friends(friends)
    today_datetime = datetime.today()
    days = 0
    for fr in friends:
        bday_datetime = datetime.strptime(fr['bdate'], '%d.%m.%Y')
        days += (today_datetime - bday_datetime).days
    return days // len(friends) // 365

'''
def messages_get_history(user_id, offset=0, count=20):
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    # PUT YOUR CODE HERE


def count_dates_from_messages(messages):
    """ Получить список дат и их частот

    :param messages: список сообщений
    """
    # PUT YOUR CODE HERE


def plotly_messages_freq(freq_list):
    """ Построение графика с помощью Plot.ly

    :param freq_list: список дат и их частот
    """
    # PUT YOUR CODE HERE


def get_network(users_ids, as_edgelist=True):
    # PUT YOUR CODE HERE


def plot_graph(graph):
    # PUT YOUR CODE HERE

'''
