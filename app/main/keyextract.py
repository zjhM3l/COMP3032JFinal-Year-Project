import sys,codecs
import pandas as pd
import numpy as np
import jieba.posseg
import jieba.analyse
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

from app.models import Post


def dataPrepos(text, stopkey):
    l = []
    pos = ['n', 'nz', 'v', 'vd', 'vn', 'l', 'a', 'd']
    seg = jieba.posseg.cut(text)
    for i in seg:
        if i.word not in stopkey and i.flag in pos:
            l.append(i.word)
    return l


def getKeywords_tfidf(stopkey,topK):
    posts = Post.query.all()
    corpus = []
    for index in range(len(posts)):
        text = '%s。%s' % (posts[index].title, posts[index].body)
        text = dataPrepos(text,stopkey)
        text = " ".join(text)
        corpus.append(text)

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)

    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(X)

    word = vectorizer.get_feature_names()

    weight = tfidf.toarray()

    ids, titles, keys = [], [], []
    for i in range(len(weight)):

        ids.append(posts[i].id)
        titles.append(posts[i].title)
        df_word,df_weight = [],[]
        for j in range(len(word)):

            df_word.append(word[j])
            df_weight.append(weight[i][j])
        df_word = pd.DataFrame(df_word,columns=['word'])
        df_weight = pd.DataFrame(df_weight,columns=['weight'])
        word_weight = pd.concat([df_word, df_weight], axis=1)
        word_weight = word_weight.sort_values(by="weight",ascending = False)
        keyword = np.array(word_weight['word'])
        word_split = [keyword[x] for x in range(0,topK)]
        word_split = " ".join(word_split)
        keys.append(word_split)

    result = pd.DataFrame({"id": ids, "title": titles, "key": keys},columns=['id','title','key'])
    return result


def testKey():
    encoding = "utf-8"
    stopkey = [w.strip() for w in codecs.open('app/static/stopWord.txt', 'r', encoding=encoding).readlines()]

    result = getKeywords_tfidf(stopkey,10)
    result.to_csv("app/static/result/keys_TFIDF.csv", index=False)
    return result




