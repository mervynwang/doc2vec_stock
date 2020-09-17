# coding: utf-8
import sys, json, os, time, pickle, csv, random


import argparse, gensim
import numpy as np
import sklearn as sk
import pandas as pd

# svm bayes
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn import svm

class train(object):

	processor = ''
	model = ''
	tag = ''
	start_ts = 0.0

	def __init__(self):
		self.start_ts = time.time()

	def __del__(self):
		print('cost %.3f seconds' %(time.time() - self.start_ts))

	def setArgv(self):
		parser = argparse.ArgumentParser(description='train model')

		parser.add_argument('-s', '--save', type=str, help='model save to ')
		parser.add_argument('-t', '--tag', type=str, help='tag pkl')
		parser.add_argument('-b', '--bow', type=str, help='bow pkl')
		parser.add_argument('-e', '--echo', type=str, help='print fisrt')


		parser.add_argument('processor',
			choices=['rand', 'bayes', 'svm'],
			help='main function')

		args = parser.parse_args(namespace=self)
		self.processor = self.processor.lower()

		if self.echo :
			print("\n=====\n")
			print("Run %s, %s :" % (self.processor, self.echo))
			self.echo = None

		getattr(self, self.processor)()

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

		SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
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