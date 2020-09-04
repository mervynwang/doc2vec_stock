
import re, csv

from datetime import datetime

from bs4 import BeautifulSoup


soup = BeautifulSoup(open("./wsj/arix.html"), "html.parser")

articles = soup.find_all('article')

#WSJTheme--pagepicker
main = soup.select('#main div[class^="WSJTheme--pagepicker"]')
pages = main[0].select('div[class*="-option-"]')
url = "wsj/"

nu = len(pages)
for page in range(2, nu):
	nurl = url + "?page="+ str(page)
	print(nurl)

# print(pages)
# print(len(pages))

# for headline in articles :
# 	titles = headline.select('h2 a')
# 	tags = headline.select('div span')
# 	# times = soup.select('div p')
# 	if not tags:
# 		print(headline.text)
# 		continue
# 	if not re.search("(Marketing|Markets|Stocks|Business)", tags[0].text):
# 		print(tags[0].text)
# 		# print(titles[0].text)
# # Marketing Markets Stocks Business
# 	# print(titles[0]["href"])
# 	# print(titles[0].text)



