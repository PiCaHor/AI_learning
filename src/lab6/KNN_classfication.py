from function_KNN import init
import math
from function_KNN import test
from function_KNN import validation
K = 2
dictionary = set()
Mood = set()
Word = []
Label = []
tf = []
idf = {}
if __name__ == '__main__':
    n = init(Word, Label, dictionary, Mood)
    K = int(math.sqrt(n))
    Mood = list(Mood)
    dictionary = list(dictionary)
    for word in dictionary:
        idf[word] = 0
    for i in range(n):
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

    test(tf, idf, Mood, dictionary, K, Label,  n)

'''
    tmp = 0
    final_K = 0
    K = int(math.sqrt(n))
    while K < 50:
        res = validation(tf, idf, Mood, dictionary, K, Label,  n)
        print(K)
        print(res)
        if res > tmp:
            tmp = res
            final_K = K
        K += 1
    print("final param K:")
    print(final_K)
    print(tmp)
'''


# one_hot 方法
'''
from function_KNN import init
import math
from function_KNN import validation
K = 2
dictionary = set()
Mood = set()
Word = []
Label = []
one_hot = []
if __name__ == '__main__':
    n = init(Word, Label, dictionary, Mood)
    K = int(math.sqrt(n))
    Mood = list(Mood)
    dictionary = list(dictionary)
    for i in range(n):
        tmp = {}
        for word in dictionary:
            tmp[word] = 0
        for word in Word[i]:
            tmp[word] = tmp[word] + 1
        for word in dictionary:
            if tmp[word] != 0:
                tmp[word] = 1
        one_hot.append(tmp)

    res = validation(one_hot, Mood, dictionary, K, Label,  n)
    print(res)
'''