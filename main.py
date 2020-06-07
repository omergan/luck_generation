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
    users.append(User("Charliedysonrec")) # 800589492
    tsmtool = tsm.TieStrengthTool(is_online=False, limit=20, username="Charliedysonrec")
    # users.append(User("uriadoni"))  # 167900828
    # users.append(User("cakiralp1"))  # 800589492
    # users.append(User("PennanenMaria"))  # 1587925376
    # users.append(User("accelerator_ffm"))  # 4186469475
    # users.append(User("LukeMorton"))  # 1587925376
    # users.append(User("scimon"))  # 4186469475

    # 2993950570:  # michael's id

    logger.debug("Starting main program!\n")
    # luck_generator = LG.LuckGenerator(is_online=False, limit=LIMIT)
    # username = "Charliedysonrec"
    # luck_generator.generating_luck(username, "Looking for a software engineering job")
    # luck = luck_generator.luck

    df = pd.read_excel('full - Charliedysonrec.xlsx')
    luck = list(df.T.to_dict().values())

    orig_list = tsmtool.network.graph
    nodelist = list(orig_list)[:30]
    import pdb; pdb.set_trace()
    shape_map = map_shapes(luck, orig_list)
    color_map = map_colors(luck, orig_list, 800589492)
    tsmtool.network.draw(list(orig_list), color_map, shape_map)


    # luck_generator.generating_luck("Charliedysonrec", "Looking for a software engineering job")
    # luck_generator.scrap("DevProtege")
    logger.debug("\nEnding main program!")
