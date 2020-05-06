from measuring_luck_generation import generating_luck as LG
from measuring_tie_strength import measure_tie_strength as tsm
import twint_api
from measuring_luck_generation import datamuse_api
import database_api
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
from measuring_tie_strength.models import User, Tweet
from measuring_tie_strength.graph import Network
LIMIT = 1

from utils import Logger
logger = Logger()


import networkx as nx
def map_connections(graph):
    key_indexes = {}
    value_indexes = {}
    i = 0
    j = 0
    for key in graph:
        if key not in key_indexes:
            key_indexes[key] = i
            i += 1
        for value in graph[key]:
            if value not in value_indexes:
                value_indexes[value] = j
                j += 1

    map = np.zeros((len(key_indexes), len(value_indexes)))
    for key in graph:
        for value in graph[key]:
            map[key_indexes[key]][value_indexes[value]] = 1

    plt.subplot(111), plt.imshow(map, cmap='gray'), plt.title("Tightness")
    plt.xticks([]), plt.yticks([])
    plt.show()

def count_followers(graph):
    for key in graph:
        print(f'{key} : {len(graph[key])}')

def networkx_things():
    # with open('datasets/edge_list.txt') as f:
    #     for row in f:
    #         print(row)
    g = nx.read_edgelist('datasets/edge_list.txt', create_using=nx.Graph(), nodetype=str)
    nx.draw(g)
    plt.show()
    # f = open("datasets/edge_list.txt", "w")
    # i=1
    # for key in graph:
    #     for value in graph[key]:
    #         f.write('{} {}\n'.format(key, value))
    #         print(f'{i} {key} {value}')
    #         i += 1
    # f.close()
    # pprint(graph)


if __name__ == '__main__':
    user = User("Charliedysonrec")
    network = Network()
    graph = network._graph
    # count_followers(graph)
    # map_connections(graph)
    # networkx_things()
    nx.draw(graph)
    plt.show()  # display
    # logger.debug("Starting main program!\n")
    # luck_generator = LG.LuckGenerator(is_online=False, limit=LIMIT)
    # # luck_generator.generating_luck("Charliedysonrec", "Looking for a software engineering job")
    # luck_generator.scrap("DevProtege")
    # # luck_generator.draw_mosaic(None)
    # logger.debug("\nEnding main program!")
