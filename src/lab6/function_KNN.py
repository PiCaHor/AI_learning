import math


def init(Word, Label, dictionary, Mood):
    fl = True
    num = 0
    with open('./dataset/train_set.csv') as file_object:
        for line in file_object.readlines():
            if fl:
                fl = False
                continue
            line = line.split('\n')
            line = line[0].split(',')
            words = line[0].split(' ')
            g = []
            for word in words:
                g.append(word)
                dictionary.add(word)
            Word.append(g)
            Label.append(line[1])
            Mood.add(line[1])
            num = num + 1
    # 加入测试集
    fl = True
    with open('./dataset/validation_set.csv') as file_object:
        for line in file_object.readlines():
            if fl:
                fl = False
                continue
            line = line.split('\n')
            line = line[0].split(',')
            words = line[0].split(' ')
            g = []
            for word in words:
                g.append(word)
                dictionary.add(word)
            Word.append(g)
            Label.append(line[1])
            Mood.add(line[1])
            num = num + 1
    return num


def cal_dis(idf, tf, test_tf, dictionary):
    res = 0
    for word in dictionary:
        res += idf[word] * idf[word] * (tf[word] - test_tf[word]) * (tf[word] - test_tf[word])
    res = math.sqrt(res)
    return res


def KNN(tf, idf, Mood, dictionary, K, words, Label,  n):
    dis = []
    test_tf = {}
    for word in dictionary:
        test_tf[word] = 0
    lenth = len(words)
    for word in words:
        if word in dictionary:
            test_tf[word] += 1
    for word in dictionary:
        test_tf[word] /= lenth
    for i in range(n):
        distance = cal_dis(idf, tf[i], test_tf, dictionary)
        dis.append((distance, Label[i]))
    dis = sorted(dis, key=lambda x: x[0], reverse=True)
    cnt = {}
    for mood in Mood:
        cnt[mood] = 0
    ans = ''
    anst = 0
    for i in range(K):
        cnt[dis[i][1]] += 1
        if ans == '':
            ans = dis[i][1]
            anst = cnt[dis[i][1]]
        elif anst < cnt[dis[i][1]]:
            ans = dis[i][1]
            anst = cnt[dis[i][1]]
    return ans


def validation(tf, idf, Mood, dictionary, K, Label,  n):
    num = 0
    cur = 0
    fl = True
    with open('./dataset/validation_set.csv') as file_object:
        for line in file_object.readlines():
            if fl:
                fl = False
                continue
            num = num + 1
            line = line.split('\n')
            line = line[0].split(',')
            words = line[0].split(' ')

            ans = KNN(tf, idf, Mood, dictionary, K, words, Label,  n)

            if ans == line[1]:
                cur += 1

    return cur/num


def test(tf, idf, Mood, dictionary, K, Label,  n):
    num = 0
    fl = True
    with open('./result/20337228_pengchenhan_KNN_classification.csv', 'w') as file_object1:
        file_object1.write('textid,Words (split by space),label\n')
    with open('./dataset/test_set.csv') as file_object:
        for line in file_object.readlines():
            if fl:
                fl = False
                continue
            num = num + 1
            line = line.split('\n')
            line = line[0].split(',')
            stmp = line[0] + ',' + line[1] + ','
            words = line[1].split(' ')

            ans = KNN(tf, idf, Mood, dictionary, K, words, Label,  n)

            with open('./result/20337228_pengchenhan_KNN_classification.csv', 'a') as file_object1:
                file_object1.write(stmp + ans + '\n')

# one hot 方法
'''
import math


def init(Word, Label, dictionary, Mood):
    fl = True
    num = 0
    with open('./dataset/train_set.csv') as file_object:
        for line in file_object.readlines():
            if fl:
                fl = False
                continue
            line = line.split('\n')
            line = line[0].split(',')
            words = line[0].split(' ')
            g = []
            for word in words:
                g.append(word)
                dictionary.add(word)
            Word.append(g)
            Label.append(line[1])
            Mood.add(line[1])
            num = num + 1
    return num


def cal_dis(one_hot, test, dictionary):
    res = 0
    for word in dictionary:
        res += (one_hot[word] - test[word]) * (one_hot[word] - test[word])
    res = math.sqrt(res)
    return res


def KNN(one_hot, Mood, dictionary, K, words, Label,  n):
    dis = []
    test = {}
    for word in dictionary:
        test[word] = 0
    for word in words:
        if word in dictionary:
            test[word] = 1
    for i in range(n):
        distance = cal_dis(one_hot[i], test, dictionary)
        dis.append((distance, Label[i]))
    dis = sorted(dis, key=lambda x: x[0], reverse=True)
    cnt = {}
    for mood in Mood:
        cnt[mood] = 0
    ans = ''
    anst = 0
    for i in range(K):
        cnt[dis[i][1]] += 1
        if ans == '':
            ans = dis[i][1]
            anst = cnt[dis[i][1]]
        elif anst < cnt[dis[i][1]]:
            ans = dis[i][1]
            anst = cnt[dis[i][1]]
    return ans


def validation(one_hot, Mood, dictionary, K, Label,  n):
    num = 0
    cur = 0
    fl = True
    with open('./dataset/validation_set.csv') as file_object:
        for line in file_object.readlines():
            if fl:
                fl = False
                continue
            num = num + 1
            line = line.split('\n')
            line = line[0].split(',')
            words = line[0].split(' ')
            ans = KNN(one_hot, Mood, dictionary, K, words, Label,  n)

            if ans == line[1]:
                cur += 1

    return cur/num
'''