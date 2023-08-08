# mark.py

import re
import time

import jieba
import torch
from model import BertClassifier
import requests
from transformers import BertTokenizer, BertConfig, AutoTokenizer, BertModel
import random
import torch.nn as nn
from feature import getFeature, stop_word


class MaskHandler:
    def __init__(self, model_path):
        # Initialize the local BERT model
        self.labels = ["N", "P", "A", "E", "O"]
        self.bert_config = BertConfig.from_pretrained('bert-base-chinese')
        self.model = BertClassifier(self.bert_config, len(self.labels))
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')), strict=False)
        self.model.eval()
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

        # Initialize the cloud-based roberta model
        self.cloud_tokenizer = AutoTokenizer.from_pretrained("hfl/chinese-roberta-wwm-ext-large")

    def classic(self, query):
        text = jieba.lcut(query)
        sensitive_words = []
        for tmp_text in text:
            print(tmp_text)
            token = self.tokenizer(tmp_text, add_special_tokens=True, padding='max_length', truncation=True,
                                   max_length=512)
            input_ids = token['input_ids']
            attention_mask = token['attention_mask']
            token_type_ids = token['token_type_ids']
            input_ids = torch.tensor([input_ids], dtype=torch.long)
            attention_mask = torch.tensor([attention_mask], dtype=torch.long)
            token_type_ids = torch.tensor([token_type_ids], dtype=torch.long)
            predicted = self.model(input_ids, attention_mask, token_type_ids)
            pred_label = torch.argmax(predicted, dim=1)
            if self.labels[pred_label] in ["A", "E", "P", "N"]:
                sensitive_words.append(tmp_text)

        return sensitive_words

    def mask_sensitive_info(self, text, sensitive):
        for word in sensitive:
            # text_jieba = jieba.lcut(text)
            tmp_word = word
            length = (int)(len(word) / 2)
            list = range(0, len(word))
            py = random.sample(list, length)
            for count in range(0, length):
                pos = py[count]
                masked_sensitive = tmp_word[:pos] + '*' + tmp_word[pos + 1:]
                tmp_word = masked_sensitive
                #print(tmp_word)
            text = re.sub(word, masked_sensitive, text, flags=re.IGNORECASE)
            #print(text)
        return text

#把句子按标点符号分割
def fun_splite(text):
    outstr = text.strip()
    pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|：|！| |…|（|）,·'
    result_list = re.split(pattern, outstr)

    return result_list

#把句子内部用停词表分割
def fun_splitein(text):
    sentence_depart = jieba.lcut(text.strip())
    stopwords = stop_word()
    outstr = ""
    for word in sentence_depart:
        if word not in stopwords:
            if word != "\t":
                outstr += word
                # outstr += " "
    return outstr

#判断是否敏感，目前模型识别的不行，所以没用
def fun_isSen(maskHandler, text):
    flag = False
    token = maskHandler.tokenizer(text, add_special_tokens=True, padding='max_length', truncation=True,
                                  max_length=512)
    input_ids = token['input_ids']
    attention_mask = token['attention_mask']
    token_type_ids = token['token_type_ids']
    input_ids = torch.tensor([input_ids], dtype=torch.long)
    attention_mask = torch.tensor([attention_mask], dtype=torch.long)
    token_type_ids = torch.tensor([token_type_ids], dtype=torch.long)
    predicted = maskHandler.model(input_ids, attention_mask, token_type_ids)
    output = torch.softmax(predicted, dim=1)
    #print(output)
    if output[:, 0].item() > 0.70:
        flag = True
    return flag

#将tdidf返回的不敏感词组取反，返回敏感词组
def getSen(nosen, text):
    #print(nosen)
    sen = []
    text_jieba = jieba.lcut(text)
    for word in text_jieba:
        if word not in nosen and len(word) > 1:
            if word not in sen:
                sen.append(word)
    return sen

def fun_1(text):
    maskHandler = MaskHandler("models/best_model.pkl")
    text_splite = fun_splite(text)
    tmp = text
    for tmp_text in text_splite:
        text_stop = fun_splitein(tmp_text)
        # print(text_stop)
        #if fun_isSen(maskHandler5, text_stop, 5):
        if True:#模型能够识别的精准时替换
            sen_fea = getSen(getFeature(text_stop), text_stop)
            res = maskHandler.mask_sensitive_info(tmp, sen_fea)
            #res = re.sub(tmp_text, tmp_res, text, flags=re.IGNORECASE)
            #print(res)
            tmp = res
            #print(sen_fea)
    #print(res)
    #print(tmp)
    return tmp



