# coding: UTF-8
import time, os
import torch
import numpy as np
from train_eval import train, init_network
from importlib import import_module
import argparse

parser = argparse.ArgumentParser(description='Chinese Text Classification')

parser.add_argument('-d', '--dataset', type=str, required=True,  help='Dataset Name')
parser.add_argument('-c', '--csv', nargs='+', required=True,
                        help='-c  csv1 csv2 ...')
parser.add_argument('-p', '--predict', default=7, type=int, choices=['1', '7', '30'], help='1 | 7 | 30')
parser.add_argument('-t', '--use_title', default=1, type=int, help='use title to train')
parser.add_argument('--model', type=str, required=True, help='choose a model: TextCNN, TextRNN, FastText, TextRCNN, TextRNN_Att, DPCNN, Transformer')
parser.add_argument('--embedding', default='pre_trained', type=str, help='random or pre_trained')
args = parser.parse_args()


if __name__ == '__main__':
    dataset = 'log/' + args.dataset

    if os.path.isdir(dataset) == False:
        os.makedirs(dataset, exist_ok=True)

    embedding = 'random'
    if args.embedding == 'random':
        embedding = 'random'

    model_name = args.model  # 'TextRCNN'  # TextCNN, TextRNN, FastText, TextRCNN, TextRNN_Att, DPCNN, Transformer
    if model_name == 'FastText':
        from utils_fasttext import build_dataset, build_iterator, get_time_dif
        embedding = 'random'
    else:
        from utils import build_dataset, build_iterator, get_time_dif

    x = import_module('models.' + model_name)
    config = x.Config(dataset, embedding)
    config.csv = args.csv
    config.predict = args.predict
    config.use_title = args.use_title

    np.random.seed(1)
    torch.manual_seed(1)
    torch.cuda.manual_seed_all(1)
    torch.backends.cudnn.deterministic = True  # 保证每次结果一样

    start_time = time.time()
    print("Loading data...")
    vocab, train_data, dev_data, test_data = build_dataset(config)
    # train_iter = build_iterator(train_data, config)
    # dev_iter = build_iterator(dev_data, config)
    # test_iter = build_iterator(test_data, config)
    # time_dif = get_time_dif(start_time)
    # print("Time usage:", time_dif)

    # # train
    # config.n_vocab = len(vocab)
    # model = x.Model(config).to(config.device)
    # if model_name != 'Transformer':
    #     init_network(model)
    # print(model.parameters)
    # train(config, model, train_iter, dev_iter, test_iter)
