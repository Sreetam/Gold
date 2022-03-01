#!/usr/bin/env python
# coding: utf-8

#!/usr/bin/env python
# coding: utf-8

import requests 
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
site = 'https://finance.yahoo.com/quote/GC%3DF/history?period1=967593600&period2=1646006400&interval=1d&filter=history&frequency=1d'
raw = requests.get(site, headers=headers)
soup = BeautifulSoup(raw.content, 'html.parser')

data = []
for i in soup.find_all('tr'):
    row = [i.text for i in i.find_all('span')]
    for j in range(1, len(row)):
        try:
            row[j] = float(row[j].replace(',', ''))
        except:
            row[j] = row[j].replace('*', '')
    data.append(row)
dfn = pd.DataFrame(data[1:100], columns=data[0])

dfc = pd.read_csv('Gold.csv')
df = pd.concat([dfc, dfn])
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(by='Date')
for i in df.columns[1:]:
    ar = df[i].values
    for j in range(len(ar)):
        try:
            ar[j] = float(ar[j])
        except:
            ar[j] = np.nan
    df[i] = ar
df.drop_duplicates(subset=['Date'], inplace=True)
df.set_index("Date", inplace=True)
date = pd.date_range(df.index[0],df.index[len(df.index)-1],freq='d')

filled = []
for i in date:
    try:
        filled.append(df.loc[i].values)
    except:
        filled.append(np.array([np.nan for i in df.columns]))
filled_df = pd.DataFrame(filled, columns=df.columns, index=date)
filled_df.index.rename('Date', inplace=True)
filled_df.to_csv("Gold.csv", index=True)