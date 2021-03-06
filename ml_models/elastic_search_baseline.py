from time import sleep

from bs4 import BeautifulSoup
import glob
import re
import subprocess
from elasticsearch import Elasticsearch
import pandas as pd
from config import DATA

MAX_ANSWER_COUNT = 3
MAX_TEXT_LEN = 280
es = Elasticsearch()


def get_answer_first(query):
    res = es.search(index="some-index",
                    body={'query': {'match': {
                        'text':
                            {'query': query,
                             'operator': 'OR'}
                    }}})
    return print_res(res)


def get_answer(query):
    try:
        return get_answer_first(query)
    except:
        subprocess.call('systemctl restart elasticsearch', shell=True)
        sleep(10)
        return get_answer_first(query)


def extract_keywords(subsection1):
    keywords = []
    deprecated_words = {'Overview', 'Important Information'}
    for keyword in subsection1.find_all('a', {'class': 'link'}):
        keyword = keyword.text.strip()
        if keyword not in deprecated_words:
            keywords.append(keyword)
    return keywords


def process_input_files():
    idir = f'{DATA}/input'
    ofile_path = f'{DATA}/wrike_faq_index.csv'

    pages = filter(lambda x: not x.endswith('index-en.html'), sorted(glob.glob(idir + '/*')))
    deprecated_sections = {'Overview', 'Important Information'}

    lines = []
    for page_id, page_path in enumerate(pages):
        print(page_path)
        soup = BeautifulSoup(open(page_path), "html.parser")
        # for title in soup.find_all('div', {'class': 'title'}):
        #     print('\t', title.text.strip())
        page_title = soup.find('h2', {'class': 'title'}).text  # page title
        for doc_id, subsection1 in enumerate(soup.find_all('div', {'class': 'section internal internal'})):
            doc_text = re.sub('\n+', '\n', subsection1.text) \
                .strip()
            subsection1_title = subsection1.find(['h4', 'h5', 'h6']).text

            if subsection1_title in deprecated_sections or not doc_text:
                print('skip doc', doc_id, subsection1_title)
                continue

            keywords = extract_keywords(subsection1)
            line = dict(
                page_id=page_id,
                section0=page_title,
                doc_id=doc_id,
                section1=subsection1_title,
                doc_text=f'{page_title}\n{doc_text}',
                doc_len=len(doc_text),
                doc_words_count=len(set(doc_text.lower().split())),
                keywords=keywords
            )
            lines.append(line)

    print('found sections: ', len(lines))
    data = pd.DataFrame(lines)
    data['section01_path'] = data['section0'] + '/' + data['section1']
    data.to_csv(ofile_path, index=False)


def print_res(res):
    if len(res['hits']['hits']) > 0:
        ans_list = ["Here you can find the instructions: "]
        for i, item in enumerate(res['hits']['hits']):
            if i > MAX_ANSWER_COUNT:
                break
            doc_title = item['_source']['doc_title']

            doc_preview_text = '\n'.join(item['_source']["show_text"].split('\n')[2:])
            doc_preview_text = doc_preview_text[: MAX_TEXT_LEN] + '...'
            ans_line = "\n".join(["\n_______ " + f"<b>{doc_title}</b>", doc_preview_text, item['_source']['link']])
            if ans_line not in ans_list:
                ans_list.append(ans_line)

        return "\n".join(ans_list + ['___________________________________'])
    else:
        return "not found"


def get_doc_title(doc_text):
    lines = doc_text.split('\n')
    doc_title = f'{lines[0]}/{lines[1]}'
    return doc_title


def add_doc_to_index(doc):
    try:
        res = es.index(index="some-index", doc_type="text", body=doc)
    except Exception as ex:
        print(ex)
        pass


def build_index():
    subprocess.call('curl -XDELETE localhost:9200/some-index', shell=True)
    doc_dir = 'data'
    data = pd.read_csv(f'{doc_dir}/help_title_v2.csv')
    init_len = len(data)
    data = data.query('section_4 not in ["Overview", "Important Information"]')
    after_len = len(data)
    print('dropped ', init_len - after_len, ' rows')
    success_count = 0
    # section_1,url_1,section_2,url_2,section_3,url_3,section_4,url_4,section_text,keywords,text_len

    for doc_id, doc_row in data.iterrows():
        doc_title = f"{doc_row['section_1']}/{doc_row['section_2']}/{doc_row['section_3']}/{doc_row['section_4']}"
        doc_link = doc_row['url_4']

        keywords = doc_row['keywords'].replace('[', '').replace(']', '').replace("'", '') \
            if doc_row['keywords'] and doc_row['keywords'] == doc_row['keywords'] else ""

        text = doc_title + '\n' + str(doc_row['keywords']) + '\n' + str(doc_row['section_text'])
        section_text = str(doc_row['section_text'])
        if not section_text or len(section_text) < 20:
            continue

        doc = {"doc_id": doc_id,
               "doc_title": doc_title,
               "show_text": doc_row['section_text'],
               "text": text,
               "keywords": keywords,
               'link': doc_link,
               'section_1': doc_row['section_1'],
               'section_2': doc_row['section_2'],
               'section_3': doc_row['section_3'],
               'section_4': doc_row['section_4'],
               }
        try:
            res = es.index(index="some-index", doc_type="text", body=doc)
            success_count += 1
            print(success_count)
        except Exception as ex:
            print(ex)
            pass
    print(f'success {success_count / (doc_id + 1):0.2f}')
    check_elastic_ans()


def check_elastic_ans():
    test_q_list = [
        'Gantt chart',
        'Machine learning',
        'assign subtasks so that each team member (or team members)',
        'New tasks are created as backlogged by default and remain that way unless you add start and end dates to the task or convert it to a milestone',
        'what information is or is not copied when you duplicate tasks',
        'what information is or is not copied when you duplicate task',
        'what information about duplicated task',
        'How to move task to another column?'
    ]
    for test_q in test_q_list:
        answer = get_answer(test_q)
        print(test_q)
        print('\t', answer)


def run_elastic_circle():
    while True:
        query = input('input query:\n')
        if query == 'stop':
            break
        print('Your query:', query)
        answer = get_answer(query)
        print(answer)
        print()


def msg_to_doc(input_msg):
    try:
        text, *q_list = input_msg.split('\n')
        doc_list = []
        for q in q_list:
            if q:
                q_groups = re.findall(r'(.*\?) (.*\.) (.*.) (http.\://.*)', q)
                question, answer_title, answer, doc_link = q_groups[0]
                doc = {"doc_id": None,
                       "doc_title": answer_title,
                       "text": text,
                       "keywords": answer,
                       'link': doc_link,
                       'section0': None,
                       'section1': answer_title,
                       }
                doc_list.append(doc)
        return doc_list
    except:
        return


def main():
    # process_input_files()
    build_index()
    check_elastic_ans()
    run_elastic_circle()


if __name__ == '__main__':
    main()
