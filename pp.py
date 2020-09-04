# coding: utf-8
import sys, json, os

import argparse, gensim, nltk
import numpy as np




fn = './data/usat3/2012-12-31_1801581'

data = []
with open(fn, 'r') as f:
	lines = f.read().splitlines(True)
	for i, ln in enumerate(lines):
		words = nltk.tokenize.word_tokenize(ln.strip().lower())
		data.append(gensim.models.doc2vec.TaggedDocument(words=words, tags=['1801581_'+ str(i)] ))


print(data)

max_epochs=15
vec_size=200
alpha=0.025

model = gensim.models.doc2vec.Doc2Vec(vector_size=vec_size, alpha=alpha, min_alpha=0.025, min_count=5,
                dm=1, workers=30)

model.build_vocab(data)


for epoch in range(max_epochs):
    print('iteration {0}'.format(epoch))
    model.train(data,
                total_examples=model.corpus_count,
                epochs=model.iter)
    # decrease learning rate
    model.alpha -= 0.0002
    # and reinitialize it
    model.min_alpha = model.alpha

model.save('./code_test')
print("Model saved")
