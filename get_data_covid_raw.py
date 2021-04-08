import io
import requests
from os import path
import pandas as pd
from datetime import datetime, timedelta

for i in range(1,26):
    url = "https://api.covid19india.org/csv/latest/raw_data" + str(i) + ".csv"
    print(url)
    r = requests.get(url)
    if i == 1:
        df = pd.read_csv(url)
    else:
        dx = pd.read_csv(url)
        df = df.append(dx)
    open("./dataset/covid_data_raw_" + str(i).zfill(2) + ".csv", "w", encoding="utf-8").write(r.text)

df.loc[(df.Gender == 'M'),'Gender']='Male'
df.loc[(df.Gender == 'M,'),'Gender']='Male'
df.loc[(df.Gender == 'F'),'Gender']='Female'
df.loc[(df.Gender == 'Femal e'),'Gender']='Female'

df["Date"] = df["Date Announced"].str.slice(6, 10) + "-" + df["Date Announced"].str.slice(3, 5) + "-" + df["Date Announced"].str.slice(0, 2)
df["Age"] = pd.to_numeric(df["Age Bracket"], errors='ignore', downcast='integer')
df["Age Group"] = df["Age"].apply(lambda x: str(round(int(x)/10)*10).zfill(3) + "-" + str((round(int(x)/10)*10) + 9).zfill(3) if str(x).isnumeric() else "")

df.to_csv("./dataset/covid_data.csv",index=False)