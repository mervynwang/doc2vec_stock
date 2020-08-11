from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime

soup = BeautifulSoup(open("./ust/content.html"), "html.parser")

dt = soup.select('div.gnt_ar_dt')[0]['aria-label']
dt = re.search('(\d+:\d+) (a\.m\.|p\.m\.) \w+ (\w{3}\. \d+, \d+)', dt)
print(dt.group(0))
print(dt.group(1))
print(dt.group(2))
print(datetime.strptime(dt.group(3), '%b. %d, %Y'))
print("=====")



artist = soup.select('article div.gnt_ar_by')
print(artist[0].text)
print("=====")

content = soup.select('article div.gnt_ar_b')
print(content[0].text)