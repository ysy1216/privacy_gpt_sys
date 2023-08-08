# -*- coding: utf-8 -*-
import jieba
from pandas import DataFrame
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.naive_bayes import BernoulliNB
def importdata():
    text_list = []
    for i in range(3, 13):
        file_path = r"data/Info/info" + str(i) + ".txt"
        with open(file_path, encoding="UTF-8") as f:
            text = f.read()
            # text_jieba = jieba.cut(text, cut_all=True)
            text_jieba = jieba.lcut(text)
            text_jieba = " ".join(text_jieba)
            # print(text_jieba)
            text_list.append(text_jieba)
            f.close()
    #print(text_list)
    return text_list


def inputSen(text):
    text_jieba = jieba.lcut(text)
    return text_jieba


def stop_word():
    stopword_list = []
    for i in range(1, 5):
        file_path = r"data/StopWord/StopWord" + str(i) + ".txt"
        with open(file_path, encoding="UTF-8") as f:
            stopword = f.read().split("\n")
            for j in range(0, len(stopword)):
                stopword_list.append(stopword[j])
    # print(stopword)
    return stopword_list


def getFeature(sentence):
    vectorizer = TfidfVectorizer(stop_words=stop_word())
    # 转换数据
    X = vectorizer.fit_transform(importdata()).toarray()
    # 查看特征
    #X_fea = vectorizer.get_feature_names()
    X_fea = vectorizer.get_feature_names_out()
    #print(X_fea)
    # print(X)
    # 生成分析库
    analyzer = vectorizer.build_analyzer()
    #print(analyzer)
    #sentence_jieba = jieba.lcut(sentence)
    sentence_jieba = jieba.lcut(sentence)
    sentence_jieba = " ".join(sentence_jieba)
    sentence_jieba = [sentence_jieba]
    #print(sentence_jieba)
    res = vectorizer.transform(sentence_jieba).toarray()
    #print(res)
    #print(res.max())
    X_pd: DataFrame = pd.DataFrame(res, columns=X_fea)
    #print(X_pd)
    #for i in range(0, 2):
    #    print(X_pd.sort_values(by=i, axis=1, ascending=False))
    X_pd_sort = X_pd.sort_values(by=0, axis=1, ascending=False)
    #print(X_pd_sort)
    nosentitve = []
    for i in range(0, 50):
        #print(X_pd_sort.iat[0, i])
        #print(X_pd_sort.iloc[:, i])
        if X_pd_sort.iat[0, i] > 0.40:
            tmp = X_pd_sort.iloc[:, i]
            tmp_frame = tmp.to_frame()
            #word = tmp_frame.columns.values
            word = "".join(tmp_frame.columns.tolist())
            #print(word)
            if word not in nosentitve:
                nosentitve.append(word)
        else:
            break
    #print(word)
    #print(nosentitve)
    return nosentitve
