# coding: UTF-8
import time, os

import torch, gensim
import numpy as np
import torch.nn as nn
from train_eval import train, init_network
from importlib import import_module
import argparse

parser = argparse.ArgumentParser(description='Chinese Text Classification')

parser.add_argument('-d', '--dataset', type=str, required=True,  help='Dataset Name')
parser.add_argument('-c', '--csv', nargs='+', required=True,
                        help='-c  csv1 csv2 ...')
parser.add_argument('-p', '--predict', default=7, type=int, choices=['1', '7', '30'], help='1 | 7 | 30')
parser.add_argument('-t', '--use_title', default=0, type=int, help='use title to train')
parser.add_argument('-a', '--pad_size', default=32, type=int, help='pad_size')
parser.add_argument('-m', '--min_freq', default=1, type=int, help='min_freq')
parser.add_argument('--model', type=str, required=True, help='choose a model: TextCNN, TextRNN, FastText, TextRCNN, TextRNN_Att, DPCNN, Transformer')
parser.add_argument('--embedding', default='pre_trained', type=str, help='random or pre_trained')
parser.add_argument('-e', '--emb_type', default=1, choices=[1, 2, 3], type=int, help='1:genism.word2vec, 2:genism.doc2vec, 3:npy')
parser.add_argument('-b', '--batch_size', default=0, type=int, help='batch_size')
args = parser.parse_args()


if __name__ == '__main__':
    dataset = 'log/' + args.dataset


    if os.path.isdir(dataset) == False:
        os.makedirs(dataset, exist_ok=True)

    save_path =  dataset + '/saved_dict/'
    if os.path.isdir(save_path ) == False:
        os.makedirs(save_path, exist_ok=True)

    if args.embedding == 'random':
        embedding = 'random'

    model_name = args.model  # 'TextRCNN'  # TextCNN, TextRNN, FastText, TextRCNN, TextRNN_Att, DPCNN, Transformer
    if model_name == 'FastText':
        from utils_fasttext import build_dataset, build_iterator, get_time_dif
        embedding = 'random'
    else:
        from utils import build_dataset, build_iterator, get_time_dif

    x = import_module('models.' + model_name)
    config = x.Config(dataset)

    if args.emb_type == 1 :
        # Load word2vec pre-train model
        premodel = gensim.models.Word2Vec.load(args.embedding)
        config.embedding_pretrained = torch.FloatTensor(premodel.wv.vectors)
        config.save_path = config.save_path.replace('.', '_w2v.')
        config.args += "_w2v"
    elif args.emb_type == 2 :
        premodel = gensim.models.Doc2Vec.load(args.embedding)
        config.embedding_pretrained = torch.FloatTensor(premodel.wv.vectors)
        config.save_path = config.save_path.replace('.', '_d2v.')
        config.args += "_d2v"
    else:
        config.embedding_pretrained = None
        config.args += "_r"

    if args.use_title == 1:
        config.vocab_path = config.vocab_path.replace('.', '_' + str(args.pad_size) + '_title.')
        config.save_path = config.save_path.replace('.', '_t.')
        config.args += "_ti"
    else:
        config.vocab_path = config.vocab_path.replace('.', '_' + str(args.pad_size) + '_fulltext.')
        config.save_path = config.save_path.replace('.', '_f.')
        config.args += "_ft"

    config.embed = config.embedding_pretrained.size(1)\
        if config.embedding_pretrained is not None else 300           # 字向量维度
    config.csv = args.csv
    config.predict = args.predict
    config.use_title = args.use_title
    config.pad_size = args.pad_size
    config.min_freq = args.min_freq
    config.args += "_ps" + str(args.pad_size)
    config.args += "_mf" + str(args.min_freq)

    if args.batch_size > 1 :
        config.batch_size = args.batch_size

    print("vocab: %s"  % config.vocab_path)

    np.random.seed(1)
    torch.manual_seed(1)
    torch.cuda.manual_seed_all(1)
    torch.backends.cudnn.deterministic = True  # 保证每次结果一样

    start_time = time.time()
    print("Loading data...")
    vocab, train_data = build_dataset(config)
    train_iter = build_iterator(train_data, config)
    time_dif = get_time_dif(start_time)
    print("Time usage:", time_dif)

    # train
    config.n_vocab = len(vocab)
    model = x.Model(config).to(config.device)
    if model_name != 'Transformer':
        init_network(model)
    print(model.parameters)
    train(config, model, train_iter)
