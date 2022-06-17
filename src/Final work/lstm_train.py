#! /bin/env python
# -*- coding: utf-8 -*-
"""
训练网络，并保存模型，其中LSTM的实现采用Python中的keras库
"""
import pandas as pd
import numpy as np
import keras
import multiprocessing

from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary
from keras.preprocessing import sequence

from sklearn.model_selection import train_test_split
from keras.models import Sequential
from tensorflow.python.keras.layers.embeddings import Embedding
from tensorflow.python.keras.layers.recurrent import LSTM
from tensorflow.python.keras.layers.core import Dense, Dropout, Activation
from keras import backend as K

np.random.seed(1337)  # For Reproducibility
import sys
sys.setrecursionlimit(1000000)

# set parameters:
cpu_count = multiprocessing.cpu_count()
vocab_dim = 300
n_iterations = 1  # ideally more..
n_exposures = 10 # 所有频数超过10的词语
window_size = 7
n_epoch = 5
input_length = 100
maxlen = 100

batch_size = 32


def loadfile():
    # neg=pd.read_csv('../data/neg.csv',header=None,index_col=None)
    # pos=pd.read_csv('../data/pos.csv',header=None,index_col=None,error_bad_lines=False)
    # neu=pd.read_csv('../data/neutral.csv', header=None, index_col=None)
    #
    # combined = np.concatenate((pos[0], neu[0], neg[0]))
    # y = np.concatenate((np.ones(len(pos), dtype=int), np.zeros(len(neu), dtype=int),
    #                     -1*np.ones(len(neg),dtype=int)))
    #
    # return combined,y
    f = pd.read_csv('./dataset/high_times.csv',header=None,index_col=None)
    text = f[0]
    y = f[1]
    # print(text)
    # input()
    return text, y


def tokenizer(text):
    tmp = []
    for sentence in text:
        ttmp = sentence.split(' ')
        ttmp.pop()
        tmp.append(ttmp)
        # print(ttmp)
        # input()
    return tmp


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


def word2vec_train(combined):
    model = Word2Vec(vector_size=vocab_dim, window=window_size, workers=cpu_count)
    model.build_vocab(combined)
    model.train(combined, total_words=model.corpus_count, epochs=50)
    model.save('./lstm/Word2vec_model.pkl')
    index_dict, word_vectors, combined = create_dictionaries(model=model, combined=combined)
    return index_dict, word_vectors, combined


def get_data(index_dict,word_vectors,combined,y):

    n_symbols = len(index_dict) + 1  # 所有单词的索引数，频数小于10的词语索引为0，所以加1
    embedding_weights = np.zeros((n_symbols, vocab_dim)) # 初始化 索引为0的词语，词向量全为0
    for word, index in index_dict.items(): # 从索引为1的词语开始，对每个词语对应其词向量
        embedding_weights[index, :] = word_vectors[word]
    x_train, x_test, y_train, y_test = train_test_split(combined, y, test_size=0.2)
    y_train = keras.utils.to_categorical(y_train,num_classes=2)
    y_test = keras.utils.to_categorical(y_test,num_classes=2)
    # print x_train.shape,y_train.shape
    return n_symbols,embedding_weights,x_train,y_train,x_test,y_test


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


def train_lstm(n_symbols,embedding_weights,x_train,y_train,x_test,y_test):
    print('Defining a Simple Keras Model...')
    model = Sequential()
    model.add(Embedding(output_dim=vocab_dim,
                        input_dim=n_symbols,
                        mask_zero=True,
                        weights=[embedding_weights],
                        input_length=input_length))
    model.add(LSTM(units=50, activation='tanh'))
    model.add(Dropout(0.5))
    model.add(Dense(2, activation='softmax'))
    model.add(Activation('softmax'))

    print('Compiling the Model...')
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy', f1])

    print("Train...") # batch_size=32
    model.fit(x_train, y_train, batch_size=batch_size, epochs=n_epoch, verbose=1)

    print("Evaluate...")
    score = model.evaluate(x_test, y_test, batch_size=batch_size)

    model_json = model.to_json()
    with open('./lstm/lstm.json', 'w') as outfile:
        outfile.write(model_json)
    model.save_weights('./lstm/lstm.h5')
    print('Test score:', score)


print('Loading Data...')
combined, y = loadfile()
print(len(combined), len(y))
print('Tokenising...')
combined = tokenizer(combined)
print('Training a Word2vec model...')
index_dict, word_vectors, combined = word2vec_train(combined)

print('Setting up Arrays for Keras Embedding Layer...')
n_symbols, embedding_weights, x_train, y_train, x_test, y_test = get_data(index_dict, word_vectors, combined, y)
print("x_train.shape and y_train.shape:")
print(x_train.shape,y_train.shape)
train_lstm(n_symbols,embedding_weights,x_train,y_train,x_test,y_test)