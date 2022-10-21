import json
import numpy as np
import pandas as pd
import json

def apt_search(x):
    아파트_최종 = pd.read_csv('web/real_estate/아파트_전처리_단지명포함_최종.csv')
    cond = 아파트_최종['단지명'].str.contains(x)
    size = sorted(아파트_최종[cond]['평'].unique())
    year = dict()
    price= dict()
    for i in size:
        year[f'{i}평'] = sorted(list(set(map(int,아파트_최종[cond][아파트_최종[cond]['평']==i]['계약년'].values))))
        price[f'{i}평'] = list(np.round(아파트_최종[cond][아파트_최종[cond]['평']==i].groupby('계약년').mean()['거래금액(만원)'],-3).astype('int').values/10000)
    return year,price
if __name__ == "__main__":
    x = '한남더힐'
    apt_search(x)
