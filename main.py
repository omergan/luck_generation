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
    users = []
    users.append(User("Charliedysonrec")) # 800589492
    # users.append(User("uriadoni"))  # 167900828
    # users.append(User("cakiralp1"))  # 800589492
    # users.append(User("PennanenMaria"))  # 1587925376
    # users.append(User("accelerator_ffm"))  # 4186469475
    # users.append(User("LukeMorton"))  # 1587925376
    # users.append(User("scimon"))  # 4186469475
    #
    tsmtool = tsm.TieStrengthTool(is_online=False, limit=20, username="MizrahiMichael")
    # tsmtool.create_network(directed=False)

    logger.debug("Starting main program!\n")
    luck_generator = LG.LuckGenerator(is_online=False, limit=LIMIT)
    username = "MizrahiMichael"
    luck_generator.generating_luck(username, "Looking for a software engineering job")

    luck = luck_generator.luck
    color_map = []
    for node in tsmtool.network.graph:
        luck_value=0
        for x in luck:
            if x['follower'].id == node:
                luck_value = x['luck']
        if node == 2993950570: #michael's id
            color_map.append('#00FF00')
        elif luck_value > 3.33:
            color_map.append('#FF5733')
        elif 3.33 >= luck_value > 2.5:
            color_map.append('#F6FF33')
        elif 2.5 >= luck_value > 2:
            color_map.append('#90FF33')
        else:
            color_map.append('#3390FF')
    tsmtool.network.draw(color_map)


    # luck_generator.generating_luck("Charliedysonrec", "Looking for a software engineering job")
    # luck_generator.scrap("DevProtege")
    logger.debug("\nEnding main program!")
