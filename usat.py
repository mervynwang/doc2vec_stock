import sys, os, re

from datetime import datetime

path = './data/usat/'
separator = "\n"
for news in os.listdir('./data/usat/'):
	with open(path + news , "r") as fo:
		if not news[0:2].isnumeric():
			continue;
		try:
			ffn = re.search('^(\d+)-([\w-]+)', news)
			id = ffn.group(1)
			title = ffn.group(2).replace('-', ' ').strip()

			data = fo.read().splitlines(True)
			date = str(data[0]).strip()
			data[1] = title + " \n"

			docs = separator.join(data[1:])
			docs = re.sub(r'([a-zA-Z]{2,})[\.\?\!]\s?', r'\1 \n', docs)
			docs = re.sub(r'Follow USA TODAY.*?@\w+', '', docs)
			# docs = docs.replace('"', '')
		except IndexError:
			print(news)
			continue

		if re.match('\d+-\d+-\d+', date) == None:
			print(path + news)
			continue

		with open('./data/usat3/' + date + '_' + id, 'w') as fout:
			fout.write(docs)


# news = '94063564-abercrombie-fitch'
# with open(path + news , "r") as fo:
# 	if not news[0:2].isnumeric():
# 		pass
# 	try:
# 		ffn = re.search('^(\d+)-([\w-]+)', news)
# 		id = ffn.group(1)
# 		title = ffn.group(2).replace('-', ' ').strip()

# 		data = fo.read().splitlines(True)
# 		date = str(data[0]).strip()
# 		data[1] = title + " \n"

# 		docs = separator.join(data[1:])
# 		docs = re.sub(r'([a-zA-Z]{2,})\.\s?', r'\1 \n', docs)
# 		docs = re.sub(r'Follow USA TODAY.*?@\w+', '', docs)

# 	except IndexError:
# 		print(news)
# 		pass

# 	if re.match('\d+-\d+-\d+', date) == None:
# 		print(path + news)
# 		pass

# 	with open('./data/usat3/' + date + '_' + id, 'w') as fout:
# 		fout.write(docs)


# soup = BeautifulSoup(open("./tmp/usat_3316895001.html"), "html.parser")

# dtD = soup.select('article div.gnt_ar_dt')
# print(dtD)
# if not dtD:
# 	dtD = soup.select('article span.asset-metabar-time')
# 	dtD = dtD[0].text
# else :
# 	dtD = dtD[0]['aria-label']

# ymd = re.search('(\d+:\d+) (a\.m\.|p\.m\.) \w+ (\w{3}\. \d+, \d+)', dtD).group(3)
# dt = datetime.strptime(ymd, '%b. %d, %Y').isoformat()

# artistD = soup.select('article div.gnt_ar_by')
# if not artistD:
# 	artistD = soup.select('article div.asset-metabar a')
# artist = artistD[0].text

# contentD = soup.select('article div.gnt_ar_b')
# if not contentD:
# 	contentD = soup.select('article p.p-text')

# content = ''
# for node in contentD:
# 	content += node.text

# print(content)

# # row = {"link": "http://link", "date" : dt, "artist" : artist, "content": content}
# # print(row)

# # dts = soup.select('div.gnt_ar_dt')[0]['aria-label']
# # dtg = re.search('(\d+:\d+) (a\.m\.|p\.m\.) \w+ (\w{3}\. \d+, \d+)', dts)

# # dt = datetime.strptime(dtg.group(3), '%b. %d, %Y')
# # artistd = soup.select('article div.gnt_ar_by')
# # artist = artistd[0].text
# # contentd = soup.select('article div.gnt_ar_b')
# # content = contentd[0].text

# # row = {"link": "http://link", "date" : dt, "artist" : artist, "content": content}


# # with open('us.csv', 'a', newline='') as csvfile:
# #     fieldnames = ['link', 'date', 'artist', 'content', 'ticker', 'source', '7d', '1m']
# #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# #     writer.writeheader()
# #     writer.writerow(row)



# # soup = BeautifulSoup(open("./ust/Sitemap.html"), 'html.parser')
# # # print(soup.text)
# # links = soup.find_all(href=re.compile("https://www.usatoday.com/story/money"))

# # page = soup.find_all(href=re.compile("https://www.usatoday.com/sitemap/\d+"))
# # url = ""
# # nextlink = []

# # for n in page:
# # 	# page = soup.find_all(href=re.compile("https://www.usatoday.com/sitemap/\d+"))
# # 	# print(n['href'])
# # 	for nextPage in page:
# # 		if nextPage['href'] == url:
# # 			continue
# # 		if nextPage['href'] not in nextlink:
# # 			nextlink.append(nextPage['href'])
# # 			print(nextPage['href'])

# # # li = soup.find_all("li", class_="sitemap-list-item")
# # for node in links:
# # 	# print(node['href'])
# # 	title, tid = re.search('\/([\w-]+)\/(\d+)\/$', node['href']).group(1, 2)
# # 	# print(title, tid)