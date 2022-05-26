# 训练集和验证集默认分成9：1
from PLA_function import init
from PLA_function import sign
from PLA_function import change
import math

label = []
charactor = []
learn_rat = 0.01
max_train = 99999
circle_time = 1000

if __name__ == '__main__':
    n = init(charactor, label)
    w = []
    for i in range(41):
        w.append(1)
    validation_begin = math.ceil(n * 0.9)
    validation_end = n
    # train
    cnt = 0
    best_w = []
    best_count = 99999
    while True:
        count = 0
        cnt += 1
        for i in range(n):
            tmp = sign(w, charactor[i], 41)
            if tmp * label[i] <= 0:
                change(w, charactor[i], label[i], learn_rat, 41)
                # print("Change w")
                # print(w)
                count += 1
        print("Times :" + str(cnt))
        print("Wrong data: " + str(count))
        # print(w)
        if best_count > count:
            best_w = w
            best_count = count
        if count == 0:
            break
        if cnt >= circle_time:
            break

    w = best_w
    # validation
    cur = 0
    lenth = validation_end - validation_begin
    for i in range(lenth):
        y = sign(w, charactor[validation_begin + i], 41)
        if y == label[validation_begin + i]:
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
    #     y = sign(w, test_charactor[i], 41)
    #     if y > 0:
    #         print('ex ' + str(i+1) + " is 1")
    #     else:
    #         print('ex ' + str(i+1) + " is -1")


