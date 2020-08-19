#!/usr/bin/python3


import sys, os, re, csv, hashlib, datetime

# from datetime import datetime
from time import sleep, time
from random import uniform, randint


import requests
import argparse

from fake_useragent import UserAgent
from googlesearch import search

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

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
					'keywords' : ['GOOGL', 'Alphabet'],
					'name' : 'GOOGL'
				},
				'biogen' : {
					'keywords' : ['Biogen', 'BIIB'],
					'name' : 'BIIB'
				},
				'tesla' : {
					'keywords' : ['elon musk', 'TSLA', 'tesla'],
					'name' : 'TSLA'
				},
				'amd'  : {
					'keywords' : ['Advanced Micro Devices', 'AMD'],
					'name' : 'AMD'
				}
			}

	newsCsv = './data/news.csv'



	"""docstring for collect"""
	def __init__(self):
		super(collect, self).__init__()
		ua = UserAgent()
		self.headers = {'user-agent': ua.chrome}
		self.mkdir("./data")
		self.mkdir("./tmp")


	def __del__(self):
		if(self.driver is not None):
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

		parser.add_argument('source', help='wsj|usat|ft|tii')

		args = parser.parse_args(namespace=self)

		self.fnlist = "./data/" + self.source + "/news_list"
		self.mkdir("./data/" + self.source)

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
			self.ft()

		if self.source == "usatf":
			print(self.source)
			self.ust_content(self.file, False)

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
				url = url.rstrip()
				if self.nu >= i:
					continue

				self.log(str(i) + "  " + url);
				content_parser(url, False)
				self.wait_between()

	"""docstring for collect"""
	def ft(self, target):
		self.setUp()
		driver = self.driver

		driver.get('https://www.ft.com')

		login = WebDriverWait(driver, 20).until(
		EC.presence_of_element_located((By.XPATH ,
			"/html/body/div/div[1]/header[1]/nav[2]/div/ul[2]/li[1]/a")) #sign-in
		)
		self.moveWait(login)
		login.click()

		WebDriverWait(driver, 20).until(
				EC.presence_of_element_located((By.ID ,"enter-email"))
				)

		# #account
		# inputs = driver.find_element_by_xpath('//*[@id="enter-email"]')
		# self.key_in(inputs, self.account)
		# self.moveWait(inputs)
		# self.wait_between()
		# driver.find_element_by_xpath('//*[@id="enter-email-next"]').click()


		# #password
		# self.wait_between()
		# inputs = WebDriverWait(driver, 20).until(
		# 		EC.presence_of_element_located((By.ID ,"enter-password"))
		# 		)

		# self.moveWait(inputs)
		# self.key_in(inputs, self.password)
		# self.moveWait(inputs)
		# driver.find_element_by_xpath('//*[@id="sign-in-button"]').click()



		WebDriverWait(driver, 20, 6).until(EC.presence_of_element_located((By.ID, "o-header-search-primary")))
		driver.find_element_by_xpath('//*[@id="site-navigation"]/div[1]/div/div/div[1]/a[2]').click()
		inputs = driver.find_element_by_xpath('//*[@id="o-header-search-term-primary"]')
		inputs.send_keys(target)

		WebDriverWait(driver, 40, 6).until(EC.presence_of_element_located((By.XPATH, "o-header-search-primary")))
		driver.find_element_by_xpath('//*[@id="o-header-search-primary"]/div/form/button[1]').click()

		# soup = BeautifulSoup(driver.page_source, 'html.parser')
		# # soup.find_all("")
		# content = soup.body.get_text()
		# print(content)

		# ## o-teaser__content > o-teaser__heading > a
		# ## o-teaser__content > o-teaser__timestamp > time

		# NEXT_Page XPTH /html/body/div[1]/div[2]/div/div/div/main/div/div[4]/div/a[2]

		# header   : .topper__content h1.topper__headline > span
		# subtitle : .topper__content .topper__standfirst

		# time     : #site-content article-info article-info__timestamp o-date
		# content  : #site-content article__content-body


		pass

	"""docstring for collect"""
	def fta(self):
		# https://www.gale.com/intl/c/financial-times-historical-archive
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
				tid = ""
			r = requests.get(link, headers=self.headers)
			if r.status_code != requests.codes.ok:
				self.log("Error On %s : return %s" % link, r.status_code)
			text = r.text

		else:
			text = open(link)

		try:
			soup = BeautifulSoup(text, "html.parser")

			dtD = soup.select('article div.gnt_ar_dt')
			if not dtD:
				dtD = soup.select('article span.asset-metabar-time')
				dtD = dtD[0].text
				ymd = re.search('(\d+:\d+) (a\.m\.|p\.m\.) \w+ (\w+\ \d+, \d+)', dtD).group(3)
				dt = datetime.datetime.strptime(ymd, '%B %d, %Y').isoformat()
			else :
				dtD = dtD[0]['aria-label']
				ymd = re.search('(\d+:\d+) (a\.m\.|p\.m\.) \w+ (\w+\.? \d+, \d+)', dtD).group(3)
				dt = datetime.datetime.strptime(ymd, '%b. %d, %Y').isoformat()

			artistD = soup.select('article div.gnt_ar_by')
			if not artistD:
				artistD = soup.select('article div.asset-metabar span.asset-metabar-author')

			artist = artistD[0].text

			contentD = soup.select('article div.gnt_ar_b')
			if not contentD:
				contentD = soup.select('article p.p-text')

			content = contentD[0].text

			if csv == True:
				self.toNewsCsv(
					link,
					'usatoday',
					{"date" : dt, "artist" : artist, "content": content}
					)
			else:
				with open("./data/usat/"+ tid + "-"+ title , "a") as fo:
					fo.write(content)
		except:
			if self.file :
				pass

			print("timeout : " + link)
			with open("./tmp/usat_to", 'a') as f:
				f.write("%s" % link)

			with open("./tmp/usat_" +title + "__"+ tid + ".html", 'a') as f:
				f.write(r.text)




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
	def wait_between(self):
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
