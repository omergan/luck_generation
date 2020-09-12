import math
import random

from cli.modules.initializer import Initializer
from graph_utils import filter_topology, map_size, map_colors, map_labels, filter_excel, count_parameters, extract_qualification
from scripts.twint_scripts import scrap
from utils import Logger
import requests
import json

logger = Logger()


def add_word_to_set(dest_set, source_set, word):
    if word in dest_set:
        dest_set[word] += source_set[word]
    else:
        dest_set[word] = source_set[word]


class Commands:
    def __init__(self, initializer: Initializer):
        self.initializer = initializer
        pass

    def run_online_data_mining(self, online: bool):
        scrap(self.initializer.LG, self.initializer.options.username, 0)

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
        self.initializer.EXCEL = filter_excel(self.initializer.EXCEL, self.initializer.TSM.network.graph,
                                   self.initializer.TSM.network.user_dict)
        size_map = map_size(self.initializer.EXCEL, self.initializer.TSM.network.graph, self.initializer.LG.user,
                            self.initializer.TSM.network.user_dict, type=self.initializer.TSM.network.mapping_type,
                                threshold=self.initializer.TSM.network.threshold)
        colors_map = map_colors(self.initializer.EXCEL, self.initializer.TSM.network.graph, self.initializer.LG.user,
                                self.initializer.TSM.network.user_dict, type=self.initializer.TSM.network.mapping_type,
                                threshold=self.initializer.TSM.network.threshold)
        labels_map = map_labels(self.initializer.EXCEL, self.initializer.TSM.network.graph, self.initializer.LG.user,
                                self.initializer.TSM.network.user_dict, type=self.initializer.TSM.network.mapping_type,
                                threshold=self.initializer.TSM.network.threshold)
        tsm.network.draw(color_map=colors_map, size_map=size_map, label_map=labels_map)

    def run_build_full_graph(self, directed: bool):
        size_map = map_size(self.initializer.EXCEL, self.initializer.TSM.network.graph, self.initializer.LG.user,
                            self.initializer.TSM.network.user_dict, type=self.initializer.TSM.network.mapping_type,
                                threshold=self.initializer.TSM.network.threshold)
        colors_map = map_colors(self.initializer.EXCEL, self.initializer.TSM.network.graph, self.initializer.LG.user,
                                self.initializer.TSM.network.user_dict, type=self.initializer.TSM.network.mapping_type,
                                threshold=self.initializer.TSM.network.threshold)
        labels_map = map_labels(self.initializer.EXCEL, self.initializer.TSM.network.graph, self.initializer.LG.user,
                                self.initializer.TSM.network.user_dict, type=self.initializer.TSM.network.mapping_type,
                                threshold=self.initializer.TSM.network.threshold)
        self.initializer.TSM.network.draw(color_map=colors_map, size_map=size_map, label_map=labels_map)

    def run_count_parameters(self, threshold):
        count_parameters(self.initializer.EXCEL, self.initializer.LG.user, threshold)
        logger.debug("\nAll count files have been created\n")

    def run_extract_qualification_data(self):
        total = len(self.initializer.LG.strict_set)
        extract_qualification(self.initializer.EXCEL, self.initializer.LG.user, total)
        logger.debug("\nQualification data has been extracted to file\n")

    def run_map_color_by_luck(self, threshold):
        self.initializer.TSM.network.mapping_type = "luck"
        self.initializer.TSM.network.threshold = threshold
        logger.debug("\nMapping type has been changed to luck with threshold {}\n".format(str(threshold)))

    def run_map_color_by_relevance_and_surprise(self, threshold):
        self.initializer.TSM.network.mapping_type = "relevance_and_surprise"
        self.initializer.TSM.network.threshold = threshold
        logger.debug("\nMapping type has been changed to relevance and surprise with threshold {}\n".format(str(threshold)))

    def run_map_color_by_relevance(self, threshold):
        self.initializer.TSM.network.mapping_type = "relevance"
        self.initializer.TSM.network.threshold = threshold
        logger.debug(
            "\nMapping type has been changed to relevance with threshold {}\n".format(str(threshold)))

    def run_map_color_by_surprise(self, threshold):
        self.initializer.TSM.network.mapping_type = "surprise"
        self.initializer.TSM.network.threshold = threshold
        logger.debug("\nMapping type has been changed to surprise with threshold {}\n".format(str(threshold)))

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
            'rotation': 1,
            # 'colors': ["red", "#00ff00", "rgba(0, 0, 255, 1.0)"],
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
            'width': 5000,
            'height': 5000,
            'fontScale': 1,
            'scale': 'linear',
            'text': words,
        })

        file_name = self.initializer.LG.user.username + '_followers_cloud.png'

        with open('datasets/word_clouds/' + file_name, 'wb') as f:
            f.write(resp.content)

    def generate_followers_surprise_word_cloud(self, randomized: bool):
        surprise_words = {}
        costumer_words_as_str: str = self.initializer.EXCEL[0]['customer relevance set']
        costumer_relevance_set = json.loads(costumer_words_as_str.replace("'", '"'))
        words: str = ''
        excel = self.initializer.EXCEL

        if randomized:
            excel = random.sample(excel, math.floor(0.1 * len(excel)))

        for row in excel:
            follower_words_as_str: str = row['follower set']
            follower_relevance_set = json.loads(follower_words_as_str.replace("'", '"'))
            for key in follower_relevance_set:
                if key in follower_relevance_set and key not in costumer_relevance_set:
                    add_word_to_set(surprise_words, follower_relevance_set, key)
                elif key in costumer_relevance_set and key not in follower_relevance_set:
                    add_word_to_set(surprise_words, costumer_relevance_set, key)

        for key in surprise_words:
            for i in range(surprise_words[key]):
                words += key + " "

        prefix = 'randomized/' if randomized else ''
        file_name = prefix + self.initializer.LG.user.username + '_followers_surprise_word_clouds.png'
        json_file_name = prefix + self.initializer.LG.user.username + '_followers_surprise_word_clouds.json'
        with open('datasets/word_clouds/followers_surprise_words_clouds/' + json_file_name, 'w') as outfile:
            json.dump(surprise_words, outfile)

        resp = requests.post('https://quickchart.io/wordcloud', json={
            "format": "png",
            "width": 1000,
            "height": 1000,
            "fontFamily": "sans-serif",
            "fontScale": 15,
            "rotation": 1,
            "scale": "linear",
            'text': words,
        })

        with open('datasets/word_clouds/followers_surprise_words_clouds/' + file_name, 'wb') as f:
            f.write(resp.content)