from datamuse import *
import numpy as np
import pandas as pd

api = datamuse.Datamuse()
api.set_max_default(1000)

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

def generate_weak_set(context):
    keywords = []
    for word in context.split(" "):
        triggered = api.words(rel_ant=word)
        set_of_words = [x['word'] for x in triggered]
        keywords.append(set_of_words)
    print("DM : Weak set has been successfully generated!")
    return keywords


def generate_strong_set(context):
    keywords = []
    for word in context.split(" "):
        triggered = api.words(rel_trg=word)
        set_of_words = [x['word'] for x in triggered]
        keywords.append(set_of_words)
    print("DM : Strong set has been successfully generated!")
    return keywords