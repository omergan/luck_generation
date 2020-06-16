from cli.main import cli
import numpy as np
import matplotlib.pyplot as plt
LIMIT = 1
from utils import Logger
logger = Logger()

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


if __name__ == '__main__':
    cli()
