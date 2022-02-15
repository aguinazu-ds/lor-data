import pandas as pd
import glob, os, json
import numpy as np
from get_name_and_tag_by_ppuid import get_name_and_tag_by_ppuid
from api_token import api_token_var_list

df = pd.read_json('data/lor-match-data/match_data-20220212-040548.json')

df_list = []
for index in range(len(df.columns)):
    df_list.append(pd.DataFrame(df.iloc[:,index][index]))
    df_list[index]['API Key'] = df.columns[index]

for index in range(len(df_list)):
    df_list[index] = pd.concat([pd.json_normalize(df_list[index].iloc[:,0]),pd.json_normalize(df_list[index].iloc[:,1]), df_list[index]['API Key']], axis=1, join="inner")