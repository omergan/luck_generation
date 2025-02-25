import pprint
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx
import matplotlib.image as mpimg
import networkx as nx
import database_api as db
import pandas as pd
from measuring_tie_strength.models import User

class Network(object):
    """ Graph data structure, undirected by default. """
    def __init__(self, directed=False):
        self.user_dict = {}
        self.graph = nx.DiGraph() if directed else nx.Graph()
        self.graph.add_edges_from(self.load_connections())
        self.mapping_type = "luck"
        self.threshold = 100

    def load_connections(self):
        connections = db.get_all_connections()
        user_connections = {}
        user_labels = []
        for x, y in connections:
            user_connections[x] = User(x, True)
            user_connections[y] = User(y, True)
            user_labels.append([user_connections[x].username, user_connections[y].username])
        self.user_dict = user_connections
        # return user_labels
        return connections

    def draw(self, color_map, size_map, label_map):
        # pyDot = nx.nx_pydot.to_pydot(self.graph)
        # png_str = pyDot.create_png('example1_graph.png')
        nx.draw(self.graph, node_color=color_map, with_labels=True, font_size=6, node_size=size_map, labels=label_map)
        plt.show()

    # def draw(self):
    #     nx.draw(self.graph, with_labels=True, font_size=6)
    #     plt.show()

    def create_subgraph(self, nodes):
        self.graph = self.graph.subgraph(nodes)

    def get_neighbours(self, n):
        return [x for x in self.graph.neighbors(n)]

    def get_common_neighbours(self, u, v):
        return [self.user_dict[x] for x in nx.common_neighbors(self.graph, u, v)]

    def get_shortest_path(self, u, v):
        return [self.user_dict[x] for x in list(nx.shortest_path(self.graph, u, v))]

    def count_common_neighbours(self):
        neighbours = []
        common_count = {}
        for x in nx.nodes(self.graph):
            for y in nx.nodes(self.graph):
                if x != y:
                    common = [x for x in nx.common_neighbors(self.graph,x,y)]
                    if len(common) >= 0:
                        if len(common) in common_count:
                            common_count[len(common)] = common_count[len(common)] + 1
                        else:
                            common_count[len(common)] = 1
                        if len(common) >= 4:
                            print(x, y, len(common))

                        neighbours.append({
                            'candidate': x,
                            'target': y,
                            'count': len(common)
                        })
        print(common_count)

    def count_shortest_path(self):
        shortest_count = {}
        i = 0
        for x in nx.nodes(self.graph):
            for y in nx.nodes(self.graph):
                if i == 389772:
                    continue
                if x != y:
                    try:
                        shortest = [x for x in nx.shortest_path(self.graph, x, y)]
                    except networkx.exception.NetworkXNoPath:
                        shortest = [] # TODO : add length of 1 if has edge
                    if len(shortest) >= 0:
                        if len(shortest) in shortest_count:
                            shortest_count[len(shortest)] = shortest_count[len(shortest)] + 1
                        else:
                            shortest_count[len(shortest)] = 1
                        if len(shortest) >= 12:
                            print(i, len(shortest), shortest)
                i += 1
        print(shortest_count)

    def draw_table(self, data):
        df = pd.DataFrame.from_dict(data)
        df.to_excel("count_common_neighbours.xlsx", index=None, header=True)