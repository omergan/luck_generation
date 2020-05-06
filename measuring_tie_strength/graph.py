import pprint
from collections import defaultdict
import networkx as nx
import database_api as db

class Network(object):
    """ Graph data structure, undirected by default. """
    def __init__(self, directed=True):
        self._graph = nx.Graph()
        self._graph.add_edges_from(self.load_connections())

    def load_connections(self):
        connections = db.get_all_connections()
        return connections
