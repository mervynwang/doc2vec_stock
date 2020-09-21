# coding: utf-8
import sys, json, os, pickle, csv, re


import argparse, gensim, nltk
import numpy as np

import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer  # bow
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# svm bayes
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import sklearn




class preProcess(object):

	processor = ''
	path = ''
	model = ''
	tagged_data = []
	tag = []
	fnlist = []
	tagname = ''
	stopwords = None
	cols = [ 'source', 'date', 'ticker',
				'title', 'content_fp', '0dr',
				'1dr', '7dr', '30dr',
				'1d', '7d', '30d',
				'1dt', '7dt', '30dt']


	def __init__(self):
		self.tagged_data = []

	"""docstring for collect"""
	def setArgv(self):
		parser = argparse.ArgumentParser(description='preprocess BOW, word2vec, doc2vec')

		parser.add_argument('-p', '--path',
			nargs='+', required=True,
			help='news folders e.g. -p folder1 folder2 ... ')

		parser.add_argument('-s', '--model', type=str,
			required=True,
			help='model save to')

		parser.add_argument('-a', '--tagname', default='7d', choices=['1', '7', '30'], type=str,
			help='1 | 7 | 30 ')

		parser.add_argument('-r', '--ticker', default='google', choices=['google', 'tesla', 'amd', 'biogen'], type=str,
			help='ticker')

		parser.add_argument('-u', '--useTitle', default=False, type=self.str2bool,
			help='use title to train ')

		parser.add_argument('-i', '--title', type=str, help='wordcloud title')
		parser.add_argument('-e', '--height', default=400, type=int,
			help='wordcloud image height')

		parser.add_argument('-w', '--width', default=800, type=int,
			help='wordcloud image width')

		parser.add_argument('-t', '--stop', nargs='+',
			help='stop words ')

		parser.add_argument('processor',
			choices=['word2vec', 'doc2vec', 'bow', 'wordcloud', 'bar', 'bar_ym'],
			help='main function')

		args = parser.parse_args(namespace=self)


		self.processor = self.processor.lower()
		for i in range(len(self.path)):
			self.path[i] = os.path.realpath(self.path[i])
			if not os.path.exists(self.path[i]):
				print("Directory not existed %s " % self.path[i])
				exit()

		self.stopwords = set(nltk.corpus.stopwords.words('english'))

		if not self.tagname :
			self.tagname = '7'

		if self.stop is None :
			self.stop = []

		self.stop = self.stop + ['!',',','.','?','-s','-ly','</s>','s',
			'%', '$', "'", '`', '@', "''", 'us', 'year', '”', '“'
			'new', 'today', 'usa', 'say']

		for w in self.stop:
			self.stopwords.add(w)

		getattr(self, self.processor)()

	def open_folder(self):
		for folder in self.path:
			if folder.find('.csv') != -1:
				#from csv
				with open(folder) as cf:
					rows = csv.reader(cf)
					for cols in rows:
						if cols[4] == 'content_fp' :
							continue;
						self.fnlist.append(cols[4])
						if self.useTitle:
							self.tagged_data.append(cols[3])

						if self.tagname == '1':
							self.tag.append(cols[12])  # 1dt
						elif self.tagname == '7':
							self.tag.append(cols[13])  # 7dt
						else:
							self.tag.append(cols[14])  # 30dt

			else:
				# folder
				for fn in os.listdir(folder):
					self.fnlist.append(folder + '/' + fn)

	def bar_ym(self):
		li = []

		for csvfn in self.path:
			df = pd.read_csv(csvfn, index_col=None, header=0)
			df = df.iloc[1:]
			li.append(df)

		frame = pd.concat(li, axis=0, ignore_index=True)
		li = None


		df = frame[self.cols]
		fig = plt.figure(figsize=(10,4), dpi=100)

		use_tag = ''
		if self.tagname == '1':
			use_tag = '1dt'
		elif self.tagname == '7':
			use_tag = '7dt'
		else:
			use_tag = '30dt'

		df['month_year'] = pd.to_datetime(df['date']).dt.to_period('M')
		# print(df.head())

		bar = df.groupby(['month_year', use_tag]).size().unstack().rename(columns={
				'n' : 'Neutral',
				'o' : 'Cautious Optimism',
				'co': 'Optimism',
				'cp' : 'Cautious Pessimistic',
				'p': 'Pessimistic'
			}).reindex(columns=['Pessimistic', 'Cautious Pessimistic' , 'Neutral', 'Cautious Optimism', 'Optimism'])

		bar.to_csv(self.model + '_' + use_tag +  '.csv')
		char = bar.plot.bar()
		char.set_xlabel(self.tagname + ' days predict')
		char.tick_params(axis='x', rotation=10, labelbottom=30)
		char.set_title(self.tagname + ' days predict')

		plt.savefig(self.model + '_' + use_tag + '.png')
		# plt.show()

	def bar(self):
		li = []

		for csvfn in self.path:
			df = pd.read_csv(csvfn, index_col=None, header=0)
			df = df.iloc[1:]
			li.append(df)

		frame = pd.concat(li, axis=0, ignore_index=True)
		li = None

		df = frame[self.cols]
		fig = plt.figure(figsize=(20,10))
		# print(df.head())

		use_tag = ''
		if self.tagname == '1':
			use_tag = '1dt'
		elif self.tagname == '7':
			use_tag = '7dt'
		else:
			use_tag = '30dt'

		bar = df.groupby([use_tag, 'ticker']).size().unstack().rename(
			index={
				'n' : 'Neutral',
				'o' : 'Cautious Optimism',
				'co': 'Optimism',
				'cp' : 'Cautious Pessimistic',
				'p': 'Pessimistic'
			}).reindex(['Pessimistic', 'Cautious Pessimistic' , 'Neutral', 'Cautious Optimism', 'Optimism'])

		bar.to_csv(self.model + '_' + use_tag + '.csv')

		char = bar.plot.bar()
		char.set_xlabel(self.tagname + ' days predict')
		char.tick_params(axis='x', rotation=10, labelbottom=30)
		char.set_title(self.tagname + ' days predict')

		plt.savefig(self.model + '_' + use_tag + '.png')
		# plt.show()


	def wordcloud(self):
		self.open_folder()
		text = ''
		for fn in self.fnlist:
			with open(fn, 'r', encoding='utf-8') as news:
				words = nltk.tokenize.word_tokenize(news.read().lower())
				# Remove non-alphabetic tokens, such as punctuation
				words = [word for word in words if word.isalpha()]
				filtered_words = [word for word in words if word not in self.stopwords]
				text = text + ' '.join(filtered_words)
				words = filtered_words = None

		cloud = WordCloud(
			stopwords=self.stopwords,
			max_words=400,
			width=self.width,
			height=self.height
			).generate(text)
		cloud.to_file(self.model)



	def bow(self):
		self.open_folder()
		if self.useTitle:
			self.prepare_bow_title()
		else:
			self.prepare_bow()

		self.train_bow()

	def prepare_bow_title(self):
		for i, title in enumerate(self.tagged_data):
			words = nltk.tokenize.word_tokenize(title.lower())
			# Remove non-alphabetic tokens, such as punctuation
			words = [word for word in words if word.isalpha()]
			filtered_words = [word for word in words if word not in self.stopwords]
			self.tagged_data[i] = ' '.join(filtered_words)
			words = filtered_words = None

		return self

	def prepare_bow(self):
		for news_fn in self.fnlist:
			with open(news_fn, 'r') as f:
				content = f.read()
				words = nltk.tokenize.word_tokenize(content.lower())
				# Remove non-alphabetic tokens, such as punctuation
				words = [word for word in words if word.isalpha()]
				filtered_words = [word for word in words if word not in self.stopwords]
				line = ' '.join(filtered_words)
				self.tagged_data.append(line)
				filtered_words = words = content = line = None

		return self

	def train_bow(self):
		vectorizer = CountVectorizer() # 初始化這個詞袋vectorizer
		word_vectors = vectorizer.fit_transform(self.tagged_data)
		# print('Features:', vectorizer.get_feature_names())
		# print('Values: \n', word_vectors.toarray())

		with open(self.model + '_tag.pkl', 'wb') as handle:
			pickle.dump(self.tag, handle)

		with open(self.model + '.pkl', 'wb') as handle:
			pickle.dump(word_vectors, handle)

		return word_vectors

	def word2vec(self):
		self.open_folder()
		self.prepare_word_data().train_word2vec()

	def prepare_word_data(self):
		# https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf
		for news_fn in self.fnlist:
			with open(news_fn, 'r') as f:
				for i, line in enumerate(f.read().splitlines(True)):
					words = nltk.tokenize.word_tokenize(line.strip().lower())
					# Remove non-alphabetic tokens, such as punctuation
					words = [word for word in words if word.isalpha()]
					filtered_words = [word for word in words if word not in self.stopwords]
					self.tagged_data.append(filtered_words)

		return self

	def train_word2vec(self):

		model = gensim.models.Word2Vec(self.tagged_data, min_count=1)
		model.save(self.model)
		print("Model saved")


	def doc2vec(self):
		self.open_folder()
		self.prepare_doc_data().train_doc2vec()

	def prepare_doc_data(self):

		for news_fn in self.fnlist:
			with open(news_fn, 'r') as f:
				content = f.read().lower()
				content = re.sub(r'([a-zA-Z]{2,})[\.\?\!]\s?', r'\1 \n', content)
				for i, line in enumerate(content.splitlines(True)):
					words = nltk.tokenize.word_tokenize(line.strip())
					if len(words) == 0:
						continue;
					self.tagged_data.append(gensim.models.doc2vec.TaggedDocument(words=words, tags=[news_fn[-7:] + "_" +  str(i)] ))

		return self

	def train_doc2vec(self, max_epochs=15, vec_size=200, alpha=0.025):
		"""
		Training our doc2vec model. The articles will be vectorized in a 200 dimensions vector space
		:param max_epochs: Sets the number of epochs in our training
		:param vec_size: dimension of the vector space used
		:param alpha: Learning rate used in the gradient descent
		:return:
		"""
		model = gensim.models.doc2vec.Doc2Vec(vector_size=vec_size, alpha=alpha, min_alpha=0.025, min_count=5,
						dm=1, workers=30)

		model.build_vocab(self.tagged_data)


		for epoch in range(max_epochs):
			print('iteration {0}'.format(epoch))
			model.train(self.tagged_data,
						total_examples=model.corpus_count,
						epochs=model.iter)
			# decrease learning rate
			model.alpha -= 0.0002
			# and reinitialize it
			model.min_alpha = model.alpha

		model.save(self.model)
		print("Model saved")




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
	model = preProcess()
	model.setArgv()