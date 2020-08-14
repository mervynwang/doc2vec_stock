
import csv, requests
from datetime import datetime


level2 = []
possibleTag = ['money', 'tech']


with open('./data/USAToday.csv','r') as fin, open('./data/USAToday.money.csv','w') as fout:
	writer = csv.writer(fout, delimiter=',')
	for row in csv.reader(fin, delimiter=','):
		if row[4] not in level2 :
			level2.append(row[4])

		try:
			row[2] = datetime.strptime(row[1], '%Y/%m/%d').strftime('%Y/%B/%d/')
		except:
			pass
		# https://www.usatoday.com/sitemap/

		if row[4] in possibleTag:
			 writer.writerow(row)



