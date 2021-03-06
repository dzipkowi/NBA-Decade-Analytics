# -*- coding: utf-8 -*-
"""Team Data Scraper 2010-2020.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1h8lyDhxmHyXCkCcyS1kk5NcuHrqTBbBj
"""

import requests
from bs4 import BeautifulSoup
from bs4 import Comment
import pandas as pd
import sqlite3

#Set Scraper to Start in 2010
start_year = 2010

#Set End Year to 10 Years Later
end_year = start_year + 10

#Create Empty Dataframes
df = []
dataframe = pd.DataFrame()

#Loop through each year from Start to End
#Scrape the Table we want
#Append the New Data to Dataframe
for year in range(start_year, end_year):
    url = 'https://www.basketball-reference.com/leagues/NBA_' + str(year) + '.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    tables = []
    for each in comments:
        if 'table' in each:
          try:
            tables.append(pd.read_html(each)[0])
          except:
              continue
    df = tables[7]  
    df.columns = df.columns.droplevel(0)
    df['Year'] = str(year)
    dataframe = dataframe.append(df)

#Drop Unecessary Columns
dataframe.drop(dataframe.columns[[0, 18, 19, 20, 21, 22, 23, 24]], axis=1, inplace=True)

#Write to SQLite Database File
conn = sqlite3.connect('team_history.sqlite')
dataframe.to_sql('TEAM_HISTORY', conn, if_exists='replace', index=False)

