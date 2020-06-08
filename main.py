from measuring_luck_generation import generating_luck as LG
from measuring_tie_strength import measure_tie_strength as tsm
import twint_api
from measuring_luck_generation import datamuse_api
import database_api
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
from measuring_tie_strength.models import User, Tweet
from measuring_tie_strength import measure_tie_strength as tsm
import pandas as pd
LIMIT = 1

from utils import Logger
from graph_utils import *
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
    users = []
    users.append(User("Charliedysonrec"))  # 800589492
    users.append(User("MizrahiMichael"))  # 2993950570
    users.append(User("LukeMorton"))
    user = users[0]
    tsmtool = tsm.TieStrengthTool(is_online=False, limit=20, username=user.username)


    logger.debug("Starting main program!\n")
    df = pd.read_excel('new - Charliedysonrec.xlsx')
    luck = list(df.T.to_dict().values())
    user_dict = tsmtool.network.user_dict

    orig_list = tsmtool.network.graph
    len(orig_list)
    filter = filter_topology(luck, orig_list, user, 5, user_dict)
    # filter = filter_luck(luck, orig_list, user, 3.3, user_dict)
    tsmtool.network.create_subgraph(filter)
    color_map = map_colors(luck, filter, user.id, user_dict)
    size_map = map_size(luck, filter, user.id, user_dict)
    tsmtool.network.draw(list(filter), color_map, size_map)

    logger.debug("\nEnding main program!")



    # luck_generator = LG.LuckGenerator(is_online=False, limit=LIMIT)
    # username = "Charliedysonrec"
    # luck_generator.generating_luck(username, "Looking for a software engineering job")
    # luck = luck_generator.luck
    # luck_generator.generating_luck("Charliedysonrec", "Looking for a software engineering job")
    # luck_generator.scrap("DevProtege")
