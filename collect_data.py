#!/usr/bin/python3


import sys, os, re, csv, hashlib, datetime

# from datetime import datetime
from time import sleep, time
from random import uniform, randint


import requests
import argparse

from fake_useragent import UserAgent
from googlesearch import search
from dateutil.parser import parse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup



# ua = UserAgent()
#
# ua.firefox
# ua.chrome

# Randomization Related
MIN_RAND        = 0.64
MAX_RAND        = 1.27
LONG_MIN_RAND   = 4.78
LONG_MAX_RAND = 10.1



class collect(object):

	headless = False
	driver = None
	collect_start = datetime.datetime(2013, 1, 1)
	collect_end = datetime.datetime(2020, 8, 1)
	headers = {}
	stockDict = {}
	ticker_info = {
				'google' : {
					'keywords' : ['Alphabet Inc', 'Google LLC'],
					'name' : 'GOOGL'
				},
				'biogen' : {
					'keywords' : ['Biogen Idec Inc'],
					'name' : 'BIIB'
				},
				'tesla' : {
					'keywords' : ['Tesla Inc', 'elon musk', 'TSLA'],
					'name' : 'TSLA'
				},
				'amd'  : {
					'keywords' : ['Advanced Micro Devices Inc', 'AMD'],
					'name' : 'AMD'
				}
			}

	newsCsv = './data/news.csv'
	links = []



	"""docstring for collect"""
	def __init__(self):
		super(collect, self).__init__()
		ua = UserAgent()
		self.headers = {'user-agent': ua.chrome}
		self.mkdir("./data")
		self.mkdir("./tmp")


	def __del__(self):
		if self.driver is not None and self.quit :
			self.driver.quit()


	"""docstring for collect"""
	def setArgv(self):
		parser = argparse.ArgumentParser(description='input stock name, apiKey(tiingo & google search)')
		parser.add_argument('-l', '--headless', type=self.str2bool, default=False, help='headless mode (1|0)')
		parser.add_argument('-n', '--nu', type=int, default=0, help='news list start from nu')

		parser.add_argument('-s', '--ticker', type=str, help='stock name(google|biogen|tesla|amd)')
		parser.add_argument('-t', '--tiingo', type=str, help='tiingo api key')

		parser.add_argument('-a', '--account', type=str, help='news account')
		parser.add_argument('-p', '--password', type=str, help='news account password')

		parser.add_argument('-f', '--file', type=str, help='parser file')

		parser.add_argument('-r', '--reset', type=self.str2bool, default=False, help='clean csv (1|0)')
		parser.add_argument('-d', '--debug', type=self.str2bool, default=True, help='debug info (1|0)')
		parser.add_argument('-q', '--quit', type=self.str2bool, default=True, help='quit selenium on end (1|0)')

		parser.add_argument('source', help='wsj|usat|ft|tii|eps')

		args = parser.parse_args(namespace=self)

		if args.reset == True:
			try:
				os.remove(self.fnlist+'.bak')
				os.rename(self.fnlist, self.fnlist+'.bak')

				# os.remove(self.newsCsv)
				# os.rename(self.newsCsv, self.newsCsv+'.bak')
			except OSError:
				pass

		return self

	"""docstring for collect"""
	def run(self):
		if self.source == "usatf":
			self.ust_content(self.file, False)

		if self.source == "wsjf":
			pass
			# self.ust_content(self.file, False)

		if self.source == "ftf":
			pass
			# self.ust_content(self.file, False)


		self.mkdir("./data/" + self.source)
		self.fnlist = "./data/news_list_" + self.source

		if self.source == "tii":
			self.daily()
			self.tii_news()

		if self.source == "usat":
			self.ust_sitemap()
			self.newslist_fetch(self.ust_content)

		if self.source == "wsj":
			self.wsj_arix()
			self.newslist_fetch(self.wsj_content)

		if self.source == "ft":
			if self.account is None:
				print("need account ")
				exit()

			self.ft()

		if self.source == "ftc":
			if self.account is None:
				print("need account ")
				exit()

			self.ft_formCsv()

		if self.source == "eps":
			self.eps()


	"""docstring for collect"""
	def tii(self, url, fn):
		if url is None or fn is None:
			return
		headers = {
			'Content-Type': 'application/json'
		}
		requestResponse = requests.get(url, headers=headers)
		with open(fn, "a") as fo:
			fo.write(requestResponse.text)
		return

	"""docstring for collect"""
	def daily(self):
		if self.tiingo is None:
			return;

		date = self.collect_start.strftime('%Y-%m-%d')
		ticker = self.ticker_info[self.ticker]['name']
		url = "https://api.tiingo.com/tiingo/daily/" + ticker + "/prices?startDate="+date+"&token=" + self.tiingo
		fn = './data/stock/' + ticker+"_prices.json"
		self.tii(url, fn)

	"""docstring for collect"""
	def tii_news(self):
		if self.tiingo is None:
			return;
		date = self.collect_start.strftime('%Y-%m-%d')
		ticker = self.ticker_info[self.ticker]['name']
		url = "https://api.tiingo.com/tiingo/news?startDate="+date+"&token=" + self.tiingo + "&tickers=" + ticker
		fn = './data/tiinews/' + ticker + "_news.json"
		self.tii(url, fn)

	def eps(self):
		# https://api.tiingo.com/tiingo/fundamentals/<ticker>/statements?startDate=2019-06-30
		if self.tiingo is None:
			return;
		date = self.collect_start.strftime('%Y-%m-%d')
		ticker = self.ticker_info[self.ticker]['name']
		url = "https://api.tiingo.com/tiingo/fundamentals/" + ticker + "/statements?startDate=" + date + '&token=' + self.tiingo
		print(url)
		fn = './data/eps/' + ticker + ".json"
		self.tii(url, fn)

	def stock2Json(self):
		ticker = self.ticker_info[self.ticker]['name']
		fn = './data/stock/' + ticker+ "_prices.json"
		with open(fn, 'r') as stock:
			stockList = json.load(stock)
			for node in stockList:
				date = node['date'][0:10]
				self.stockDist[date] = node

	"""docstring for collect"""
	def dayMove(self, dd, n):
		end = datetime.datetime(2020, 5, 30)

		if n > 0 :
			dd = dd + datetime.timedelta(days=n)
		dd1 = datetime.timedelta(days=1)
		while True:
			ds = dd.isoformat()[0:10]
			if ds in self.stockDist:
				return self.stockDist[ds]

			# print("%s : %s", dd, n)
			if n == 0:
				dd = dd - dd1
			else:
				dd = dd + dd1

			if dd >= end :
				break
		return False

	"""docstring for collect"""
	def toNewsCsv(self, url, source, ds):
		date = datetime.strptime(ds['date'][0:10], '%Y-%m-%d')
		st0 = self.dayMove(date, 0)
		st7 = self.dayMove(date, 7)
		st30 = self.dayMove(date, 30)

		with open(self.newsCsv, 'a', newline='') as csvfile:
			fieldnames = ['link', 'date', 'artist', 'content', 'ticker', 'source', '0d', '7d', '1m']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			writer.writerow({
				'link' : url,
				'date' : ds['date'],
				'artist' : ds['artist'],
				'content' : ds['content'],
				'ticker' : self.ticker,
				'source' : source,
				'0d' : st0,
				'7d' : st7,
				'1m' : st30,
				})

	def newslist_fetch(self, content_parser):
		i = 1
		with open(self.fnlist , "r") as fo:
			for url in fo:
				i = i + 1
				if self.nu >= i:
					continue

				url = url.rstrip()
				self.log(str(i) + "  " + url);
				content_parser(url, False)
				self.wait_between(True)

	"""docstring for collect"""
	def ft(self):
		self.ft_login()

		''' After login, Index Go search '''
		for ticker in self.ticker_info:
			for kw in self.ticker_info[ticker]['keywords']:
				self.ft_search(ticker, kw, 1)
				self.ft_search(ticker, kw, 2)
			self.links = list(dict.fromkeys(self.links))

			# for log
			for url in self.links:
				with open("./tmp/ft_to_"+ticker , 'a+') as f:
					f.write("%s\n" % url)

		self.ft_conetnet()
		# done

	def ft_login(self):
		self.setUp()
		driver = self.driver

		driver.get('https://www.ft.com')

		login = WebDriverWait(driver, 20).until(
		EC.presence_of_element_located((By.XPATH ,
			"/html/body/div/div[1]/header[1]/nav[2]/div/ul[2]/li[1]/a")) #sign-in
		)
		login.click()

		''' Login '''
		WebDriverWait(driver, 20).until(
				EC.presence_of_element_located((By.ID ,"enter-email"))
				)

		#account
		inputs = driver.find_element_by_xpath('//*[@id="enter-email"]')
		self.key_in(inputs, self.account)
		driver.find_element_by_xpath('//*[@id="enter-email-next"]').click()

		#password
		inputs = WebDriverWait(driver, 20).until(
				EC.presence_of_element_located((By.ID ,"enter-password"))
				)

		if self.password is not None:
			self.key_in(inputs, self.password)
			driver.find_element_by_xpath('//*[@id="sign-in-button"]').click()

		print("google recaptcha wait... ...")
		while wait:
			try:
				#  do check recaptcha completed
				WebDriverWait(self.driver, 120, 1).until(EC.presence_of_element_located((By.ID, "o-header-search-primary")))
				wait = False
			except NoSuchElementException:
				wait = True
				pass
		print("go search... ")


	def ft_search(self, ticker, keyword, sortBy = 1):
		print(keyword)

		self.driver.get('https://www.ft.com')
		WebDriverWait(self.driver, 40, 1).until(EC.presence_of_element_located((By.ID, "o-header-search-primary")))
		self.driver.find_element_by_xpath('//*[@id="site-navigation"]/div[1]/div/div/div[1]/a[2]').click()
		inputs = self.driver.find_element_by_xpath('//*[@id="o-header-search-term-primary"]')
		inputs.send_keys(keyword)
		inputs.send_keys(Keys.RETURN)

		try:
			# sort by date;
			# //*[@id="site-content"]/div/div[1]/div[1]/div[1]/div/div[2]/a[2]
			sortByRele = '/html/body/div[1]/div[2]/div/div/div/main/div/div[1]/div[1]/div[1]/div/div[2]/a[1]'
			sortByDate = '/html/body/div[1]/div[2]/div/div/div/main/div/div[1]/div[1]/div[1]/div/div[2]/a[2]'

			if sortBy == 1:
				WebDriverWait(self.driver, 10, 6).until(
					EC.presence_of_element_located((By.XPATH, sortByRele))
					)
			else:
				WebDriverWait(self.driver, 10, 6).until(
					EC.presence_of_element_located((By.XPATH, sortByDate))
					).click()

			self.wait_between()
		except:
			print("sort by date no found")
			pass
		finally:
			pass

		nextPagePath = '//a[@class="search-pagination__next-page o-buttons o-buttons--secondary o-buttons-icon o-buttons-icon--arrow-right o-buttons--big o-buttons-icon--icon-only"]'  # all match
		nextPage = True

		i = 0
		while nextPage is not None:
			self.wait_between(True)
			soup = BeautifulSoup(self.driver.page_source, 'html.parser')
			ul = soup.select('main ul[class="search-results__list"] li')
			for li in ul:
				header = li.find('a', class_='js-teaser-heading-link')
				subtitle = li.find('div', class_='o-teaser__meta')
				time = li.find('time')
				url = header['href']
				i = i +1
				self.links.append(header['href'])
				with open("./data/ft_news_list" , "a+") as fo:
					writer = csv.writer(fo)
					writer.writerow([ticker, time.text, header.text, url])

				self.wait_between()
			try:
				nextPage = WebDriverWait(self.driver, 20, 1).until(
					EC.presence_of_element_located((By.XPATH, nextPagePath)))
				nextPage.click()

			except:
				print(nextPage)
				nextPage = None
				print("End, Next kw, total %s", i)

				with open("./tmp/ft_"+ keyword.replace(' ', '_')  +"_end.html", 'a') as f:
					f.write(self.driver.page_source)

			finally:
				pass


	def ft_formCsv(self):
		with open("./data/ft_news_list") as cf:
			rows = csv.reader(fo)
			for line in rows:
				self.links.append(line[4])

		self.links = list(dict.fromkeys(self.links))

		print("total %s", len(self.links))
		self.ft_login()
		sleep(5)
		self.ft_conetnet()


	"""docstring for collect"""
	def ft_conetnet(self):
		baseUrl = 'https://www.ft.com'

		i = 0
		for url in self.links:
			try:
				tid = re.search('\/([\w-]+)$', url).group(1)
				if url[0:4] == "http":
					goUrl = baseUrl + url
				print(goUrl)

				# WebDriverWait(self.driver, 10, 6).until(
				# 	EC.presence_of_element_located((By.XPATH, sortByRele))
				# 	)
				self.wait_between()
				self.driver.get(goUrl)
				self.wait_between(True)


				soup = BeautifulSoup(self.driver.page_source, 'html.parser')


				content = soup.find('div', class_="article__content-body")
				ps = content.find_all('p')
				ts = soup.find('time')
				ts = ts['datetime']
				ts = parse(ts).date()
				date = str(ts)
				content = ''
				for p in ps:
					content = content + p.text

				with open("./data/ft/"+ date + '_' + tid  , "a") as fo:
					fo.write(content)

			except:
				self.log("Error %s, %s : %s" % (i, sys.exc_info()[0], url) )

				fn = "./tmp/ft_" + date + "_"+ tid + ".html"
				self.log("new html type : %s on %s" % (url, fn))

				# log url
				with open("./tmp/ft_to", 'a') as f:
					f.write("%s" % url)

				# write html content
				with open(fn, 'a') as f:
					f.write(self.driver.page_source)

			finally:
				i = i+1
				pass



	# https://www.djreprints.com/menu/other-services/
	# http://www.management.ntu.edu.tw/CSIC/DB/Factiva
	# https://developer.dowjones.com/site/global/home/index.gsp
	# https://www.wsj.com/search/term.html?KEYWORDS=BIIB&mod=searchresults_viewallresults
	# OR https://www.wsj.com/market-data/quotes/TSLA
	#
	# https://www.wsj.com/news/archive/2020/08/18
	"""docstring for collect"""
	def wsj_arix(self):
		if os.path.exists(self.fnlist):
			return

		baseUrl = 'https://www.wsj.com/news/archive/'
		date = self.collect_end
		d1 = datetime.timedelta(days=1)

		with open(self.fnlist , "w+") as fo:
			fo.write("")

		while date > self.collect_start:
			self.wait_between()
			date = (date - d1)
			url = baseUrl + date.strftime('%Y/%m/%d/').lower()
			print("start  %s", url)
			news, nextpage = self.wsj_arix_parser(url)

			for page in range(2, nextpage):
				nurl = url + "?page=" + str(page)
				news_child, _ = self.wsj_arix_parser(nurl)
				self.wait_between()
				news.extend(news_child)

			for news_url in news:
				with open(self.fnlist , "a") as fo:
					fo.write(news_url+"\n")

			news = []
			nextpage = 0


	def wsj_login(self):
		if not self.driver:
			self.setUp()
		driver = self.driver
		loginUrl = 'https://sso.accounts.dowjones.com/login?state=g6Fo2SBiYlhrLUZCUmY1b0xiVTBsZkF0UTkyMEZEX3ozOXZpNKN0aWTZIGJBaEN4R2dDcGQzY3hIYktyZFJGazRjZlBmZVZ2czllo2NpZNkgNWhzc0VBZE15MG1KVElDbkpOdkM5VFhFdzNWYTdqZk8&client=5hssEAdMy0mJTICnJNvC9TXEw3Va7jfO&protocol=oauth2&scope=openid%20idp_id%20roles%20email%20given_name%20family_name%20djid%20djUsername%20djStatus%20trackid%20tags%20prts&response_type=code&redirect_uri=https%3A%2F%2Faccounts.wsj.com%2Fauth%2Fsso%2Flogin&nonce=2f4078c1-39fe-4c4a-9abe-a36a8399ad40&ui_locales=en-us-x-wsj-83-2&ns=prod%2Faccounts-wsj&savelogin=on#!/signin'
		driver.get(loginUrl)

		login = WebDriverWait(driver, 20).until(
		EC.presence_of_element_located((By.XPATH ,
			'//*[@id="username"]')) #sign-in
		)
		self.moveWait(login)
		self.key_in(login, self.account)

		pw = EC.presence_of_element_located((By.ID ,'//*[@id="password"]'))
		self.key_in(pw, self.password)
		self.moveWait(pw)

		driver.find_element_by_xpath('//*[@id="basic-login"]/div[1]/form/div/div[6]/div[1]/button').click()




	""" wsj_arix_parser """
	def wsj_arix_parser(self, url):
		r = requests.get(url, headers=self.headers)
		if r.status_code != requests.codes.ok:
			print("Error On %s : return %s", url, r.status_code)
			return [[], 0]

		newslinks = [];
		pages = 0;
		soup = BeautifulSoup(r.text, 'html.parser')
		articles = soup.find_all('article')

		for headline in articles :
			titles = headline.select('h2 a')
			tags = headline.select('div span')
			if not tags:
				continue;

			if not re.search("(Marketing|Markets|Stocks|Business)", tags[0].text):
				continue

			if not titles:
				continue

			newslinks.append(titles[0]['href'])

		main = soup.select('#main div[class^="WSJTheme--pagepicker"]')
		if not main:
			pages = 0
		else:
			pages = main[0].select('div[class*="-option-"]')
			pages = len(pages)

		return [newslinks, pages]

	def wsj_content(self, url):



		soup = BeautifulSoup(r.text, 'html.parser')

		titleDoms = soup.select("article h1.wsj-article-headline")

		artistDoms = soup.select("article div.author-container")

		contentDom = soup.select("article div.wsj-snippet-body")
		pass




	"""docstring for collect"""
	def usat_search(self):
		fn = "./url.temp"
		if os.path.exists(fn) == True:
			with open(fn, 'r', newline='', encoding='utf-8') as f:
				url = f.readline()
				while url:
					print(url)
					self.wait_between()
					self.ust_content(url, True)
					url = f.readline()
			try:
				os.remove(self.newsCsv)
			except :
				pass
			return

		self.setUp()
		driver = self.driver
		base = 'https://www.usatoday.com'
		newslinks = []

		ticker = self.ticker_info[self.ticker]['name']
		for kw in self.ticker_info[self.ticker]['keywords']:
			print("keyword: " + kw )

			driver.get('https://www.usatoday.com/search/?q=' +kw )
			nextPageClass = '//a[@class="gnt_se_pgn_a gnt_se_pgn_pn gnt_se_pgn_pn__nt"]'  # all match
			nextPage = WebDriverWait(driver, 20).until(
				EC.presence_of_element_located((By.XPATH, nextPageClass))
			)

			while nextPage is not None:
				soup = BeautifulSoup(driver.page_source, 'html.parser')
				links = soup.find_all("a", class_="gnt_se_a")
				for arch in links:
					# print(arch['href'])
					newslinks.append(base + arch['href'])
				self.wait_between()
				nextPage.click() # next

				try:
					nextPage = WebDriverWait(driver, 20).until(
						EC.presence_of_element_located((By.XPATH, nextPageClass)))
				except:
					print("nextPage None")
					nextPage = None

		newslinks = list(dict.fromkeys(newslinks))
		with open(fn, 'w', newline='') as f:
			for url in newslinks:
				f.write("%s\n" % url)

		for url in newslinks:
			# print(url)
			self.wait_between()
			self.ust_content(url)

		if os.path.exists(fn) == True:
			os.reomve(fn)

	"""docstring for collect"""
	def ust_sitemap(self):
		if os.path.exists(self.fnlist):
			return

		baseUrl = 'https://www.usatoday.com/sitemap/'
		date = self.collect_end
		d1 = datetime.timedelta(days=1)

		while date > self.collect_start:
			self.wait_between()
			date = (date - d1)
			url = baseUrl + date.strftime('%Y/%B/%d/').lower()
			print("start  %s", url)
			news, nextpage = self.ust_sitemap_parser(url)
			for nurl in nextpage:
				news_child, _ = self.ust_sitemap_parser(nurl)
				self.wait_between()
				news.extend(news_child)

			for news_url in news:
				with open(self.fnlist , "w+") as fo:
					fo.write(news_url+"\n")

			news = nextpage = []

	"""docstring for collect"""
	def ust_sitemap_parser(self, url):
		r = requests.get(url, headers=self.headers)
		if r.status_code != requests.codes.ok:
			print("Error On %s : return %s", url, r.status_code)
			return [[], []]

		soup = BeautifulSoup(r.text, 'html.parser')
		links = soup.find_all(href=re.compile("https://www.usatoday.com/story/money"))
		newslinks = [];
		nextlink = [];
		for node in links:
			newslinks.append(node['href'])

		page = soup.find_all(href=re.compile("https://www.usatoday.com/sitemap/\d+"))
		for nextPage in page:
			if nextPage['href'] == url:
				continue
			if nextPage['href'] not in nextlink:
				nextlink.append(nextPage['href'])
		return [newslinks, nextlink]


	"""docstring for collect"""
	def ust_content(self, link, csv):

		if link[0:4] == "http":
			try:
				title, tid = re.search('\/([\w-]+)\/(\d+)\/$', link).group(1,2)
			except:
				self.log("Error : %s" % link)
				title = ""
				tid = "0"

			try:
				r = requests.get(link, headers=self.headers)
				if r.status_code != requests.codes.ok:
					self.log("Error On %s : return %s" % (link, r.status_code))
				text = r.text
			except:
				self.log("Error %s : %s" % (sys.exc_info()[0], link) )

		else:
			text = open(link)


		soup = BeautifulSoup(text, "html.parser")

		try:
			date, artist, content = self.usat_t1(soup) or self.usat_t2(soup)
			if date:
				with open("./data/usat/"+ date + '_' + tid  , "a") as fo:
					fo.write(content)
			else:
				self.log("Error date is False : %s" % (link) )

		except:
			self.log("Error %s : %s" % (sys.exc_info()[0], link) )
			if not self.file:
				fn = "./tmp/usat_" + date + "__"+ tid + ".html"
				self.log("new html type : %s on %s" % (link, fn))

				with open("./tmp/usat_to", 'a') as f:
					f.write("%s" % link)

				with open(fn, 'a') as f:
					f.write(text)
		finally:
			pass


	"""type 1"""
	def usat_t1(self, soup):
		dtD = soup.select('article div.gnt_ar_dt')
		if not dtD:
			return False

		dtD = dtD[0]['aria-label']
		ymd = re.search('(\d+:\d+) +[ap]\.m\. +\w+ (\w+[\ \.]*\d+, +\d+)', dtD).group(2)
		dt = parse(ymd).date()

		artistD = soup.select('article div.gnt_ar_by')
		artist = artistD[0].text

		contentD = soup.select('article div.gnt_ar_b')
		content = ''
		for node in contentD:
			content += node.text
		return str(dt), artist, content

	"""type 2"""
	def usat_t2(self, soup):
		dtD = soup.select('article span.asset-metabar-time')
		if not dtD:
			return False

		dtD = dtD[0].text    #Published 6:00 a.m. ET Dec. 5, 2019 | Updated 4:34 p.m. ET Dec. 5, 2019
		ymd = re.search('(\d+:\d+) +[ap]\.m\. +\w+ (\w+[\ \.]*\d+, +\d+)', dtD).group(2)
		dt = parse(ymd).date()


		artistD = soup.select('article div.asset-metabar span.asset-metabar-author')
		artist = artistD[0].text

		contentD = soup.select('article p.p-text')
		content = ''
		for node in contentD:
			content += node.text

		return str(dt), artist, content



	"""docstring for collect"""
	def goo_search(self, site):
		if self.google is None :
			return
		try:
			ff = self.site[site]
		except KeyError:
			print('site not exist ' + site)
			return
		q = self.ticker + ("" if site is None else "%20+site:%20" + self.site[site])
		# q = urllib.parse.quote(q)
		if self.debug:
			print(q)
		for link in search(q, lang = 'en', tld="com",
				num = 10,     # Number of results per page
				start = 0,    # First result to retrieve
				stop = None,  # Last result to retrieve
				pause = 2.0,  # Lapse between HTTP requests)
			):
			print(link)

	"""argv bool"""
	def str2bool(self, v):
		if isinstance(v, bool):
		   return v
		if v.lower() in ('yes', 'true', 't', 'y', '1'):
			return True
		elif v.lower() in ('no', 'false', 'f', 'n', '0'):
			return False
		else:
			raise argparse.ArgumentTypeError('Boolean value expected.')
		return

	# Setup settings
	def setUp(self):
		profile = webdriver.FirefoxProfile()
		# profile._install_extension("buster_captcha_solver_for_humans-0.7.2-an+fx.xpi", unpack=False)
		# profile.set_preference("security.fileuri.strict_origin_policy", False)
		# profile.set_preference("general.useragent.override", fua)
		profile.update_preferences()
		capabilities = webdriver.DesiredCapabilities.FIREFOX
		capabilities['marionette'] = True

		options = webdriver.FirefoxOptions()
		# options.add_option('useAutomationExtension', False)
		options.headless = self.headless

		self.driver = webdriver.Firefox(options=options, capabilities=capabilities, firefox_profile=profile, executable_path='./geckodriver')
		self.driver.set_window_size(1024, 1024)

	# Simple logging method
	def log(self,t=None):
		if not self.debug :
			return

		now = datetime.datetime.now()
		if t is None :
				t = "Main"
		print ("%s :: %s  " % (str(now), t))

	# Use time.sleep for waiting and uniform for randomizing
	def wait_between(self, longer = False):
		if longer :
			rand=uniform(MIN_RAND, LONG_MAX_RAND)
		else:
			rand=uniform(MIN_RAND, MAX_RAND)
		sleep(rand)

	# Using B-spline for simulate humane like mouse movments
	def human_like_mouse_move(self, action, start_element):
		points = [[6, 2], [3, 2],[0, 0], [0, 2]];
		points = np.array(points)
		x = points[:,0]
		y = points[:,1]

		t = range(len(points))
		ipl_t = np.linspace(0.0, len(points) - 1, 100)

		x_tup = si.splrep(t, x, k=1)
		y_tup = si.splrep(t, y, k=1)

		x_list = list(x_tup)
		xl = x.tolist()
		x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

		y_list = list(y_tup)
		yl = y.tolist()
		y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

		x_i = si.splev(ipl_t, x_list)
		y_i = si.splev(ipl_t, y_list)

		startElement = start_element

		action.move_to_element(startElement);
		action.perform();

		c = 5 # change it for more move
		i = 0
		for mouse_x, mouse_y in zip(x_i, y_i):
			action.move_by_offset(mouse_x,mouse_y);
			action.perform();
			self.log("Move mouse to, %s ,%s" % (mouse_x, mouse_y))
			i += 1
			if i == c:
				break;

	def moveWait(self, ele):
		driver = self.driver
		action =  ActionChains(driver);
		self.human_like_mouse_move(action, ele)
		self.wait_between()

	def key_in(self, controller, keys, min_delay=0.05, max_delay=0.25):
		for key in keys:
			controller.send_keys(key)
			sleep(uniform(min_delay,max_delay))

	""" mkdir """
	def mkdir(self, path):
		if os.path.isdir(path) == False:
			os.makedirs(path, exist_ok=True)


###
if __name__ == '__main__':
	co = collect()
	co.setArgv().run()
