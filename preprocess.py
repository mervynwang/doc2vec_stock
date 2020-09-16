# coding: utf-8
import sys, json, os, pickle


import argparse, gensim, nltk
import numpy as np

#from gensim.models.doc2vec import Doc2Vec, TaggedDocument
# from nltk.tokenize import word_tokenize


# import spacy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud



class preProcess(object):

    processor = ''
    path = ''
    model = ''
    tagged_data = []
    fnlist = []
    stopwords = None


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

        parser.add_argument('-e', '--height', default=400, type=int,
            help='wordcloud image height')

        parser.add_argument('-w', '--width', default=800, type=int,
            help='wordcloud image width')

        parser.add_argument('-t', '--stop', nargs='+',
            help='stop words ')

        parser.add_argument('processor',
            choices=['word2vec', 'doc2vec', 'bow', 'wordcloud', 'load'],
            help='main function')

        args = parser.parse_args(namespace=self)


        self.processor = self.processor.lower()
        for i in range(len(self.path)):
            self.path[i] = os.path.realpath(self.path[i])
            if not os.path.exists(self.path[i]):
                print("Directory not existed %s " % self.path[i])
                exit()

        self.stopwords = set(nltk.corpus.stopwords.words('english'))

        if self.stop is None :
            self.stop = []

        self.stop = self.stop + ['!',',','.','?','-s','-ly','</s>','s',
            '%', '$', "'", '`', '@', "''", 'us', 'year',
            'new', 'today', 'usa', 'say']

        for w in self.stop:
            self.stopwords.add(w)

        return self


    """docstring for collect"""
    def run(self):
        getattr(self, self.processor)()

        # if self.processor == "bow":
        #     self.prepare_bow().train_bow()

        if self.processor == "load":
            vec = np.load(self.path)
            print(vec)
            # model = gensim.models.doc2vec.Doc2Vec.load(self.path)
            # vector = model.docvecs['0000_40']
            # print(type(vector))


    def open_folder(self):
        for folder in self.path:
            for fn in os.listdir(folder):
                self.fnlist.append(folder + '/' + fn)


    def wordcloud(self):
        self.open_folder()
        text = ''
        for fn in self.fnlist:
            with open(fn, 'r', encoding='utf-8') as news:
                words = nltk.tokenize.word_tokenize(news.read())
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


    def dow(self):
        pass

    # https://colab.research.google.com/drive/14HcWVXEQ8OwUuNLcYWg0ZDT1RtpMVl7b#forceEdit=true&sandboxMode=true&scrollTo=8iElYoMOhSIy
    def prepare_bow(self):
        j = 0
        for news_fn in self.fnlist:
            with open(news_fn, 'r') as f:
                for i, line in enumerate(f.read().splitlines(True)):
                    line = line.strip("\n ")
                    if len(line) == 0:
                        continue

                    words = nltk.tokenize.word_tokenize(line.lower())
                    filtered_words = [word for word in words if word not in self.stopwords]
                    line = ' '.join(filtered_words)
                    self.tagged_data.append(line)

            # print(news_fn)
            # j = j + 1
            # if j >= 10 :
            #     break;

        return self

    def train_bow(self):
        vectorizer = CountVectorizer() # 初始化這個詞袋vectorizer
        word_vectors = vectorizer.fit_transform(self.tagged_data)

        # print('Features:', vectorizer.get_feature_names())
        # print('Values: \n', word_vectors.toarray())
        with open(self.model + '_bow.pkl', 'wb') as handle:
            pickle.dump(word_vectors, handle) #, protocol=pickle.HIGHEST_PROTOCOL


    def word2vec(self):
        self.open_folder()
        self.prepare_word_data().train_word2vec()

    def prepare_word_data(self):
        # https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf
        for news_fn in self.fnlist:
            with open(news_fn, 'r') as f:
                for i, line in enumerate(f.read().splitlines(True)):
                    words = nltk.tokenize.word_tokenize(line.strip().lower())
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
                for i, line in enumerate(f.read().splitlines(True)):
                    words = nltk.tokenize.word_tokenize(line.strip().lower())
                    # empty line
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
    model.setArgv().run()

