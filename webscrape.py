"""
This script will get the crypto descriptions scraping a website. The website is found lower in the url variable. 
This is the article I am following to learn how to do this

https://towardsdatascience.com/web-scraping-basics-82f8b5acd45c 
"""
from bs4 import BeautifulSoup
import requests 


url = "https://www.upfolio.com/100-coins-explained-backup"

req=requests.get(url)
content=req.text

# print(content)

soup=BeautifulSoup(content)

# print(soup)

names = soup.findAll("h3", {"class": "coinname"})
links = soup.findAll("a", {"class": "coinlink1"})
logo = soup.findAll("img",  {"class": "coinlogo"})
description = soup.findAll("p", {"class": "cointext"})
print(names)
print(links)
print(logo)
print(description)