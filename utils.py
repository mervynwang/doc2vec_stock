# coding: UTF-8
import os
import torch
import numpy as np
import pickle as pkl
from tqdm import tqdm
import time
from datetime import timedelta
import pandas as pd


MAX_VOCAB_SIZE = 10000  # 词表长度限制
UNK, PAD = '<UNK>', '<PAD>'  # 未知字，padding符号

def build_dataset(config, ticker = '',show = False):

    pad_size = config.pad_size
    vocab_dic = {}
    vocab_build = True
    contents = []
    cols = [ 'source', 'date', 'ticker',
                'title', 'content_fp', '0dr',
                '1dr', '7dr', '30dr',
                '1d', '7d', '30d',
                '1dt', '7dt', '30dt']

    start_date = '2013-01-01'
    end_date = '2019-12-30'
    li = []
    tokenizer = lambda x: x.split(' ')
    rows_len = []

    if os.path.exists(config.vocab_path) and show == False:
        vocab_dic = pkl.load(open(config.vocab_path, 'rb'))
        vocab_build = False
        print(f"Vocab size: {len(vocab_dic)}")

    for csvfn in config.csv:
        df = pd.read_csv(csvfn, index_col=None, header=0)
        df = df.iloc[1:]
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)
    li = None

    df = frame[cols]
    df.set_index('date')
    mask = (df['date'] > start_date) & (df['date'] <= end_date)
    df = df.loc[mask]
    if ticker != '':
        df = df[ticker = ticker]

    df.sort_values(by='date', inplace=True, ascending=True)

    use_tag = ''
    if config.predict == 1:
        use_tag = '1dt'
    elif config.predict == 7:
        use_tag = '7dt'
    else:
        use_tag = '30dt'

    df = df.loc[:, ['date', 'title', 'content_fp', use_tag]]
    max_len = 0




    for row in df.itertuples():
        label = row._4
        content = row.title
        if config.use_title == 0 :
            with open(row.content_fp, 'r', encoding='UTF-8') as f:
                content = f.read().lower()
        else:
            content = row.title
        clen = len(content)
        if clen > max_len:
            max_len = clen
        if show == True:
            rows_len.append(clen)

        words_line = []
        token = tokenizer(content)
        seq_len = len(token)

        if vocab_build == False:
            if pad_size:
                if len(token) < pad_size:
                    token.extend([PAD] * (pad_size - len(token)))
                else:
                    token = token[:pad_size]
                    seq_len = pad_size

            for word in token:
                words_line.append(vocab_dic.get(word, vocab_dic.get(UNK)))
            contents.append((words_line, int(label), seq_len)) #, row.date

        else:

            for word in token:
                vocab_dic[word] = vocab_dic.get(word, 0) + 1
            vocab_list = sorted([_ for _ in vocab_dic.items() if _[1] >= config.min_freq], key=lambda x: x[1], reverse=True)[:MAX_VOCAB_SIZE]
            vocab_dic = {word_count[0]: idx for idx, word_count in enumerate(vocab_list)}
            vocab_dic.update({UNK: len(vocab_dic), PAD: len(vocab_dic) + 1})

            if pad_size:
                if len(token) < pad_size:
                    token.extend([PAD] * (pad_size - len(token)))
                else:
                    token = token[:pad_size]
                    seq_len = pad_size

            for word in token:
                contents.append((token, int(label), seq_len)) #, row.date

            pkl.dump(vocab_dic, open(config.vocab_path, 'wb'))

            for idx, node in enumerate(contents):
                words_line = []
                for word in node[0]:
                    words_line.append(vocab_dic.get(word, vocab_dic.get(UNK)))
                contents[idx] = (words_line, node[1], node[2]) #node[3]

    if show == True:
        avg = sum(rows_len) / len(rows_len)
        med = np.median(rows_len)
        print(" max_len : %d , avg : %d, median %d" % (max_len, avg, med) )

    return vocab_dic, contents


class DatasetIterater(object):
    def __init__(self, batches, batch_size, device):
        self.batch_size = batch_size
        self.batches = batches
        self.n_batches = len(batches) // batch_size
        self.residue = False  # 记录batch数量是否为整数
        if len(batches) % self.n_batches != 0:
            self.residue = True
        self.index = 0
        self.device = device
        self.oindex = 0

    def _to_tensor(self, datas):
        try:
            x = torch.LongTensor([_[0] for _ in datas]).to(self.device)
            y = torch.LongTensor([_[1] for _ in datas]).to(self.device)

            # pad前的长度(超过pad_size的设为pad_size)
            seq_len = torch.LongTensor([_[2] for _ in datas]).to(self.device)
            return (x, seq_len), y
        except Exception as e:
            print(datas)
            raise e

    def go_next(self, dev = True):
        self.oindex = self.index
        self.index += 1 if dev == True else 2
        if self.index >= self.n_batches:
            self.index = 0

    def go_prev(self):
        self.index = self.oindex

    def __next__(self):
        if self.residue and self.index == self.n_batches:
            batches = self.batches[self.index * self.batch_size: len(self.batches)]
            self.index += 1
            batches = self._to_tensor(batches)
            return batches

        elif self.index >= self.n_batches:
            self.index = 0
            raise StopIteration
        else:
            batches = self.batches[self.index * self.batch_size: (self.index + 1) * self.batch_size]
            self.index += 1
            batches = self._to_tensor(batches)
            return batches

    def __iter__(self):
        return self

    def __len__(self):
        if self.residue:
            return self.n_batches + 1
        else:
            return self.n_batches


def build_iterator(dataset, config):
    iter = DatasetIterater(dataset, config.batch_size, config.device)
    return iter


def get_time_dif(start_time):
    """获取已使用时间"""
    end_time = time.time()
    time_dif = end_time - start_time
    return timedelta(seconds=int(round(time_dif)))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Stock News Text Classification Build vocab')

    parser.add_argument('-d', '--dataset', type=str, required=True,  help='Dataset Name')
    parser.add_argument('-c', '--csv', nargs='+', required=True,
                            help='-c  csv1 csv2 ...')
    parser.add_argument('-t', '--use_title', default=0, type=int, help='use content|title to vulid vocab')
    parser.add_argument('-a', '--pad_size', default=500, type=int, help='pad_size')
    parser.add_argument('-m', '--min_freq', default=1, type=int, help='min_freq')

    args = parser.parse_args()

    dataset = './log/' + args.dataset
    if os.path.isdir(dataset) == False:
        os.makedirs(dataset, exist_ok=True)

    class Config():
        vocab_path = './log/'
        pad_size = 32
        predict = 1     # 0|1|7
        use_title = 1   # 0|1


    v_config = Config()
    v_config.vocab_path += args.dataset + '/vocab'

    if args.use_title == 1:
        v_config.vocab_path += '_ti'
    else:
        v_config.vocab_path += '_fc'

    v_config.csv = args.csv
    v_config.use_title = args.use_title
    v_config.pad_size = args.pad_size
    v_config.min_freq = args.min_freq

    v_config.vocab_path += '_ps' + str(args.pad_size)
    v_config.vocab_path += '_mf' + str(args.min_freq)
    v_config.vocab_path += '.pkl'

    print("save to %s " % v_config.vocab_path )
    build_dataset(v_config, True)
