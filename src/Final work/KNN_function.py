import math


def init(Word, Label, dictionary):
    num = 0
    with open('./dataset/tidy_train.csv') as file_object:
        for line in file_object.readlines():
            line = line.split('\n')
            line = line[0].split(',')
            words = line[1].split(' ')
            g = []
            for word in words:
                g.append(word)
                dictionary.add(word)
            Word.append(g)
            Label.append(line[0])
            num = num + 1
    return num


def cal_dis(idf, tf, test_tf, dictionary):
    res = 0
    for word in dictionary:
        res += idf[word] * idf[word] * (tf[word] - test_tf[word]) * (tf[word] - test_tf[word])
    res = math.sqrt(res)
    return res


def KNN(tf, idf, dictionary, K, words, Label, n):
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
    cnt['0'] = 0
    cnt['1'] = 0
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


def validation(tf, idf, dictionary, K, Word, Label, n, train_n):
    num = 0
    cur = 0
    fl = True
    for i in range(n-train_n):
        print(train_n + i)
        ans = KNN(tf, idf, dictionary, K, Word[train_n+i], Label, train_n)
        if ans == Label[train_n+i]:
            cur += 1
    return cur/num
