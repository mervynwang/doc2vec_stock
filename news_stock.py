
import csv, requests, json
import datetime


level2 = []
possibleTag = ['money', 'tech']
stockDist = {}

with open("tsla.js", 'r') as stock:
	stockList = json.load(stock)

for node in stockList:
	date = node['date'][0:10]
	stockDist[date] = node

def daypp(dd, n):
	end = datetime.datetime(2020, 5, 30)
	if n > 0 :
		dd = dd + datetime.timedelta(days=n)
	dd1 = datetime.timedelta(days=1)
	while True:
		ds = dd.isoformat()[0:10]
		if ds in stockDist:
			return stockDist[ds]
		print("%s : %s", dd, n)
		if n == 0:
			dd = dd - dd1
		else
			dd = dd + dd1

		if dd >= end :
			break
	return False


with open('./data/news.csv','r') as fin, open('./data/news.stock.csv','w') as fout:
	# link,date,artist,content,ticker,source,7d,1m
	writer = csv.writer(fout, delimiter=',')

	for row in csv.reader(fin, delimiter=','):
		if row[1] == "date":
			continue
		dto = datetime.datetime.strptime(row[1][0:10], '%Y-%m-%d')
		st0 = daypp(dto, 0)
		st7 = daypp(dto, 7)
		st30 = daypp(dto, 30)

		row[6] = st7
		row[7] = st30
		row.append(st0)
		writer.writerow(row)

		# if row[4] not in level2 :
		# 	level2.append(row[4])

		# try:
		# 	row[2] = datetime.strptime(row[1], '%Y/%m/%d').strftime('%Y/%B/%d/')
		# except:
		# 	pass
		# # https://www.usatoday.com/sitemap/

		# if row[4] in possibleTag:
		#



