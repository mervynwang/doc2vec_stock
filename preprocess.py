# coding: utf-8
import sys, json, os

import argparse, gensim, nltk
import numpy as np

#from gensim.models.doc2vec import Doc2Vec, TaggedDocument
# from nltk.tokenize import word_tokenize




class preProcess(object):

    processor = ''
    path = ''
    model = ''
    tagged_data = None


    def __init__(self):
        self.tagged_data = []

    """docstring for collect"""
    def setArgv(self):
        parser = argparse.ArgumentParser(description='preprocess BOW, word2vec, doc2vec')

        parser.add_argument('-p', '--path', type=str, help='news folder')
        parser.add_argument('-s', '--model', type=str, default='./data/', help='model save to')

        parser.add_argument('processor', help='bow|word2vec|doc2vec|load')
        args = parser.parse_args(namespace=self)

        if not self.path or not self.processor:
            parser.print_help()
            exit()

        self.processor = self.processor.lower()
        self.path = os.path.realpath(self.path)

        # nltk.download('')
        if not os.path.exists(self.path):
            print("Directory not existed %s ", self.path)
            exit()

        return self

    """docstring for collect"""
    def run(self):
        if self.processor == "bow":
            pass

        if self.processor == "word2vec":
            pass

        if self.processor == "doc2vec":
            self.save = "./data/doc2vec"
            self.prepare_doc_data().train_doc2vec()

        if self.processor == "load":
            vec = np.load(self.path)
            print(vec)


    def prepare_word_data(self):
        data = []
        tag = []

        for newspaper in os.listdir(self.path):
            with open(self.path + '/' +newspaper, 'r') as f:
                for i, line in enumerate(f.read().splitlines(True)):
                    words = nltk.tokenize.word_tokenize(line.strip().lower())
                    self.tagged_data.append(words)

        return self

    def train_word2vec(self, max_epochs=15, vec_size=200, alpha=0.025):

        model = gensim.models.Word2Vec(self.tagged_data, min_count=1)



    def prepare_doc_data(self):
        data = []
        tag = []

        for newspaper in os.listdir(self.path):
            with open(self.path + '/' +newspaper, 'r') as f:
                for i, line in enumerate(f.read().splitlines(True)):
                    words = nltk.tokenize.word_tokenize(line.strip().lower())
                    self.tagged_data.append(gensim.models.doc2vec.TaggedDocument(words=words, tags=[newspaper[0:7] + "_" +  str(i)] ))


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

    def clean_train_model(self):

        model = gensim.models.doc2vec.Doc2Vec.load(self.model)
        # Be careful here
        model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)

    def test_doc2vec(self):

        """
        To test the  model
        :return:

        """
        model = gensim.models.doc2vec.Doc2Vec.load(self.model)

        model.docvecs.doctags

        # test_data = word_tokenize("Odorizzi".lower())
        # test_data2 = word_tokenize("Page".lower())

        # v1 = model.infer_vector(test_data)
        # v2 = model.infer_vector(test_data2)

        # to print the vectorized article using tags
        vector = model.docvecs['0000_40']
        print(type(vector))
        print("Vector of document:", vector)

    def readFile(self):

        """
        To read the files created by doc2vec model
        :return:
        """

        model = gensim.models.doc2vec.Doc2Vec.load(self.model_path)

        print(type(model.docvecs.doctags))

        file = np.load('/Users/rugerypierrick/PycharmProjects/doc2vec/d2v.model.docvecs.vectors_docs.npy')

        fil2 = np.load('/Users/rugerypierrick/PycharmProjects/doc2vec/d2v.model.trainables.syn1neg.npy')

        file3 = np.load('/Users/rugerypierrick/PycharmProjects/doc2vec/d2v.model.wv.vectors.npy')


        print(file3)

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

