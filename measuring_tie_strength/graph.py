import pprint
from collections import defaultdict
import database_api as db

class Network(object):
    """ Graph data structure, undirected by default. """
    def __init__(self, directed=True):
        self._graph = defaultdict(set)
        self._directed = directed
        connections = self.load_connections()
        self.add_connections(connections)

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """
        for node1, node2 in connections:
            self.add(node1, node2)

    def add(self, node1, node2):
        """ Add connection between node1 and node2 """
        self._graph[node1].add(node2)
        if not self._directed:
            self._graph[node2].add(node1)

    def remove(self, node):
        """ Remove all references to node """
        for n, cxns in self._graph.items():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    def load_connections(self):
        connections = db.get_all_connections()
        return connections
