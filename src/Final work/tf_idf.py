import math
K = 2
dictionary = set()
Word = []
Label = []
tf = []
idf = {}

fw = open('./dataset/tf_idf.csv', 'w', encoding='utf-8', errors='ignore')


def init(Word, Label, dictionary):
    num = 0
    with open('./dataset/high_times.csv') as file_object:
        for line in file_object.readlines():
            line = line.strip()
            line = line.split(',')
            words = line[0].split(' ')
            g = []
            for word in words:
                if word == '':
                    continue
                g.append(word)
                dictionary.add(word)
            Word.append(g)
            Label.append(line[1])
            num = num + 1
    return num


if __name__ == '__main__':
    n = init(Word, Label, dictionary)
    dictionary = list(dictionary)
    print(len(dictionary))  # 2:9214  5 : 5550
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

    for i in range(n):
        for word in dictionary:
            fw.write(str(tf[i][word] * idf[word]) + ',')
        fw.write(Label[i] + '\n')

