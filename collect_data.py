#!/usr/bin/python3


import sys, time

import numpy as np
import scipy.interpolate as si

from datetime import datetime
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
LONG_MAX_RAND = 11.1



class collect(object):

	number = None
	headless = False
	options = None
	profile = None
	capabilities = None

	"""docstring for collect"""
	def __init__(self):
		super(collect, self).__init__()
		self.site = {
			'ust' : 'usatoday.com',
			'wsj' : 'wsj.com',
			'ft' : 'ft.com',
			}

		self.ticker = {
				'google' : {
					'keywords' : ['Alphabet', 'GOOGL'],
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


	def setArgv(self):
		parser = argparse.ArgumentParser(description='input stock name, apiKey(tiingo & google search)')
		parser.add_argument('-s', '--ticker', type=str, help='stock name')
		parser.add_argument('-t', '--tiingo', type=str, help='tiingo api key')
		parser.add_argument('-a', '--account', type=str, help='news account')
		parser.add_argument('-p', '--password', type=str, help='news account password')
		parser.add_argument('-d', '--debug', type=self.str2bool, default=False, help='debug info')
		args = parser.parse_args()
		self.ticker = args.ticker
		self.tiingo = args.tiingo
		self.account = args.account
		self.password = args.password
		self.debug = args.debug
		return args

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

	def tii(self, url, fn):
		if url == None or fn == None:
			return
		headers = {
			'Content-Type': 'application/json'
		}
		requestResponse = requests.get(url, headers=headers)
		with open(fn, "a") as fo:
			fo.write(requestResponse.text)
		return

	def daily(self):
		if self.tiingo == None:
			return;
		url = "https://api.tiingo.com/tiingo/daily/" + self.ticker + "/prices?startDate=2000-01-01&token=" + self.tiingo
		fn = self.ticker+"_prices.json"
		tii(url, fn)

	def tii_news(self):
		if self.tiingo == None:
			return;
		url = "https://api.tiingo.com/tiingo/news?startDate=2000-01-01&token=" + self.tiingo + "&tickers=" + self.ticker
		fn = self.ticker + "_news.json"
		tii(url, fn)

	def goo_search(self, site):
		if self.google == None :
			return
		try:
			ff = self.site[site]
		except KeyError:
			print('site not exist ' + site)
			return
		q = self.ticker + ("" if site == None else "%20+site:%20" + self.site[site])
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

	# Setup options for webdriver
	def setUpOptions(self):
		self.options = webdriver.FirefoxOptions()
		# self.options.add_option('useAutomationExtension', False)
		self.options.headless = self.headless

	# Setup profile with buster captcha solver
	def setUpProfile(self):
		# ua = UserAgent()
		# fua = ua.firefox
		# print(fua)

		self.profile = webdriver.FirefoxProfile()
		self.profile._install_extension("buster_captcha_solver_for_humans-0.7.2-an+fx.xpi", unpack=False)
		self.profile.set_preference("security.fileuri.strict_origin_policy", False)
		# self.profile.set_preference("general.useragent.override", fua)
		self.profile.update_preferences()


	# Enable Marionette, An automation driver for Mozilla's Gecko engine
	def setUpCapabilities(self):
		self.capabilities = webdriver.DesiredCapabilities.FIREFOX
		self.capabilities['marionette'] = True

	# Setup settings
	def setUp(self):
		self.setUpProfile()
		self.setUpOptions()
		self.setUpCapabilities()
		self.driver = webdriver.Firefox(options=self.options, capabilities=self.capabilities, firefox_profile=self.profile, executable_path='./geckodriver')
		self.driver.set_window_size(1024, 768)

	# Simple logging method
	def log(s,t=None):
			now = datetime.now()
			if t == None :
					t = "Main"
			print ("%s :: %s -> %s " % (str(now), t, s))

	# Use time.sleep for waiting and uniform for randomizing
	def wait_between(self, a, b):
		rand=uniform(a, b)
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
		self.wait_between(MIN_RAND, MAX_RAND)


	def key_in(self, controller, keys, min_delay=0.05, max_delay=0.25):
		for key in keys:
			controller.send_keys(key)
			sleep(uniform(min_delay,max_delay))


	def ft(self, target):
		self.setUp()
		driver = self.driver
		number = self.number
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
		# self.wait_between(MIN_RAND, MAX_RAND)
		# driver.find_element_by_xpath('//*[@id="enter-email-next"]').click()


		# #password
		# self.wait_between(LONG_MIN_RAND, LONG_MAX_RAND)
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


	def fta(self):
		# https://www.gale.com/intl/c/financial-times-historical-archive
		pass

	def wsj(self, target):
		# https://www.djreprints.com/menu/other-services/
		# http://www.management.ntu.edu.tw/CSIC/DB/Factiva
		# https://developer.dowjones.com/site/global/home/index.gsp
		# https://www.wsj.com/search/term.html?KEYWORDS=BIIB&mod=searchresults_viewallresults
		return

	def ust(slef, target):
		# https://www.usatoday.com/search/?q=TSLA
		return

if __name__ == '__main__':
	co = collect()
	argv = co.setArgv()
	print(argv)
	# co.daily()
	# co.news()
	# co.gapi("ft", num = 10)

	co.ft('')
