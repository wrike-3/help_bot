# -*- coding: utf-8 -*-
import urllib.parse
from gensim.summarization import keywords
from gensim.parsing.preprocessing import remove_stopwords
import enum
from ml_models import elastic_search_baseline, bert_emb_baseline, tfidf_baseline, bpe_baseline


class ModelNames(enum.Enum):
    REDIRECT = 'redirect'
    ELASTIC = 'elastic'
    BERT = 'bert'
    BPE = 'bpe'
    TFIDF = 'tfidf'


# default model
MODEL_NAME = ModelNames.ELASTIC

model_name_dict = {x.value: x for x in ModelNames}


def get_keywords(query):
    return keywords(query)


def remove_stop_words_func(query):
    return remove_stopwords(query)


def get_answer_redirect(query):
    query_encode = urllib.parse.quote(query)
    return f"Let's go to https://help.wrike.com/hc/en-us/search?query={query_encode}"


def get_answer(query, use_lower=True, use_keywords=False, use_remove_stopwords=False, model_name=MODEL_NAME):
    if use_lower:
        query = query.lower()
    if use_keywords:
        query = get_keywords(query)
    if use_remove_stopwords:
        query = remove_stop_words_func(query)
    try:
        if model_name == ModelNames.REDIRECT:
            return get_answer_redirect(query)
        if model_name == ModelNames.ELASTIC:
            return elastic_search_baseline.get_answer(query)
        if model_name == ModelNames.BERT:
            return bert_emb_baseline.get_answer(query)
        if model_name == ModelNames.BPE:
            return bpe_baseline.get_answer(query)

        if model_name == ModelNames.TFIDF:
            return tfidf_baseline.get_answer(query)
    except Exception as ex:
        print(ex)
        return "not found :(\nPlease paraphrase your query"


def main():
    query = 'How plot gantt Chart?'
    answer = get_answer(query)
    print(answer)


if __name__ == '__main__':
    main()
