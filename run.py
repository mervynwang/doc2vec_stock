# coding: UTF-8
import time, os

import torch, gensim
import numpy as np
import torch.nn as nn
from train_eval import train, init_network
from importlib import import_module
import argparse
from utils import build_dataset, build_iterator, get_time_dif

parser = argparse.ArgumentParser(description='Stock News Text Classification')

parser.add_argument('-d', '--dataset', type=str, required=True,  help='Dataset Name')
parser.add_argument('--model', type=str, required=True, help='choose a model: TextCNN, TextRNN, FastText, TextRCNN, TextRNN_Att, DPCNN, Transformer')

parser.add_argument('-c', '--csv', nargs='+',  help='-c  csv1 csv2 ...')
parser.add_argument('-p', '--predict', default=7, type=int, choices=[1, 7, 30], help='1 | 7 | 30')
parser.add_argument('-t', '--use_title', default=0, type=int, help='use title to train')
parser.add_argument('-a', '--pad_size', default=32, type=int, help='pad_size')
parser.add_argument('-m', '--min_freq', default=5, type=int, help='min_freq')
parser.add_argument('-v', '--vocab', default='', type=str, help='vocab pkl')
parser.add_argument('-e', '--embedding', default='', type=str, help='random or pre_trained')
parser.add_argument('-n', '--emb_type', default=1, choices=[1, 2, 3, 4], type=int, help='1:genism.word2vec, 2:genism.doc2vec, 3:npy 4: random')
parser.add_argument('-b', '--batch_size', default=128, type=int, help='batch_size, note batch_size too small DPCNN cant work ')
parser.add_argument('--ticker', type=str, default='', choices=['google','tesla', 'amd', 'biogen'], help='ticker')

args = parser.parse_args()


if __name__ == '__main__':
    dataset = './log/' + args.dataset

    if os.path.isdir(dataset) == False:
        os.makedirs(dataset, exist_ok=True)

    save_path =  dataset + '/saved_dict/'
    if os.path.isdir(save_path ) == False:
        os.makedirs(save_path, exist_ok=True)

    model_name = args.model  # 'TextRCNN'  # TextCNN, TextRNN, FastText, TextRCNN, TextRNN_Att, DPCNN, Transformer

    x = import_module('models.' + model_name)
    config = x.Config(dataset)

    embed_path = './vecs/' + args.dataset + '_'
    if args.emb_type == 1 :
        embed_path += 'word2vec'
        config.args += "_w2v"

        premodel = gensim.models.Word2Vec.load(embed_path if args.embedding == '' else args.embedding)
        config.embedding_pretrained = torch.FloatTensor(premodel.wv.vectors)

    elif args.emb_type == 2 :
        embed_path += 'doc2vec'
        config.args += "_d2v"

        premodel = gensim.models.Doc2Vec.load(embed_path if args.embedding == '' else args.embedding)
        config.embedding_pretrained = torch.FloatTensor(premodel.wv.vectors)

    elif args.emb_type == 3 :
        config.embedding_pretrained =  self.embedding_pretrained = torch.tensor(
            np.load(args.embedding)["embeddings"].astype('float32'))
        config.args += "_pte"

    else:
        config.embedding_pretrained =  None
        config.args += "_rrr"


    if args.use_title == 1:
        config.args += "_t"
    else:
        config.args += "_a"

    config.embed = config.embedding_pretrained.size(1)\
        if config.embedding_pretrained is not None else 300           # 字向量维度

    if args.csv == None :
        config.csv = ['./data/news_' + args.dataset + '.csv']
    else :
        config.csv = args.csv

    config.dataset = args.dataset
    config.predict = args.predict

    config.use_title = args.use_title
    config.pad_size = args.pad_size
    config.min_freq = args.min_freq
    config.rebuild = False
    config.show = False

    config.args += "_" + str(args.predict)
    config.args += "_ps" + str(args.pad_size)
    config.args += "_mf" + str(args.min_freq)
    config.args += "_b"  + str(args.batch_size)
    config.save_path = config.save_path.replace('.c', config.args +'.c')


    # np.random.seed(1)
    # torch.manual_seed(1)
    # torch.cuda.manual_seed_all(1)
    # torch.backends.cudnn.deterministic = True  # 保证每次结果一样

    start_time = time.time()
    print("Loading data...")
    vocab, train_data, test_2020_data, test_data = build_dataset(config, args.ticker)

    print("train set %d, 2020 set %d, test set:%d" %(len(train_data), len(test_2020_data), len(test_data)))

    train_iter = build_iterator(train_data, config)
    test_2020_iter = build_iterator(test_2020_data, config)
    test_iter = build_iterator(test_data, config)
    time_dif = get_time_dif(start_time)
    print("Time usage:", time_dif)

    # train
    config.n_vocab = len(vocab)
    model = x.Model(config).to(config.device)
    if model_name != 'Transformer':
        init_network(model)
    print(model.parameters)
    train(config, model, train_iter, test_iter, test_2020_iter)

    time_dif = get_time_dif(start_time)
    print("Total Time usage:", time_dif)