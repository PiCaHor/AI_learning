"""
该部分用于数据清理
目前功能： 去除字符，规整格式
形如 I’ve 形式的 变成 Ive单词
结果保存至 tidy_train.csv

停用词除去
低频词除去-低于2的去除
全部保存成小写
结果保存至 high_time.csv
"""

stopwords = ['a', 'in','to']
fw = open('./dataset/tidy_test.csv', 'w', encoding='utf-8')
fw1 = open('./dataset/final.csv', 'w', encoding='utf-8')
cnt = {}
if __name__ == '__main__':
    fl = True

    with open('./dataset/test.csv', encoding='utf-8') as file_object:
        for line in file_object.readlines():
            if fl:
                fl = False
                continue
            constr = ''
            line = line.split(',')
            fw.write(line[0] + ',')
            word = ''
            for i in range(len(line)):
                if i == 0:
                    continue
                word += line[i]
            constr = ''
            for uchar in word:
                if 'a' <= uchar <= 'z' or 'A' <= uchar <= 'Z' or uchar == ' ':
                    constr += uchar.lower()
            fw.write(constr + '\n')
    fw.close()
    with open('./dataset/tidy_test.csv', encoding='utf-8') as file_object:
        for line in file_object.readlines():
            line = line.split(',')
            line[1] = line[1].strip()
            words = line[1].split(' ')
            for word in words:
                if word in cnt:
                    cnt[word] += 1
                else:
                    cnt[word] = 1
    with open('./dataset/tidy_test.csv', encoding='utf-8') as file_object:
        for line in file_object.readlines():
            line = line.split(',')
            line[1] = line[1].strip()
            words = line[1].split(' ')
            for word in words:
                # if word != '' and cnt[word] > 5 and (word not in stopwords.words('english')):
                if word != '' and cnt[word] > 10 and (word not in stopwords):
                    fw1.write(word + ' ')
            # fw1.write(',' + line[0] + '\n')
            fw1.write('\n')
    fw1.close()


