# coding: utf-8
# @File: dataset.py
# @Author: HE D.H.
# @Email: victor-he@qq.com
# @Time: 2021/12/09 11:01:32
# @Description:

import torch
import numpy as np
import torch.nn as nn
from torch.utils.data import Dataset
from transformers import BertTokenizer
from tqdm import tqdm

class CNewsDataset(Dataset):
    def __init__(self, filename):
        # 数据集初始化
        self.labels = ["N", "E", "P", "A", "O"]#N姓名，E邮箱，P手机号，A地址，O其他
        self.labels_id = list(range(len(self.labels)))
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
        self.input_ids = []
        self.token_type_ids = []
        self.attention_mask = []
        self.label_id = []
        self.load_data(filename)
    
    def load_data(self, filename):
        # 加载数据
        print('loading data from:', filename)
        with open(filename, 'r', encoding='utf-8') as rf:
            lines = rf.readlines()
        for line in tqdm(lines, ncols=100):
            text, label = line.strip().split('_')
            #print(text)
            #print(label)
            label_id = self.labels.index(label)
            token = self.tokenizer(text, add_special_tokens=True, padding='max_length', truncation=True, max_length=512)
            self.input_ids.append(np.array(token['input_ids']))
            self.token_type_ids.append(np.array(token['token_type_ids']))
            self.attention_mask.append(np.array(token['attention_mask']))
            self.label_id.append(label_id)

    def __getitem__(self, index):
        return self.input_ids[index], self.token_type_ids[index], self.attention_mask[index], self.label_id[index]

    def __len__(self):
        return len(self.input_ids)

