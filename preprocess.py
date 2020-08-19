# coding: utf-8
import sys, json, csv



import argparse
import gensim



# Load data
raw_doc = [
    'Today is a nice day',
    'I want to go to play'
]

with open('./data/news.csv', 'r', newline='') as csvfile:
    # fieldnames = ['link', 'date', 'artist', 'content', 'ticker', 'source', '7d', '1m']
    rows = csv.reader(csvfile)
    for i, row in enumerate(rows):
    	if i == 5:
    		raw_doc = row[3]
    		break


# Preprocess


tokens = gensim.utils.simple_preprocess(raw_doc)
train_corpus = list(gensim.models.doc2vec.TaggedDocument(tokens, [1]))
model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count=2, epochs=40)
model.build_vocab(train_corpus)
model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
vector = model.infer_vector(['only', 'you', 'can', 'prevent', 'forest', 'fires'])
print(vector)










# docs = []
# words = raw_doc.split()
# # print(words)

# # docs.append(words, [index])
# # analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')
# # for index, text in enumerate(rows[3]):
# #     words = text.split()
# #     docs.append(words)


# # Train
# model = doc2vec.Doc2Vec(words, size=300, window=300, min_count=1, workers=4, dm=1)

# # print(model)

# # Save
# # model.save('doc2vec.model')


# # Load
# # model = doc2vec.Doc2Vec.load('doc2vec.model')
# # print(model.docvecs[1].shape)