from support_model import get_answer, ModelNames
import re
import pandas as pd
import numpy as np


df = pd.read_csv('data/all_dataset.csv')
# df = df.query('source == "from_wrike_org"')
# only qna labelled
#%%


def print_scores(df):
    lines = []
    for model_name in ModelNames:
        print(model_name)
        score_top_1 = 0
        score_top_3 = 0
        n = len(df)
        elapsed_list = []
        for q, true_link in zip(df['questions'].values, df['url_3'].values):
            start = pd.Timestamp.now()
            ans = get_answer(q, model_name=model_name)
            elapsed = pd.Timestamp.now() - start
            links = re.findall('(https?:.*)\s*', ans)
            if links:
                links = [x.strip().split('#')[0] for x in links]
                acc_top_1 = int(true_link == links[0])
                acc_top_3 = int(any(true_link == link for link in links[:3]))
            else:
                acc_top_1 = 0
                acc_top_3 = 0

            score_top_1 += acc_top_1
            score_top_3 += acc_top_3
            elapsed_list.append(elapsed)
            # print('\t\t', true_link, links, 'URL: ' in ans, 'acc_top_1:', acc_top_1)
        line = dict(
            model=model_name.value,
            acc_top_1=score_top_1 / n,
            acc_top_3=score_top_3 / n,
            elapsed=str(np.mean(elapsed_list)).replace("0 days ", "")
        )
        lines.append(line)
        # print(model_name.value, score_top_1 / n, score_top_3 / n, np.mean(elapsed_list))

    report = pd.DataFrame(lines)
    return report


for slice_name, df_slice in df.groupby('source'):

    df_slice = df_slice[['questions', 'url_3']].dropna()
    if len(df_slice) > 5:
        report = print_scores(df_slice)
        print(slice_name)
        print(report)
# old model
# from_wrike_org scores
#      model  acc_top_1  acc_top_3                   elapsed
# 0  elastic   0.142857   0.220238 0 days 00:00:00.008382589
# 1     bert   0.035714   0.053571 0 days 00:00:00.125237083
# 2      bpe   0.059524   0.101190 0 days 00:00:00.024513452
# 3    tfidf   0.125000   0.125000 0 days 00:00:00.201081690

# new model
# from_wrike_org
#      model  acc_top_1  acc_top_3             elapsed
# 0  elastic   0.142857   0.220238  00:00:00.005085732
# 1     bert   0.035714   0.053571  00:00:00.105197255
# 2      bpe   0.059524   0.101190  00:00:00.024737744
# 3    tfidf   0.125000   0.125000  00:00:00.280389505

# from_dirty_questions
#      model  acc_top_1  acc_top_3             elapsed
# 0  elastic   0.256545   0.350785  00:00:00.004212481
# 1     bert   0.073298   0.115183  00:00:00.182275057
# 2      bpe   0.109948   0.157068  00:00:00.025434586
# 3    tfidf   0.287958   0.298429  00:00:00.181515293

# from_crawl_spider
#      model  acc_top_1  acc_top_3             elapsed
# 0  elastic   0.214286   0.303571  00:00:00.004827672
# 1     bert   0.017857   0.059524  00:00:00.143165196
# 2      bpe   0.071429   0.130952  00:00:00.024092190
# 3    tfidf   0.791667   0.791667  00:00:00.094076059


