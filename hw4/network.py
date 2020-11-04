from api import get_friends, get_friends_with_execute
from igraph import Graph, plot
import igraph
import numpy as np
import time
from api_models import User
from typing import List


def get_network(users_ids, as_edgelist=True):
    # Gets network
    edgelist = []
    matrix = [[0]*len(users_ids) for i in range(len(users_ids))]
    for i, user in enumerate(users_ids):
        time.sleep(1/3)
        # Using try to exclude blocked users
        try:
            user_friends = set(get_friends(user, count=0)['items'])
            user_connections = set(users_ids) & user_friends
            for part in user_connections:
                connection = (users_ids.index(user), users_ids.index(part))
                edgelist.append(connection)
                matrix[users_ids.index(part)][i] = 0
        except Exception as e:
            pass
    if as_edgelist:
        return edgelist
    else:
        return matrix


def get_network_with_execute(users: List[User]):
    # Gets network using get_friends_with_execute
    users = [u.id for u in users]
    friends_list = get_friends_with_execute(users)
    friends_list = [[friend.id for friend in user] for user in friends_list]

    network = []
    for friend_ind, friends in enumerate(friends_list):
        user_connections = set(users) & set(friends)
        for part in user_connections:
            connection = (friend_ind, users.index(part))
            network.append(connection)
    return network


def plot_graph(user_id):
    # plots network graph
    user_friends = get_friends(user_id, count=0)
    # Deleting deactivated and closed users
    user_friends = [f for f in user_friends if (f.deactivated is None and not f.is_closed)]
    edges = get_network_with_execute(user_friends)
    vertices = [fr.last_name for fr in user_friends]

    g = Graph(vertex_attrs={"label": vertices},
              edges=edges, directed=False)
    g.es["width"] = 1
    g.simplify(multiple=True, loops=True)

    print(g)

    # sometimes can't make comunity coloring because too many comunyties?

    # communities = g.community_edge_betweenness(directed=False)
    # clusters = communities.as_clustering()
    # pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    # g.vs['color'] = pal.get_many(clusters.membership)

    # Making a style of graph
    N = len(vertices)

    visual_style = {
        "vertex_size": 20,
        "bbox": (2000, 2000),
        "margin": 100,
        "vertex_label_dist": 1.6,
        "edge_color": "gray",
        "autocurve": True,
        "layout": g.layout_fruchterman_reingold(
            maxiter=100000,
            area=N ** 2,
            repulserad=N ** 2)
    }

    # Plotting a graph
    plot(g, **visual_style)


def main():
    434463725
    plot_graph(434463725)


if __name__ == '__main__':
    main()
