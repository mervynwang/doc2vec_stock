# coding: utf-8
import sys, json, os

import argparse, gensim, nltk
import numpy as np

#from gensim.models.doc2vec import Doc2Vec, TaggedDocument
# from nltk.tokenize import word_tokenize




class preProcess(object):

    """
    Class to create a doc2vec model
    """

    def __init__(self):

        self.path = ''
        self.model = './data/'
        self.tagged_data = []

    """docstring for collect"""
    def setArgv(self):
        parser = argparse.ArgumentParser(description='preprocess BOW, word2vec, doc2vec')
        parser.add_argument('-b', '--bow', type=self.str2bool, default=False, help='headless mode (1|0)')
        parser.add_argument('-w', '--word', type=self.str2bool, default=False, help='headless mode (1|0)')
        parser.add_argument('-d', '--doc', type=self.str2bool, default=False, help='headless mode (1|0)')

        parser.add_argument('-p', '--path', type=str, default='./data/', help='news folder')
        parser.add_argument('-s', '--save', type=str, default='./data/', help='model save to')
        args = parser.parse_args(namespace=self)

        if not self.path:
            parser.print_help()
            exit()

        self.path = os.path.realpath(self.path)

        # nltk.download('')
        if not os.path.exists(self.path):
            print("Directory not existed %s ", self.path)
            exit()

        return self

    """docstring for collect"""
    def run(self):
        if self.bow:
            pass

        if self.word:
            pass

        if self.doc:
            self.model = "./data/doc2vec"
            self.prepare_data().train_doc2vec()


    def prepare_data(self):
        data = []
        tag = []
        i = 0

        # simple for loops to get all the articles and add them to the data and tag list
        for newspaper in os.listdir(self.path):
            data.append(open(self.path + '/' +newspaper, 'rb').read())
            tag.append(newspaper[0:7])
            i += 1

        # tagging all the articles
        self.tagged_data = [ gensim.models.doc2vec.TaggedDocument(words=nltk.tokenize.word_tokenize(str(_d.lower())), tags=[str(tag[i])]) for i, _d in
                            enumerate(data)]

        # Freeing memory

        data = []
        tag = []

        return self

    def train_doc2vec(self, max_epochs=15, vec_size=200, alpha=0.025):
        """
        Training our doc2vec model. The articles will be vectorized in a 200 dimensions vector space
        :param max_epochs: Sets the number of epochs in our training
        :param vec_size: dimension of the vector space used
        :param alpha: Learning rate used in the gradient descent
        :return:
        """
        model = Doc2Vec(vector_size=vec_size, alpha=alpha, min_alpha=0.025, min_count=5,
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
        print("Model savec")

    def clean_train_model(self):

        """
        Aims at using the model trainned by first deleting the temporary training data. Use it carefully you can lose all the progress made in the training.
        :return:
        """

        model = Doc2Vec.load(self.model_path)
        # Be careful here
        model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)

    def test_doc2vec(self):

        """
        To test the  model
        :return:

        """
        model = Doc2Vec.load(self.model_path)

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

        model = Doc2Vec.load(self.model_path)

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
    model.setArgv().prepare_data()

