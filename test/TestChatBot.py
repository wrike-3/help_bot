import os
import unittest

from config import ROOT_DIR
from ml_models.elastic_search_baseline import add_doc_to_index, msg_to_doc
from support_model import ModelNames, get_answer


class TestChatBot(unittest.TestCase):
    def test_parse_msg(self):
        input_msg = '''Some information text. First sentence about thing1. Second sentence about thing2.
What about sentence1? thing1_title. thing1. https://wrike.com/help.
What about sentence2? thing2_title. thing2. https://wrike.com/help.
'''
        doc_list = msg_to_doc(input_msg)
        true_ans = [{'doc_id': None, 'doc_title': 'thing1_title.',
                     'text': 'Some information text. First sentence about thing1. Second sentence about thing2.',
                     'keywords': 'thing1.', 'link': 'https://wrike.com/help.', 'section0': None,
                     'section1': 'thing1_title.'}, {'doc_id': None, 'doc_title': 'thing2_title.',
                                                    'text': 'Some information text. First sentence about thing1. Second sentence about thing2.',
                                                    'keywords': 'thing2.', 'link': 'https://wrike.com/help.',
                                                    'section0': None, 'section1': 'thing2_title.'}]
        self.assertEqual(true_ans, doc_list)

    def test_add_doc_to_index(self):
        docs = [{'doc_id': None, 'doc_title': 'thing1_title.',
                 'text': 'Some information text. First sentence about thing1. Second sentence about thing2.',
                 'keywords': 'thing1.', 'link': 'https://wrike.com/help.',
                 'section0': None, 'section1': 'thing1_title.'}, {'doc_id': None, 'doc_title': 'thing2_title.',
                                                                  'text': 'Some information text. First sentence about thing1. Second sentence about thing2.',
                                                                  'keywords': 'thing2.',
                                                                  'link': 'https://wrike.com/help.', 'section0': None,
                                                                  'section1': 'thing2_title.'}]
        for d in docs:
            add_doc_to_index(d)

    def test_baselines(self):
        questions = ['gantt chart', 'export report', 'support MS', 'share data', 'Machine Learning',
                     'how to create a task',
                     'how to reorder a subtask',
                     'where is user settings',
                     'how to export to Excel',
                     'how to reset a user password',
                     'how to reset a password',
                     'how to move task to another column']

        os.chdir(ROOT_DIR)
        for model_name in ModelNames:
            print(model_name.value)
            for q in questions:
                print('\t', q)
                ans = get_answer(q, model_name=model_name)
                print('\t\t', ans)
