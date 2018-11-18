import requests
#from datetime import datetime
import time
#import plotly
#import plotly.plotly as py
#import plotly.graph_objs as go
import config
import igraph
from igraph import Graph, plot
import numpy as np

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


def get_network(users_ids, as_edgelist=True):
    network = []
    for user in users_ids:
        time.sleep(3/2.5)
        # use try to exclude blocked users
        try:
            user_friends = set(get_friends(user, count=0)['items'])
            user_connections = set(users_ids) & user_friends
            for part in user_connections:
                connection = (users_ids.index(user), users_ids.index(part))
                network.append(connection)            
        except Exception as e:
            pass
    return network


"""my_friends = get_friends(config.VK['MY_ID'], count=0)['items']
ntw = get_network(my_friends)

f = open('ntw.py', 'w')
f.write('ntw = {}   '.format(ntw))
f.close()"""



from ntw import ntw

def plot_graph(network):
    # Создание вершин и ребер
    edges = network
    vertices = [i for i in range(len(edges))]

    # Создание графа
    g = Graph(vertex_attrs={"label":vertices},
        edges=edges, directed=False)

    # Задаем стиль отображения графа
    N = len(vertices)
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=1000,
        area=N**3,
        repulserad=N**3)

    g.simplify(multiple=True, loops=True)
    """
    communities = g.community_edge_betweenness(directed=False)
    clusters = communities.as_clustering()
    print(clusters)

    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    """
    # Отрисовываем граф
    plot(g, **visual_style)

plot_graph(ntw)