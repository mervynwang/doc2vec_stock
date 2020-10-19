# coding: utf-8
import sys, json, os, time, pickle, csv, random


import argparse, gensim
import numpy as np
import sklearn as sk
import pandas as pd

# svm bayes
from sklearn.naive_bayes import MultinomialNB
# from sklearn.model_selection import train_test_split
from sklearn.model_selection import TimeSeriesSplit
from sklearn import svm

class train(object):

	rows = None
	total = 0
	output = 5

	# timer
	start_ts = 0.0

	def __init__(self):
		self.start_ts = time.time()

	def __del__(self):
		print('cost %.3f seconds' %(time.time() - self.start_ts))

	def setArgv(self):
		parser = argparse.ArgumentParser(description='train model')

		parser.add_argument('-c', '--csv', type=str, nargs='+', help='csv e.g. -p csv1 csv2  ...')
		parser.add_argument('-t', '--use-title', type=self.str2bool, default=False, help='use title')
		parser.add_argument('-d', '--predict', type=str, choices=['1', '7', '30'], help='predict (1,7,30) day')
		parser.add_argument('-s', '--save', type=str, help='save model to ')

		parser.add_argument('-e', '--epoch', type=int, help='epoch')

		parser.add_argument('-e', '--echo', type=self.str2bool, default=False help='print first')

		parser.add_argument('processor',
			choices=['rand', 'bayes', 'svm'],
			help='main function')

		args = parser.parse_args(namespace=self)
		self.processor = self.processor.lower()

		if self.echo :
			print("\n=====\n")
			print("Run model %s : predict %s day :" % (self.processor, self.predict))

		getattr(self, self.processor)()



	def csv_merge(self):
		li = []
		for csvfn in self.csv:
			df = pd.read_csv(csvfn, index_col=None, header=0)
			df = df.iloc[1:] # remove head
			li.append(df)
		frame = pd.concat(li, axis=0, ignore_index=True)
		li = None

		start_date = '2013-01-01'
		end_date = '2020-06-30'

		pd = frame[self.cols]
		pd.set_index('date')
		pd['date'] = pd.to_datetime(pd['date'])
		mask = (self.rows['date'] > start_date) & (self.rows['date'] <= end_date)
		self.rows = self.rows.loc[mask]
		if self.use-title:
			# self.rows = self.rows.loc[:, 'C':'E']
		else:


		self.rows.set_index('date')
		self.rows['date'] = pd.to_datetime(self.rows['date'])

		mask = (self.rows['date'] > start_date) & (self.rows['date'] <= end_date)
		self.rows = self.rows.loc[mask]
		self.rows.sort_values(by='date', inplace=True, ascending=True)
		self.total = len(self.rows)

	def fetch(self, step):
		if ( step - 1 ) <= 0 :
			step = 1

		sep = round(self.total / self.epoch)
		verify_len = round(sep/4)

		start = (step - 1) * sep
		end = step * sep

		return (self.rows[start:end]), (self.rows[end:end+verify_len])



	def rand(self):
		with open(self.tag, 'rb') as tfn:
			tag = pickle.load(tfn)

		with open(self.bow, 'rb') as bfn:
			X = pickle.load(bfn)

		X_train, X_test, y_train, y_test = train_test_split(X, tag, test_size=0.3)

		y_result = []
		classtype = ['o', 'co', 'n', 'cp', 'p']
		for i in range(len(y_test)):
			y_result.append(random.choice(classtype))

		asc = sk.metrics.accuracy_score(y_test, y_result)

		# print("rand total is %s error number: %s " % (len(y_test), (y_test != y_result).sum()))
		print("rand accuracy_score: %s " % asc)

	def bayes(self):
		with open(self.tag, 'rb') as tfn:
			tag = pickle.load(tfn)

		with open(self.bow, 'rb') as bfn:
			X = pickle.load(bfn)

			# StratifiedKFold
			# KFold
		X_train, X_test, y_train, y_test = train_test_split(X, tag, test_size=0.3)

		bayes = MultinomialNB()
		bayes.fit(X_train, y_train)
		y_result = bayes.predict(X_test)

		asc = sk.metrics.accuracy_score(y_test, y_result)
		# rsc = sklearn.metrics.recall_score(y_test, y_result, average='samples')

		# print("y_result : %s " % y_result)
		# print("y_test : %s "% y_test)
		print("bayes total is %s error number: %s " % (len(y_test), (y_test != y_result).sum()))
		print("bayes accuracy_score: %s " % asc)
		# print("bayes recall_score: %s " % rsc)

	def svm(self):
		with open(self.tag, 'rb') as tfn:
			tag = pickle.load(tfn)

		with open(self.bow, 'rb') as bfn:
			X = pickle.load(bfn)

		X_train, X_test, y_train, y_test = train_test_split(X, tag, test_size=0.3)

		SVM = svm.SVC(C=1.0, kernel='linear', degree=5, gamma='auto')
		SVM.fit(X_train, y_train)
		y_result = SVM.predict(X_test)

		asc = sk.metrics.accuracy_score(y_test, y_result)
		# rsc = sklearn.metrics.recall_score(y_test, y_result, average='samples')

		# print("y_result : %s " % y_result)
		# print("y_test : %s "% y_test)
		print("SVM total is %s error number: %s " % (len(y_test), (y_test != y_result).sum()))
		print("SVM accuracy_score: %s " % asc)
		# print("bayes recall_score: %s " % rsc)


	# http://nadbordrozd.github.io/blog/2016/05/20/text-classification-with-word2vec/
	def w2v_nn(self):
		pass



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


if __name__ == '__main__':
	model = train()
	model.setArgv()