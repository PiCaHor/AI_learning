#! /bin/env python
# -*- coding: utf-8 -*-
"""
预测
"""
import jieba
import numpy as np
from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary
from keras.preprocessing import sequence
from tensorflow.keras.models import (Model, model_from_json, load_model)
from keras import backend as K

np.random.seed(1337)  # For Reproducibility
import sys

sys.setrecursionlimit(1000000)

# define parameters
maxlen = 100


def create_dictionaries(model=None, combined=None):
    if (combined is not None) and (model is not None):
        gensim_dict = Dictionary()
        gensim_dict.doc2bow(model.wv.index_to_key,allow_update=True)
        w2indx = {v: k+1 for k, v in gensim_dict.items()}
        w2vec = {word: model.wv[word] for word in w2indx.keys()}

        def parse_dataset(combined):
            data = []
            for sentence in combined:
                new_txt = []
                for word in sentence:
                    try:
                        new_txt.append(w2indx[word])
                    except:
                        new_txt.append(0)
                data.append(new_txt)
            return data
        combined = parse_dataset(combined)
        combined = sequence.pad_sequences(combined, maxlen=maxlen)
        return w2indx, w2vec, combined
    else:
        print('No data provided...')


def input_transform(string):
    words = string.split(' ')
    words = np.array(words).reshape(1, -1)
    model = Word2Vec.load('./lstm/Word2vec_model.pkl')
    _, _, combined = create_dictionaries(model, words)
    return combined


def f1(y_true, y_pred):
    def recall(y_true, y_pred):
        """Recall metric.
        Only computes a batch-wise average of recall.
        Computes the recall, a metric for multi-label classification of
        how many relevant items are selected.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

    def precision(y_true, y_pred):
        """Precision metric.
        Only computes a batch-wise average of precision.
        Computes the precision, a metric for multi-label classification of
        how many selected items are relevant.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision

    precision = precision(y_true, y_pred)
    recall = recall(y_true, y_pred)
    return 2 * ((precision * recall) / (precision + recall + K.epsilon()))


fw = open('./dataset/result.csv', 'w', encoding='utf-8')


def lstm_predict():
    print('loading model......')
    with open('./lstm/lstm.json', 'r') as f:
        model = model_from_json(f.read())

    print('loading weights......')
    model.load_weights('./lstm/lstm.h5')
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy', f1])
    cnt = 113000
    fw.write("sentenceID,gold_label\n")
    with open('./dataset/final.csv', encoding='utf-8') as file_object:
        for string in file_object.readlines():
            string = string.strip()
            data = input_transform(string)
            data.reshape(1, -1)
            result = model.predict_classes(data)
            fw.write(str(cnt) + ',' + str(result[0]) + '\n')
            cnt += 1
            print(cnt, result[0])
    fw.close()


if __name__ == '__main__':
    # string = "should he agree to go there we would send him there"
    lstm_predict()
