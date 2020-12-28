# coding: UTF-8
import os, math
import torch, nltk
import numpy as np
import pickle as pkl
from tqdm import tqdm
import time
from datetime import timedelta
import pandas as pd

pd.options.mode.chained_assignment = None

MAX_VOCAB_SIZE = 40000  # 词表长度限制
UNK, PAD = '<UNK>', '<PAD>'  # 未知字，padding符号
# tokenizer = lambda x: x.split(' ')

def fetch_data(config, test = False ,ticker = ''):
    """
        @param object  config  Config
        @param boolean test,   create test set
        @param string  ticker,  select ticker only
    """
    cols = [ 'source', 'date', 'ticker',
                'title', 'content_fp', '0dr',
                '1dr', '7dr', '30dr',
                '1d', '7d', '30d',
                '1dt', '7dt', '30dt']

    start_date = '2013-01-01'
    end_date = '2019-12-31'
    li = []

    for csvfn in config.csv:
        df = pd.read_csv(csvfn, index_col=None, header=0)
        df = df.iloc[1:]
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)
    li = None

    df = frame[cols]
    use_tag = ''
    if config.predict == 1:
        use_tag = '1dt'
    elif config.predict == 7:
        use_tag = '7dt'
    else:
        use_tag = '30dt'

    df = df.loc[:, ['date', 'title', 'ticker', 'content_fp', use_tag]]

    df.set_index('date')
    mask = (df['date'] > start_date) & (df['date'] < end_date)
    mask2 = (df['date'] > end_date)
    df_main = df.loc[mask]
    df_2020 = df.loc[mask2]
    if ticker != '':
        df_main = df_main.loc[df_main['ticker'] == ticker]
        df_2020 = df_2020.loc[df_2020['ticker'] == ticker]

    df_main.sort_values(by='date', inplace=True, ascending=True)
    df_test = [] if test != True else df_main.sample(frac=0.1).copy(deep = True)

    # df_2020 = df_2020.sample(frac=0.5)

    if test == True :
        drop_index = []
        for row in df_test.itertuples():
            drop_index.append(row.Index)
        df_main = df_main.drop(drop_index)

    return df_main, df_2020, df_test

def build_vocab(config, showv = False):
    """
        build vocab
        @param object {vocab_path, rebuild, show, use_title, min_freq }
    """


    if config.vocab_path == '' :
        config.vocab_path = './vecs/vocab_' +  config.dataset
        config.vocab_path += '_t' if config.use_title == 1 else '_a'
        config.vocab_path += '_p' + str(config.pad_size)
        config.vocab_path += '_f' + str(config.min_freq)
        config.vocab_path += '.pkl'
        print("vocab_path is %s " % config.vocab_path )

    if os.path.exists(config.vocab_path) and config.rebuild == False:
        vocab_dic = pkl.load(open(config.vocab_path, 'rb'))
        if showv :
            print(vocab_dic)
        print(f"Vocab size: {len(vocab_dic)}")
        return vocab_dic
    else:
        vocab_dic = {}
        # print("rebuild")

    rows_len = []
    max_len = 0
    df, _, _ = fetch_data(config)

    for row in df.itertuples():
        content = ''
        if config.use_title == 0 :
            with open(row.content_fp, 'r', encoding='UTF-8') as f:
                content = f.read().lower()
        else:
            content = row.title
        clen = len(content)
        if clen > max_len:
            max_len = clen

        if config.show == True:
            rows_len.append(clen)

        words_line = []
        token = nltk.tokenize.word_tokenize(content)
        seq_len = len(token)

        for word in token:
            vocab_dic[word] = vocab_dic.get(word, 0) + 1
        vocab_list = sorted([_ for _ in vocab_dic.items() if _[1] >= config.min_freq], key=lambda x: x[1], reverse=True)[:MAX_VOCAB_SIZE]
        vocab_dic = {word_count[0]: idx for idx, word_count in enumerate(vocab_list)}
        vocab_dic.update({UNK: len(vocab_dic), PAD: len(vocab_dic) + 1})

        pkl.dump(vocab_dic, open(config.vocab_path, 'wb'))

    if config.show == True:
        avg = sum(rows_len) / len(rows_len)
        med = np.median(rows_len)
        print("max_len : %d , avg : %d, median %d" % (max_len, avg, med) )
        print(f"Vocab size: {len(vocab_dic)}")

    if showv :
        print(vocab_dic)

    return vocab_dic

def build_dataset(config, ticker = ''):

    pad_size = config.pad_size
    vocab = build_vocab(config)
    df, df_20, df_test =  fetch_data(config, ticker=ticker, test = True)

    def biGramHash(sequence, t, buckets):
        t1 = sequence[t - 1] if t - 1 >= 0 else 0
        return (t1 * 14918087) % buckets

    def triGramHash(sequence, t, buckets):
        t1 = sequence[t - 1] if t - 1 >= 0 else 0
        t2 = sequence[t - 2] if t - 2 >= 0 else 0
        return (t2 * 14918087 * 18408749 + t1 * 14918087) % buckets

    def sub_vocab(token, seq_len, label):
        words_line = []
        for word in token:
            words_line.append(vocab.get(word, vocab.get(UNK)))

        if config.model_name == 'FastText':
            buckets = config.n_gram_vocab
            bigram = []
            trigram = []
            # ------ngram------
            for i in range(pad_size):
                bigram.append(biGramHash(words_line, i, buckets))
                trigram.append(triGramHash(words_line, i, buckets))
            # -----------------
            return (words_line, int(label), seq_len, bigram, trigram)
        else:
            return (words_line, int(label), seq_len)

    def build_set(dl):
        contents = []

        token_len = []
        max_len = 0
        counter = 0

        for row in dl.itertuples():
            counter += 1
            label = ''

            if config.num_classes == 3:
                if row._5 == 1 or row._5 == 2:
                    label = 0
                elif row._5 == 4 or row._5 == 5:
                    label = 2
                else:
                    label = 1
            else:
                label = row._5

            content = ''
            if config.use_title == 0 :
                with open(row.content_fp, 'r', encoding='UTF-8') as f:
                    content = f.read().lower()
            else:
                content = row.title


            token = nltk.tokenize.word_tokenize(content)
            seq_len = len(token)

            clen = len(token)
            if clen > max_len:
                max_len = clen
            token_len.append(clen)

            if pad_size and len(token) < pad_size:
                token.extend([PAD] * (pad_size - len(token)))


            if (clen / pad_size) < 1.2 :
                token = token[:pad_size]
                seq_len = pad_size
                contents.append(sub_vocab(token, seq_len, label))
            else :
                for i in range(1, math.floor(clen / pad_size)):
                    start = (i-1) * pad_size
                    end = i * pad_size
                    if end > clen:
                        start = start - (end - clen)
                        end = clen

                    tmp_token = token[start:end]
                    seq_len = pad_size

                    # print("total %d, i:%d,  start %d, end %d fetch %d" % (clen, i, start, end, len(tmp_token) ))
                    contents.append(sub_vocab(tmp_token, seq_len, label))

        avg = sum(token_len) / len(token_len)
        med = np.median(token_len)
        print("total row %d; word vocab, max_len : %d , avg : %d, median %d to total %d" % (counter, max_len, avg, med, len(contents)) )

        return contents

    return vocab, build_set(df), build_set(df_20), build_set(df_test)

class DatasetIterater(object):
    FastText = False
    def __init__(self, batches, batch_size, device, fasttext = False):
        self.batch_size = batch_size
        self.batches = batches
        self.n_batches = len(batches) // batch_size
        self.residue = False  # 记录batch数量是否为整数
        if len(batches) % self.n_batches != 0:
            self.residue = True
        self.index = 0
        self.device = device
        self.oindex = 0
        self.fasttext = fasttext

    def _to_tensor(self, datas):
        try:
            x = torch.LongTensor([_[0] for _ in datas]).to(self.device)
            y = torch.LongTensor([_[1] for _ in datas]).to(self.device)
            seq_len = torch.LongTensor([_[2] for _ in datas]).to(self.device)

            if self.fasttext:
                bigram = torch.LongTensor([_[3] for _ in datas]).to(self.device)
                trigram = torch.LongTensor([_[4] for _ in datas]).to(self.device)
                return (x, seq_len, bigram, trigram), y

            else:
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
    if config.model_name == 'FastText':
        iter = DatasetIterater(dataset, config.batch_size, config.device, True)
    else :
        iter = DatasetIterater(dataset, config.batch_size, config.device)
    return iter

def get_time_dif(start_time):
    end_time = time.time()
    time_dif = end_time - start_time
    return timedelta(seconds=int(round(time_dif)))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Stock News Text Classification Build vocab')
    parser.add_argument('-d', '--dataset', type=str, required=True,  help='Dataset Name')
    parser.add_argument('-c', '--csv', nargs='+', help='-c  csv1 csv2 ...')
    parser.add_argument('-t', '--use_title', default=0, type=int, help='use content|title to vulid vocab')
    parser.add_argument('-a', '--pad_size', default=500, type=int, help='pad_size')
    parser.add_argument('-m', '--min_freq', default=5, type=int, help='min_freq')
    parser.add_argument('-r', '--rebuild', default=1, choices=[0,1], type=int, help='1:rebuild')
    parser.add_argument('-s', '--show', default=1, choices=[0,1], type=int, help='1:show news info len avg median')

    parser.add_argument('-v', '--vocab_info', default=0, choices=[0,1], type=int, help='1:show vocab list')
    args = parser.parse_args()

    class Config():
        dataset = ''
        vocab_path = ''
        pad_size = 32
        predict = 0
        use_title = 0   # 0|1
        show = True
        min_freq = 2
        rebuild = True


    v_config = Config()

    if args.csv == None :
        v_config.csv = ['./data/news_' + args.dataset + '.csv']
    else :
        v_config.csv = args.csv

    v_config.dataset = args.dataset
    v_config.use_title = args.use_title
    v_config.pad_size = args.pad_size
    v_config.min_freq = args.min_freq
    v_config.rebuild = True if args.rebuild == 1 else False
    v_config.show = True if args.show == 1 else False

    st = time.time()
    build_vocab(v_config, args.vocab_info)

    td = get_time_dif(st)
    print("Build time :", td)
