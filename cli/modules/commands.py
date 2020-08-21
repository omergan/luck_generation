from cli.modules.initializer import Initializer
from graph_utils import filter_topology, map_size, map_colors, map_labels, filter_excel, count_parameters, extract_qualification
from scripts.twint_scripts import scrap
from utils import Logger
import requests
import json

logger = Logger()
class Commands:
    def __init__(self, initializer: Initializer):
        self.initializer = initializer
        pass

    def run_generating_luck_simulation(self, online: bool):
        options = self.initializer.options
        tsm = self.initializer.TSM
        self.initializer.LG.generating_luck(options.username, options.context, options.network, tsm)

    def run_build_sub_graph_by_topology(self, topology):
        tsm = self.initializer.TSM
        if self.initializer.EXCEL is None:
            raise Exception('Excel not found')

        filtered = filter_topology(self.initializer.EXCEL, self.initializer.TSM.network.graph,
                                   self.initializer.LG.user, int(topology),
                                   self.initializer.TSM.network.user_dict)
        tsm.network.create_subgraph(filtered)
        tsm.network.draw()

    def run_build_full_graph(self, directed: bool):
        self.initializer.TSM.network.draw()

    def generate_costumer_word_cloud(self):
        costumer_words_as_str: str = self.initializer.EXCEL[0]['customer relevance set']
        costumer_relevance_set = json.loads(costumer_words_as_str.replace("'", '"'))
        words: str = ''

        for key in costumer_relevance_set:
            for i in range(costumer_relevance_set[key]):
                words += key + " "

        resp = requests.post('https://quickchart.io/wordcloud', json={
            'format': 'png',
            'width': 500,
            'height': 500,
            'fontScale': 25,
            'scale': 'linear',
            'padding': 1,
            'removeStopwords': False,
            'minWordLength': 1,
            'text': words,
        })

        file_name = self.initializer.LG.user.username + '_costumer_cloud.png'
        with open('datasets/word_clouds/' + file_name, 'wb') as f:
            f.write(resp.content)

    def generate_followers_word_cloud(self):
        followers_words = {}
        words: str = ''
        for row in self.initializer.EXCEL:
            follower_words_as_str: str = row['follower set']
            follower_relevance_set = json.loads(follower_words_as_str.replace("'", '"'))
            for key in follower_relevance_set:
                if key in followers_words:
                    followers_words[key] += follower_relevance_set[key]
                else:
                    followers_words[key] = follower_relevance_set[key]
        for key in followers_words:
            for i in range(followers_words[key]):
                words += key + " "

        json_file_name = self.initializer.LG.user.username + '_followers_cloud_words.json'
        with open('datasets/word_clouds/' + json_file_name, 'w') as outfile:
            json.dump(followers_words, outfile)

        resp = requests.post('https://quickchart.io/wordcloud', json={
            'format': 'png',
            'width': 500000,
            'height': 500000,
            'fontScale': 1,
            'scale': 'linear',
            'text': words,
        })

        file_name = self.initializer.LG.user.username + '_followers_cloud.png'

        with open('datasets/word_clouds/' + file_name, 'wb') as f:
            f.write(resp.content)
