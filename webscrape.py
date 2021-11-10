"""
This script will get the crypto descriptions scraping a website. The website is found lower in the url variable. 
This is the article I am following to learn how to do this

https://towardsdatascience.com/web-scraping-basics-82f8b5acd45c 
"""
from bs4 import BeautifulSoup
import requests 
import pandas as pd
import re 


url = "https://www.upfolio.com/100-coins-explained-backup"

req=requests.get(url)
content=req.text

# print(content)

soup=BeautifulSoup(content, features="lxml")

# print(soup)

names = soup.findAll("h3", {"class": "coinname"})
links = soup.findAll("a", {"class": "coinlink1"})
logo = soup.findAll("img",  {"class": "coinlogo"})
description = soup.findAll("p", {"class": "cointext"})

names = [x.text for x in names]
coin_name = [x[:x.find(" ")] for x in names]
print(coin_name)

tickers = [re.search('\(([^)]+)', x).group(0).replace('(', "") for x in names]
# print(tickers)

links = [x.get('href') for x in links]
logo = [x.get('src') for x in logo]
description = [x.text for x in description]

print(names)
# print(links)
# print(logo)
# print(description)

df = pd.DataFrame(list(zip(tickers, coin_name, links, logo, description)),
               columns =['Tickers', 'Name', 'Link', "Logo", "Description"])


df = df.set_index("Tickers")


print(df)

df.to_csv("Coins.csv")