from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime

soup = BeautifulSoup(open("./ust/content.html"), "html.parser")

dts = soup.select('div.gnt_ar_dt')[0]['aria-label']
dtg = re.search('(\d+:\d+) (a\.m\.|p\.m\.) \w+ (\w{3}\. \d+, \d+)', dts)

dt = datetime.strptime(dtg.group(3), '%b. %d, %Y')
artistd = soup.select('article div.gnt_ar_by')
artist = artistd[0].text
contentd = soup.select('article div.gnt_ar_b')
content = contentd[0].text

row = {"link": "http://link", "date" : dt, "artist" : artist, "content": content}


with open('us.csv', 'a', newline='') as csvfile:
    fieldnames = ['link', 'date', 'artist', 'content', 'ticker', 'source', '7d', '1m']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow(row)
