# %%
import pandas as pd

df = pd.read_csv('data/all_dataset.csv')
df
# %%
len(df.dropna(subset=['questions']))
# %%
df
# %%
df_info = pd.read_csv('data/help_title_v2.csv')
df_info

# Q
# How to plot Gantt Chart? -- class1
# Hello! you can use this tool for plotting -- class1

# A1
# - Hello! you can use this tool for plotting
#     https // wrikie..: -- content
#     class1

# Machine learning
