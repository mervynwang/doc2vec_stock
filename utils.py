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

def build_dataset(config):

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

    if os.path.exists(config.vocab_path):
        vocab = pkl.load(open(config.vocab_path, 'rb'))
        vocab_build = False
        print(f"Vocab size: {len(vocab)}")

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
    df.sort_values(by='date', inplace=True, ascending=True)

    use_tag = ''
    if config.predict == 1:
        use_tag = '1dt'
    elif config.predict == 7:
        use_tag = '7dt'
    else:
        use_tag = '30dt'

    df = df.loc[:, ['date', 'title', 'content_fp', use_tag]]
    for row in df.itertuples():
        label = row._4
        content = row.title
        if config.use_title == 0 :
            with open(row.content_fp, 'r', encoding='UTF-8') as f:
                content = f.read().lower()
        else:
            content = row.title
        words_line = []
        token = tokenizer(content)
        seq_len = len(token)

        if vocab_build == True:
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
            contents.append((token, int(label), seq_len)) #, row.date
        else:
            for word in token:
                words_line.append(vocab_dic.get(word, vocab_dic.get(UNK)))
            contents.append((words_line, int(label), seq_len)) #, row.date

    if vocab_build == True:
        pkl.dump(vocab_dic, open(config.vocab_path, 'wb'))
        for idx, node in enumerate(contents):
            words_line = []
            for word in node[0]:
                words_line.append(vocab_dic.get(word, vocab_dic.get(UNK)))
            contents[idx] = (words_line, node[1], node[2]) #node[3]

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

    def _to_tensor(self, datas):
        x = torch.LongTensor([_[0] for _ in datas]).to(self.device)
        y = torch.LongTensor([_[1] for _ in datas]).to(self.device)

        # pad前的长度(超过pad_size的设为pad_size)
        seq_len = torch.LongTensor([_[2] for _ in datas]).to(self.device)
        return (x, seq_len), y

    def go_next(self):
        self.index += 1
        if self.index >= self.n_batches:
            self.index = 0

    def go_prev(self):
        self.index -= 1
        # if self.index >= self.n_batches:
        #     self.index = 0

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
    '''提取预训练词向量'''
    # 下面的目录、文件名按需更改。
    train_dir = "./THUCNews/data/train.txt"
    vocab_dir = "./THUCNews/data/vocab.pkl"
    pretrain_dir = "./THUCNews/data/sgns.sogou.char"
    emb_dim = 300
    filename_trimmed_dir = "./THUCNews/data/embedding_SougouNews"
    if os.path.exists(vocab_dir):
        word_to_id = pkl.load(open(vocab_dir, 'rb'))
    else:
        # tokenizer = lambda x: x.split(' ')  # 以词为单位构建词表(数据集中词之间以空格隔开)
        tokenizer = lambda x: [y for y in x]  # 以字为单位构建词表
        word_to_id = build_vocab(train_dir, tokenizer=tokenizer, max_size=MAX_VOCAB_SIZE, min_freq=1)
        pkl.dump(word_to_id, open(vocab_dir, 'wb'))

    embeddings = np.random.rand(len(word_to_id), emb_dim)
    f = open(pretrain_dir, "r", encoding='UTF-8')
    for i, line in enumerate(f.readlines()):
        # if i == 0:  # 若第一行是标题，则跳过
        #     continue
        lin = line.strip().split(" ")
        if lin[0] in word_to_id:
            idx = word_to_id[lin[0]]
            emb = [float(x) for x in lin[1:301]]
            embeddings[idx] = np.asarray(emb, dtype='float32')
    f.close()
    np.savez_compressed(filename_trimmed_dir, embeddings=embeddings)