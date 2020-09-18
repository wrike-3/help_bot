from support_model import get_answer, ModelNames
import re
import pandas as pd
import numpy as np


df = pd.read_csv('data/all_dataset.csv')
df = df.query('source == "from_wrike_org"')
# only qna labelled
#%%
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
print('from_wrike_org scores')
print(report)

# from_wrike_org scores
#      model  acc_top_1  acc_top_3                   elapsed
# 0  elastic   0.142857   0.220238 0 days 00:00:00.008382589
# 1     bert   0.035714   0.053571 0 days 00:00:00.125237083
# 2      bpe   0.059524   0.101190 0 days 00:00:00.024513452
# 3    tfidf   0.125000   0.125000 0 days 00:00:00.201081690
