import math
from KNN_function import init
from KNN_function import validation
K = 2
dictionary = set()
Mood = set()
Word = []
Label = []
tf = []
idf = {}
if __name__ == '__main__':
    n = init(Word, Label, dictionary)
    dictionary = list(dictionary)
    for word in dictionary:
        idf[word] = 0
    train_n = int(n * 0.9)
    print(len(dictionary))
    for i in range(train_n):
        lenth = len(Word[i])
        tf_tmp = {}
        for word in dictionary:
            tf_tmp[word] = 0
        for word in Word[i]:
            tf_tmp[word] = tf_tmp[word] + 1
        for word in dictionary:
            if tf_tmp[word] != 0:
                idf[word] = idf[word] + 1
            tf_tmp[word] = tf_tmp[word]/lenth
        tf.append(tf_tmp)

    for word in dictionary:
        idf[word] = math.log(n / (1 + idf[word]))

    K = int(math.sqrt(train_n))
    res = validation(tf, idf, dictionary, K, Word, Label,  n, train_n)
    print(res)
