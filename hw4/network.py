from api import get_friends, get_friends_with_execute
from igraph import Graph, plot
import igraph
import numpy as np
import time
from api_models import User
from typing import List


def get_network(users_ids, as_edgelist=True):
    network = []
    for i, user in enumerate(users_ids):
        time.sleep(1/3)
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


def get_network_with_execute(users: List[User]) :
    users = [fr.id for fr in users]
    friends_list = get_friends_with_execute(users)
    friends_list = [[friend.id for friend in user] for user in friends_list]

    network = []
    for i, friends in enumerate(friends_list):
        user_connections = set(users) & set(friends)
        for part in user_connections:
            connection = (i, users.index(part))
            network.append(connection)
    return network


def plot_graph(user_id):
    user_friends = get_friends(user_id, count = 1000)
    edges = get_network_with_execute(user_friends)
    vertices = [fr.last_name for fr in user_friends]

    # Создание графа
    g = Graph(vertex_attrs={"label":vertices},
        edges=edges, directed=False)
    g.es["width"] = 1
    g.simplify(multiple=True, loops=True, combine_edges={ "width": "sum" })

    communities = g.community_edge_betweenness(directed=False)
    clusters = communities.as_clustering()

    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)

    # Задаем стиль отображения графа
    N = len(vertices)
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=1000,
        area=N**3,
        repulserad=N**3)

    # Отрисовываем граф
    plot(g, **visual_style)


def main():
    plot_graph(434463725)

main()