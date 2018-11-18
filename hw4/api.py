# TODO: separate graphing stuff and vk analisys with different files
# TODO: write excecute function to get data from vk faster
# TODO: remake graphing function. Add more settings


import requests
import time
from datetime import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import igraph
from igraph import Graph, plot
import numpy as np
import config


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос c экспоненциальным нарастанием задержки при ошибке """
    request_status = False
    retries = 1
    while (request_status == False) and (retries < max_retries):
        try:
            r = requests.get(url, params)
            request_status = True
        except requests.RequestException as e:
            time.sleep(timeout * backoff_factor * retries)
            retries += 1
    return r.json()['response']


def is_api_ok():
    # функция для отладки. Проверка, доступно ли api
    url = "https://api.vk.com/method/friends.get"
    parameters = {'access_token': config.VK['VK_ACCESS_TOKEN'],
                  'user_id': config.VK['MY_ID'],
                  'fields': '',
                  'count': 1,
                  'v': config.VK['API_VERSION']}
    r = requests.get(url, params=parameters).json()
    print(r)
    return r


def get_friends(user_id, fields='', count=5):
    """ Вернуть данныe о друзьях пользователя """
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
    """ Выборка друзей с полной датой рождения """
    good_friends = []
    for fr in friends:
        if 'bdate' in fr:
            if len(fr['bdate']) == 9:
                good_friends.append(fr)
    return good_friends


def age_predict(user_id):
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя """
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
    """ Получить историю переписки с указанным пользователем """
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
    """ Получить список дат и их частот """
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
    """ Построение графика с помощью Plot.ly """
    x = freq_list[0]
    y = freq_list[1]
    data = [go.Scatter(x=x, y=y)]
    py.plot(data)


def get_network(users_ids, as_edgelist=True):

    network = []
    start_time = time.time()
    for i, user in enumerate(users_ids):
        # sleep for not to be banned
        if i % 3 == 0:
            time.sleep(time.time() - start_time)
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


def plot_graph(network):
    # Создание вершин
    vertices = [i for i in range(len(network))]

    # Создание графа
    g = Graph(vertex_attrs={"label":vertices},
        edges=network, directed=False)

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


def main():
    # login to your plotly account
    plotly.tools.set_credentials_file(username=config.PLOTLY['USERNAME'], api_key=config.PLOTLY['API_KEY'])

if __name__ == '__main__':
    main()