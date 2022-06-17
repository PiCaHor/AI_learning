import math


def init(charactor, label):
    num = 0
    size = 0
    with open('./dataset/tf_idf.csv') as file_object:
        for line in file_object.readlines():
            num += 1
            line = line.strip()
            line = line.split(',')
            if size == 0:
                size = len(line)
                # print(size)
                # input()
            g = [1]
            for i in range(size-1):
                g.append(float(line[i]))
            charactor.append(g)
            if line[size-1] == '0':
                label.append(0)
            else:
                label.append(1)
    return num, size


def change(w, x, y, learn_rat, n):
    for i in range(n):
        w[i] += learn_rat * y * x[i]


def sigmoid(a, b, n):
    res = 0
    for i in range(n):
        res += a[i] * b[i]
    # print(res)
    return 1.0/(1.0 + math.exp(-res))
