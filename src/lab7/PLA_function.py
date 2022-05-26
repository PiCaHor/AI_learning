def init(charactor, label):
    num = 0
    with open('./dataset/train.csv') as file_object:
        for line in file_object.readlines():
            num += 1
            line = line.split('\n')
            line = line[0].split(',')
            g = [1]
            for i in range(40):
                g.append(float(line[i]))
            charactor.append(g)
            if line[40] == '0':
                label.append(-1)
            else:
                label.append(1)
    return num


def sign(a, b, n):
    res = 0
    for i in range(n):
        res += a[i] * b[i]
    if res > 0:
        return 1
    else:
        return -1


def change(w, x, y, learn_rat, n):
    for i in range(n):
        w[i] += learn_rat * y * x[i]
