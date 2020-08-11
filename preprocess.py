# coding: utf-8
import sys
import json

import argparse

from gensim.models import doc2vec
from collections import namedtuple




# Preprocess
docs = []
analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')
for index, text in enumerate(raw_doc):
    words = text.split()
    docs.append(analyzedDocument(words, [index]))


# Train
model = doc2vec.Doc2Vec(docs, size=300, window=300, min_count=1, workers=4, dm=1)


# Save
model.save('doc2vec.model')


# Load
model = doc2vec.Doc2Vec.load('doc2vec.model')
print(model.docvecs[1].shape)