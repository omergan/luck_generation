import datamuse
import numpy as np

api = datamuse.Datamuse()
api.set_max_default(1000)

def generate_set(context, strength):
    means_like = api.words(ml=context)
    adjectives_used_to_describe = api.words(rel_jjb='job')
    words_that_are_triggered_by = api.words(rel_trg='job')
    keywords = means_like + adjectives_used_to_describe + words_that_are_triggered_by
    return sorted(keywords, key = lambda i: i['score'])

def generate_weak_set(context):
    return 0


def generate_strong_set(context):
    return 0