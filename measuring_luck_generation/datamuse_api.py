from datamuse import *
import numpy as np
import pandas as pd

api = datamuse.Datamuse()
api.set_max_default(100)

def set_to_df(datamuse_response):
    """Converts the json response of the datamuse API into a DataFrame
    :datamuse_response
        [{'word': 'foo', 'score': 100}, {'word': 'bar', 'score': 120}]
    """
    reformatted = {
        'word': [response['word'] for response in datamuse_response],
        'score': [response['score'] for response in datamuse_response]
    }

    return pd.DataFrame.from_dict(reformatted)

def generate_set(context, strength='strong_set'):
    means_like = api.words(ml=context)
    adjectives_used_to_describe = api.words(rel_jjb='job')
    words_that_are_triggered_by = api.words(rel_trg='job')
    keywords = means_like + adjectives_used_to_describe + words_that_are_triggered_by
    sorted_keywords = sorted(keywords, key = lambda i: i['word'])
    print("DM : Set has been successfully generated!")
    return sorted_keywords

def generate_weak_set(context):
    return 0


def generate_strong_set(context):
    return 0