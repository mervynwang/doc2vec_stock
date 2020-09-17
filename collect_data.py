#!/usr/bin/python3


import sys, os, re, csv, hashlib, datetime, glob, json, math

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
	headers = {}

	collect_start = datetime.datetime(2013, 1, 1)
	collect_end = datetime.datetime(2020, 5, 30)
	ticker_info = {
				'google' : {
					'keywords' : ['Alphabet Inc', 'Google LLC'],
					'name' : 'GOOGL',
					'stock':{}
				},
				'biogen' : {
					'keywords' : ['Biogen Idec Inc'],
					'name' : 'BIIB',
					'stock':{}
				},
				'tesla' : {
					'keywords' : ['Tesla Inc', 'elon musk', 'TSLA'],
					'name' : 'TSLA',
					'stock':{}
				},
				'amd'  : {
					'keywords' : ['Advanced Micro Devices Inc', 'AMD'],
					'name' : 'AMD',
					'stock':{}
				}
			}

	newsCsv = './data/news.csv'
	links = []
	csvheader = True



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
		parser.add_argument('-l', '--headless', type=self.str2bool, default=True, help='headless mode (1|0)')
		# parser.add_argument('-n', '--nu', type=int, default=0, help='news list start from nu')

		parser.add_argument('-t', '--tiingo', type=str, help='tiingo api key')

		parser.add_argument('-a', '--account', type=str, help='news account')
		parser.add_argument('-p', '--password', type=str, help='news account password')

		parser.add_argument('-f', '--file', type=str, help='parser file')

		parser.add_argument('-r', '--reset', type=self.str2bool, default=False, help='clean csv (1|0)')
		parser.add_argument('-d', '--debug', type=self.str2bool, default=True, help='debug info (1|0)')
		parser.add_argument('-q', '--quit', type=self.str2bool, default=True, help='quit selenium on end (1|0)')

		parser.add_argument('source',
			choices=['wsj', 'usat', 'ft', 'tii', 'usat_arix', 'ft_arix', 'ft_csv', 'usat_csv', 'wsj_arix'],
			help='data source'
			)

		args = parser.parse_args(namespace=self)

		if "_" in self.source:
			to = self.source.index("_")
			self.fnlist = "./data/news_list_" + self.source[0:to]
		else:
			self.fnlist = "./data/news_list_" + self.source
			self.mkdir("./data/" + self.source)

		if args.reset == True:
			try:
				os.remove(self.fnlist+'.bak')
				os.rename(self.fnlist, self.fnlist+'.bak')
			except OSError:
				pass

		return self

	"""docstring for collect"""
	def run(self):
		getattr(self, self.source)()


	def tii(self):
		for t in self.ticker_info:
			self.ticker = self.ticker_info[t]['name']
			self.tii_daily()
			self.tii_news()
			self.tii_eps()

	"""docstring for collect"""
	def tiiapi(self, url, fn):
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
	def tii_daily(self):
		if self.tiingo is None:
			return;

		date = self.collect_start.strftime('%Y-%m-%d')
		ticker = self.ticker_info[self.ticker]['name']
		url = "https://api.tiingo.com/tiingo/daily/" + ticker + "/prices?startDate="+date+"&token=" + self.tiingo
		fn = './data/prices_' + ticker+  '.json'
		self.tiiapi(url, fn)

	"""docstring for collect"""
	def tii_news(self):
		if self.tiingo is None:
			return;
		date = self.collect_start.strftime('%Y-%m-%d')
		ticker = self.ticker_info[self.ticker]['name']
		url = "https://api.tiingo.com/tiingo/news?startDate="+date+"&token=" + self.tiingo + "&tickers=" + ticker
		fn = './data/tii_news ' + ticker + ' .json'
		self.tiiapi(url, fn)

	def tii_eps(self):
		# https://api.tiingo.com/tiingo/fundamentals/<ticker>/statements?startDate=2019-06-30
		if self.tiingo is None:
			return;
		date = self.collect_start.strftime('%Y-%m-%d')
		ticker = self.ticker_info[self.ticker]['name']
		url = "https://api.tiingo.com/tiingo/fundamentals/" + ticker + "/statements?startDate=" + date + '&token=' + self.tiingo
		fn = './data/eps_' + ticker + ".json"
		self.tiiapi(url, fn)

	def stock2Json(self):
		for ticker in self.ticker_info:
			# ticker = self.ticker_info[t]['name']
			fn = './data/prices_' + ticker + '.json'
			try:
				with open(fn, 'r') as stock:
					stockList = json.load(stock)
					for node in stockList:
						date = node['date'][0:10]
						avg = (node['high'] + node['low'])/2
						dateNode = {'d': date, 'h': node['high'], 'l':node['low'], 'a': avg}

						self.ticker_info[ticker]['stock'][date] = dateNode
			except:
				self.log("Error %s : %s" % (sys.exc_info()[0], fn) )

	def find_tag(self, content):
		for ticker in self.ticker_info:
			for kw in self.ticker_info[ticker]['keywords']:
				if content.find(kw) != -1 :
					return ticker
		return False

	"""docstring for collect"""
	def dayMove(self, ticker, dd, n):

		if n > 0 :
			dd = dd + datetime.timedelta(days=n)
		dd1 = datetime.timedelta(days=1)
		while True:
			ds = dd.isoformat()[0:10]
			if ds in self.ticker_info[ticker]['stock']:
				return self.ticker_info[ticker]['stock'][ds]

			# print("%s : %s", dd, n)
			if n == 0:
				dd = dd - dd1
			else:
				dd = dd + dd1

			if dd >= self.collect_end :
				break
		return False


	def tag(self, diff):
		if diff <= 2  and diff >= -2:
			return 'e'

		if diff <= 10  and diff > 2:
			return 'p'

		if diff > 10  :
			return 'pp'

		if diff < -2  and diff >= -10:
			return 'n'

		if diff < -10  :
			return 'nn'


	"""docstring for collect"""
	def toNewsCsv(self, fn, source, title, ticker, ds):
		date = datetime.datetime.strptime(ds, '%Y-%m-%d')

		# usa today arix from 2012-10, fetch data from 20130101 - 20200530
		if date < self.collect_start:
			return False

		st0 = self.dayMove(ticker, date, 0)
		st7 = self.dayMove(ticker, date, 7)
		st30 = self.dayMove(ticker, date, 30)

		if not st0 or not st7 or not st30:
			return False

		d7 = math.floor(((st0['a'] - st7['a'])/st0['a'] )* 100)
		d30 = math.floor(((st0['a'] - st30['a'])/st0['a'] )* 100)

		with open(self.newsCsv, 'a', newline='') as csvfile:
			fieldnames = [ 'source', 'date', 'ticker', 'title', 'content_fp', '0dr', '7dr', '30dr', '7d', '30d', '7dt', '30dt']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			if self.csvheader :
				writer.writeheader()
			writer.writerow({
				'source' : source,
				'date' : ds,
				'ticker' : ticker,
				'title' : title,
				'content_fp' : fn,
				'0dr' : st0,
				'7dr' : st7,
				'30dr' : st30,
				'7d' : d7,
				'30d' : d30,
				'7dt' : self.tag(d7),
				'30dt' : self.tag(d30),
				})
			return True


	def newslist_fetch(self, content_parser):
		with open(self.fnlist , "r") as fo:
			for url in fo:
				url = url.rstrip()
				wait = content_parser(url, False)
				self.wait_between(wait)


	""" ft login , search, & fetch content """
	def ft(self):
		self.ft_login()

		""" After login, Index Go search """
		for ticker in self.ticker_info:
			for kw in self.ticker_info[ticker]['keywords']:
				self.ft_search(ticker, kw, 1)
				self.ft_search(ticker, kw, 2)
			self.links = list(dict.fromkeys(self.links))

			# for log
			for url in self.links:
				with open("./tmp/ft_to_"+ticker , 'a+') as f:
					f.write("%s\n" % url)

		self.ft_content()
		# done

	""" login """
	def ft_login(self):
		if self.account is None:
			print("need account")
			exit()

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
		wait = True
		while wait:
			try:
				#  do check recaptcha completed
				WebDriverWait(self.driver, 120, 1).until(EC.presence_of_element_located((By.ID, "o-header-search-primary")))
				wait = False
			except NoSuchElementException:
				wait = True
				pass
		print("go search... ")

	""" serch """
	def ft_search(self, ticker, keyword, sortBy = 1):

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
				with open(self.fnlist , "a+") as fo:
					writer = csv.writer(fo)
					writer.writerow([ticker, time.text, header.text, url])

				self.wait_between()
			try:
				nextPage = WebDriverWait(self.driver, 20, 1).until(
					EC.presence_of_element_located((By.XPATH, nextPagePath)))
				nextPage.click()

			except:
				nextPage = None
				print("End, Next kw, total %s", i)

				with open("./tmp/ft_"+ keyword.replace(' ', '_')  +"_end.html", 'a') as f:
					f.write(self.driver.page_source)

			finally:
				pass

	""" when search completed, content parser error goes from there"""
	def ft_arix(self):
		with open(self.fnlist) as cf:
			rows = csv.reader(cf)
			for line in rows:
				if len(line) != 4 :
					continue;
				self.links.append(line[3])

		self.links = list(dict.fromkeys(self.links))

		print("total %s", len(self.links))
		self.ft_login()
		self.ft_content()

	"""content page parser"""
	def ft_content(self):
		baseUrl = 'https://www.ft.com'

		i = 0
		goUrl = ''
		for url in self.links:

			try:
				tid = re.search('\/([\w-]+)$', url).group(1)

				fexisted = glob.glob('./data/ft/*'+tid)
				if len(fexisted) != 0:
					continue

				if url[0:4] != "http":
					goUrl = baseUrl + url
				else:
					goUrl = url
			except:
				self.log("Error %s, %s : %s" % (i, sys.exc_info()[0], url) )
				# log url
				with open("./tmp/ft_to", 'a+') as f:
					f.write("%s \n" % url)
				continue

			try:
				self.wait_between(True)
				self.driver.get(goUrl)
				WebDriverWait(self.driver, 10).until(
					EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]'))
					)

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

				with open("./data/ft/"+ date + '_' + tid  , "w+") as fo:
					fo.write(content)

			except:
				self.log("Error %s, %s : %s" % (i, sys.exc_info()[0], url) )

				fn = "./tmp/ft_" + tid + ".html"
				self.log("new html type : %s on %s" % (url, fn))

				# log url
				with open("./tmp/ft_to", 'a+') as f:
					f.write("%s \n" % url)

				# write html content
				with open(fn, 'w') as f:
					f.write(self.driver.page_source)

			finally:
				i = i+1
				pass

	def ft_csv(self):
		self.stock2Json()
		self.links = []

		self.newsCsv = self.fnlist.replace('_list', '') + '.csv'
		with open(self.fnlist) as cf:
			rows = csv.reader(cf)
			for cols in rows:
				# [ticker, time.text, header.text, url]
				if len(cols) < 1:
					continue
				ticker = cols[0]
				ymd = str(parse(cols[1]).date())
				title = cols[2]
				try:
					tid = re.search('\/([\w-]+)$', cols[3]).group(1)
				except:
					continue;

				if tid in self.links :
					continue;

				self.links.append(tid)
				fn = "./data/ft/"+ ymd + '_' + tid

				if self.ticker_info.get(ticker) is None or  os.path.exists(fn) != True:
					continue

				if not self.toNewsCsv(fn, 'ft', title, ticker, ymd):
					continue

				self.csvheader = False



	# https://www.djreprints.com/menu/other-services/
	# http://www.management.ntu.edu.tw/CSIC/DB/Factiva
	# https://developer.dowjones.com/site/global/home/index.gsp
	# https://www.wsj.com/search/term.html?KEYWORDS=BIIB&mod=searchresults_viewallresults
	# OR https://www.wsj.com/market-data/quotes/TSLA
	#
	# https://www.wsj.com/news/archive/2020/08/18


	def wsj(self):

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


	def wsj_arix(self):
		self.source = 'wsj'
		self.newsCsv = self.fnlist.replace('_list', '') + '.csv'
		self.wsj_login()
		self.newslist_fetch(self.wsj_content)

	def wsj_login(self):
		if self.account is None:
			print("need account")
			exit()

		if not self.driver:
			self.setUp()

		loginUrl = 'https://www.wsj.com/'
		self.driver.get(loginUrl)
		login = WebDriverWait(self.driver, 20).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, "header a[href*=accounts]")) #sign-in
		)
		login.click()

		login = WebDriverWait(self.driver, 60).until(
		EC.presence_of_element_located((By.XPATH ,
			'//*[@id="username"]')) #sign-in
		)
		self.key_in(login, self.account)

		pw = self.driver.find_element_by_xpath('//*[@id="password"]')
		self.key_in(pw, self.password)

		self.driver.find_element_by_xpath('//*[@id="basic-login"]/div[1]/form/div/div[6]/div[1]/button').click()

		print("google recaptcha wait... ...")
		wait = True
		while wait:
			try:
				#  do check recaptcha completed
				WebDriverWait(self.driver, 120, 1).until(
					EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[1]/header/nav'))
					)
				wait = False
			except NoSuchElementException:
				wait = True
				pass
		print("go search... ")


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


	def wsj_content(self, link, csv):
		try:
			tid = re.search('-(\d+)$', link).group(1)
			if os.path.exists('./data/wsj/'+tid):
				return False
		except:
			self.log("Error %s, %s : %s" % (sys.exc_info()[0], link))
			# log url
			with open("./tmp/wsj_to", 'a+') as f:
				f.write("%s \n" % link)
			return False

		try:
			self.driver.get(link)
			WebDriverWait(self.driver, 10).until(
				EC.presence_of_element_located((By.XPATH, '//*[@id="main"]'))
				)

			soup = BeautifulSoup(self.driver.page_source, 'html.parser')

			titleDoms = soup.find("h1", class_="wsj-article-headline")
			# artistDoms = soup.select("article div.author-container")
			ts = soup.find("time", class_="timestamp")
			ts = ts.text.replace('Updated', '')
			dt = parse(ts).date()

			title = titleDoms.text
			contentDoms = soup.select("article div.article-content p")
			ct = ''
			for p in contentDoms:
				if p.text.find('Copyright') != -1 or p.text.find('@wsj.com') != -1 :
					continue;
				ct = ct + " \n " + p.text

			fn = './data/wsj/' + tid
			ticker = self.find_tag(ct)
			if ticker != False:
				self.toNewsCsv(fn, self.source, title, ticker, str(dt))

			with open(fn , "w+") as fo:
				fo.write(ct)

		except:
			self.log("Error %s : %s" % (sys.exc_info()[0], link) )

			fn = "./tmp/wsj_" + tid + ".html"
			self.log("new html type : %s on %s" % (link, fn))

			# log url
			with open("./tmp/wsj_to", 'a+') as f:
				f.write("%s \n" % link)

			# write html content
			with open(fn, 'w') as f:
				f.write(self.driver.page_source)

		finally:
			pass

		return True

	def usat_csv(self):
		self.stock2Json()
		self.source = 'usat'
		self.newsCsv = self.fnlist.replace('_list', '') + '.csv'

		folder = './data/usat'
		fnlist = []
		for fn in os.listdir(folder):
			with open(folder + '/' + fn, 'r', encoding='utf-8') as ff :
				content = ff.read()
				ticker = self.find_tag(content)
				lines = content.splitlines(True)
				title = lines[0].strip("\n ")
				date = fn[0:10]
				if ticker != False:
					# print('find fn %s title %s, ymd %s, ticker %s' % (folder + '/' + fn, title, date , ticker))
					self.toNewsCsv(folder + '/' + fn, self.source, title, ticker, date)
					self.csvheader = False


	"""docstring for collect"""
	def usat(self):
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

	""" usa today : fetch from archive, collect all financial news """
	def usat_arix(self):
		if os.path.exists(self.fnlist):
			self.newslist_fetch(self.ust_content)
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
			fn = "./data/usat/"+ date + '_' + tid
			if date:

				with open(fn  , "a") as fo:
					fo.write(content)
			else:
				self.log("Error date is False : %s" % (link) )


			ticker = self.find_tag(content)
			if ticker != False:
				self.toNewsCsv(fn, self.source, ticker, date)

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
