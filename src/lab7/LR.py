from LR_function import init
from LR_function import sigmoid
import math

label = []
charactor = []
learn_rat = 0.00001
max_train = 99999
circle_time = 5000

if __name__ == '__main__':
    n = init(charactor, label)
    w = []
    for i in range(41):
        w.append(0)
    validation_begin = math.ceil(n * 0.9)
    validation_end = n

    for i in range(circle_time):
        print('train: ' + str(i))
        update = []
        for j in range(41):
            update.append(0)
        for j in range(n):
            tmp = sigmoid(w, charactor[j], 41)
            for k in range(41):
                update[k] += (label[j] - tmp) * charactor[j][k]
        for j in range(41):
            w[j] += learn_rat * update[j]

    cur = 0
    lenth = validation_end - validation_begin
    ans = 0
    for i in range(lenth):
        y = sigmoid(w, charactor[validation_begin + i], 41)
        if y > 0.5:
            ans = 1
        else:
            ans = 0
        if ans == label[validation_begin + i]:
            cur += 1
    print(cur/lenth)

    # length = 0
    # test_charactor = []
    # with open('./dataset/test.csv') as file_object:
    #     for line in file_object.readlines():
    #         length += 1
    #         line = line.split('\n')
    #         line = line[0].split(',')
    #         g = [1]
    #         for i in range(40):
    #             g.append(float(line[i]))
    #         test_charactor.append(g)
    #
    # for i in range(length):
    #     y = sigmoid(w, test_charactor[i], 41)
    #     if y > 0.5:
    #         print('ex ' + str(i+1) + " is 1")
    #     else:
    #         print('ex ' + str(i+1) + " is -1")
