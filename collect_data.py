#!/usr/bin/python3

import requests
import argparse
import urllib.parse

from fake_useragent import UserAgent
from googlesearch import search


# from bs4 import BeautifulSoup



# ua = UserAgent()
#
# ua.firefox
# ua.chrome



class collect(object):
	"""docstring for collect"""
	def __init__(self):
		super(collect, self).__init__()
		self.site = {
			"ust" : "usatoday.com",
			"wsj" : "wsj.com",
			"ft" : "ft.com",
			}

	def setArgv(self):
		parser = argparse.ArgumentParser(description='input stock name, apiKey(tiingo & google search)')
		parser.add_argument('-s', '--ticker', type=str, help='stock name')
		parser.add_argument('-t', '--tiingo', type=str, help='tiingo api key')
		parser.add_argument('-g', '--google', type=str, help='google search api key')
		parser.add_argument('-d', '--debug', type=self.str2bool, default=False, help='debug info')
		args = parser.parse_args()
		self.ticker = args.ticker
		self.tiingo = args.tiingo
		self.google = args.google
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

	def gapi(self, site, **kwargs):
		if self.google == None :
			return
		try:
			ff = self.site[site]
		except KeyError:
			print('site not exist ' + site)
			return

		cse_id = ""

		key = self.google
		query_service = build("customsearch", "v1", developerKey=key)
		query_results = query_service.cse().list(
			q=self.ticker, cx=cse_id,
			# siteSearch=self.site[site], siteSearchFilter="i",
			lr="lang_en"
			).execute()
		print(query_results)
		pass


	def ft(self):
		pass

	def login(self):
		ua = UserAgent()
		headers = {"User-Agent":ua.random}
		seesion = requests.session()

		post_url = "http://www.renren.com/PLogin.do"    # form表單裡面直接找到的
		post_data = {"email":"xxxx", "password":"xxxx"}
		seesion.post(post_url, headers = headers, data = post_data)

		url = "再次請求登陸的url"
		response = seesion.get(url, headers = headers)
		with open("renren3.html", "w", encoding="utf-8") as f:
		f.write(response.content.decode())

if __name__ == '__main__':
	co = collect()
	argv = co.setArgv()
	print(argv)
	# co.daily()
	# co.news()
	co.goo_search("ft")
	# co.gapi("ft", num = 10)

