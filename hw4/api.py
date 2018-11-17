import requests
from datetime import datetime
import time
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import config


#plotly.tools.set_credentials_file(username=config.PLOTLY['USERNAME'], api_key=config.PLOTLY['API_KEY'])


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    request_status = False
    retries = 1
    while (request_status == False) and (retries < max_retries):
        try:
            r = requests.get(url, params)
            request_status = True
        except requests.RequestException as e:
            time.sleep(timeout * backoff_factor * retries)
            retries += 1
    #print(r.json())
    return r.json()['response']


def is_api_ok():
    url = "https://api.vk.com/method/friends.get"
    parameters = {'access_token': config.VK['VK_ACCESS_TOKEN'],
                  'user_id': config.VK['MY_ID'],
                  'fields': '',
                  'count': 1,
                  'v': config.VK['API_VERSION']}
    r = requests.get(url, params=parameters)
    return r.json()


def get_friends(user_id, fields='', count=5):
    """ Вернуть данных о друзьях пользователя
    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    url = "https://api.vk.com/method/friends.get"
    parameters = {'access_token': config.VK['VK_ACCESS_TOKEN'],
                  'user_id': user_id,
                  'fields': fields,
                  'count': count,
                  'v': config.VK['API_VERSION']}

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

def remove_blocked_users(ids):
    not_blocked = []
    time_start = time.time()
    for user in ids:
        time.sleep(1/2.5)
        try:
            get_friends(user, count=1)
            not_blocked.append(user)
        except Exception as e:
            print('vk.com/id{} is blocked'.format(user))
    return not_blocked


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
    return days // len(friends) // 365.25


def messages_get_history(user_id, offset=0, count=200):
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
    
    url = "https://api.vk.com/method/messages.getHistory"
    parameters = {
        'access_token': config.VK['VK_ACCESS_TOKEN'],
        'user_id': user_id,
        'offset': offset,
        'count': count,
        'v': config.VK['API_VERSION']
    }
    messages_history = get(url, params=parameters)
    return messages_history


def get_many_messages(user_id, count, offset=0):
    """ возвращает список сообщений учитывая ограничения api"""
    
    messages = []
    start_time = time.time()
    for i in range(0, count, 200):
        if i % 3 == 0:
            time.sleep(time.time() - start_time)
            start_time = time.time()
        new_messages = messages_get_history(user_id, offset=offset + i, count=200)
        messages.extend(new_messages['items'])
    return messages


def count_dates_from_messages(messages):
    """ Получить список дат и их частот
    :param messages: список сообщений
    """
    freq_list = [[], []]
    for mes in messages:
        date = datetime.fromtimestamp(mes['date']).strftime("%Y-%m-%d")
        if date in freq_list[0]:
            ind = freq_list[0].index(date)
            freq_list[1][ind] += 1
        else:
            freq_list[0].append(date)
            freq_list[1].append(1)
    return freq_list




def plotly_messages_freq(freq_list):
    """ Построение графика с помощью Plot.ly
    :param freq_list: список дат и их частот
    """
    x = freq_list[0]
    y = freq_list[1]
    data = [go.Scatter(x=x, y=y)]
    py.plot(data)


my_friends = [948354, 1249681, 1419151, 2109593, 2768170, 3860625, 4047774, 5640827, 6187198, 8154147, 8745814, 9696180, 11833217, 12838642, 17593518, 18101915, 22565342, 24413126, 26174862, 32224206, 34902980, 36023372, 36465853, 42470127, 42712016, 44971144, 47369902, 50217430, 52280514, 52972873, 53414474, 54597195, 56200185, 56568321, 57902269, 59914914, 60155688, 61085756, 68948561, 70112576, 76524880, 77578732, 77788430, 80167291, 82455870, 82863319, 82935666, 83798048, 85370197, 87036399, 88589789, 90732169, 90735275, 91969986, 93023115, 93132622, 95706836, 95973175, 96952120, 99042615, 99515538, 100028094, 101530171, 105164952, 105664624, 105817079, 109812549, 112498659, 113315887, 116913967, 120831486, 121928723, 122489381, 126037618, 126405040, 134137768, 135551107, 135709136, 139899145, 141975875, 144772087, 145234784, 148286001, 149607371, 150673899, 151361871, 151379262, 153731919, 154021074, 155217236, 155599766, 157650866, 158148787, 162045852, 163781571, 164400909, 166006989, 168331752, 168339721, 168544749, 172030641, 172158253, 175968087, 177641185, 177789360, 177993324, 178411788, 184871854, 185784713, 186489225, 192268011, 203977390, 207085522, 208389069, 209077977, 209669071, 214537296, 216843689, 217829982, 218211465, 218772230, 218902184, 221450385, 222840135, 223315190, 224102023, 234936985, 235371642, 239797036, 249735203, 250683129, 256727692, 259007980, 264610219, 267778500, 269001722, 272076217, 276174822, 283994868, 285253094, 289683117, 304745115, 307145087, 308757818, 311355929, 324313708, 337271335, 359959537, 368536810, 385982077, 413155906, 427798954, 429841185, 433575696, 438224812, 452699879, 455719120, 466424081, 478277366, 504911063, 505540783]



def get_network(users_ids, as_edgelist=True):
    network = []
    user_friends_list = []

    for user in users_ids:
        time.sleep(1/2.5)
        try:
            u_friends = set(get_friends(user, count=0))
            user_friends_list = append(u_friends)
        except Exception:
            pass

    all_people = set(users_ids)
    for i in range(len(user_friends_list)):
        all_people.update(user_friends_list[i])

    


network = get_network(my_friends)


'''

def plot_graph(graph):
    # PUT YOUR CODE HERE

'''
