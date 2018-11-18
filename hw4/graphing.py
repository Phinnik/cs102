import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import igraph
from igraph import Graph, plot
import numpy as np


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