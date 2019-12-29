from datamuse import datamuse
import numpy as np
import enums

api = datamuse.Datamuse()
api.set_max_default(1000)

def generate_set(context, strength):
    keywords = []
    means_like = api.words(ml=context)
    adjectives_used_to_describe = api.words(rel_jjb='job')
    words_that_are_triggered_by = api.words(rel_trg='job')
    if strength == enums.Strength.weak:
        keywords = generate_weak_set(context)
    elif strength == enums.Strength.strong:
        keywords = generate_strong_set(context)
    keywords = means_like + adjectives_used_to_describe + words_that_are_triggered_by
    sorted(keywords.items(), key=lambda kv: (kv[1], kv[0]))
    return 0

def generate_weak_set(context):
    return 0


def generate_strong_set(context):
    return 0