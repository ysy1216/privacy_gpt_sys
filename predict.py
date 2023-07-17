# coding: utf-8
# @File: predict.py
import re
import jieba
import torch
from model import BertClassifier
from transformers import BertTokenizer, BertConfig
labels = ["敏感", "不敏感"]
bert_config = BertConfig.from_pretrained('bert-base-chinese')
# 定义模型
model = BertClassifier(bert_config, len(labels))
# 加载训练好的模型
model.load_state_dict(torch.load('../models/best_model.pkl', map_location=torch.device('cpu')))
model.eval()
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
def classic(query):
    print("脱敏前:" + query)
    text = jieba.lcut(query)
    #print(text)
    sensitive_words = []
    for tmp_text in text:
        token = tokenizer(tmp_text, add_special_tokens=True, padding='max_length', truncation=True, max_length=512)
        input_ids = token['input_ids']
        attention_mask = token['attention_mask']
        token_type_ids = token['token_type_ids']
        input_ids = torch.tensor([input_ids], dtype=torch.long)
        attention_mask = torch.tensor([attention_mask], dtype=torch.long)
        token_type_ids = torch.tensor([token_type_ids], dtype=torch.long)
        predicted = model(
            input_ids,
            attention_mask,
            token_type_ids,
            )
        pred_label = torch.argmax(predicted, dim=1)
        if labels[pred_label] == "敏感":
            sensitive_words.append(tmp_text)
            #print(sensitive_words)
        #print('Label:', labels[pred_label])
    print("脱敏后:" + mask_sensitive_info(query, sensitive_words))
def mask_sensitive_info(text, sensitive_words):
    #print(sensitive_words)
    for word in sensitive_words:
        masked_word = ""
        print(len(word))
        for i in range(0, (int)(len(word)/2)):
            masked_word += "*"
        masked_sensitive = word[:-((int)(len(word)/2))] + masked_word
        #print(masked_sensitive)
        text = re.sub(word, masked_sensitive, text, flags=re.IGNORECASE)
    return text
