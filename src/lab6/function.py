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
    # 测试集添加
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


def laplacian_smoothing(a, b, d):
    return (a + d)/(b + 2)


def validation(Mood, p_ei_list, n_ei_xk, N, dictionary, la):
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

            ans = ''
            anst = 0
            for mood in Mood:
                tmp = p_ei_list[mood]/N
                for word in words:
                    if word in dictionary:
                        tmp = tmp * laplacian_smoothing(n_ei_xk[(mood, word)], p_ei_list[mood], la)
                    else:
                        tmp = tmp * laplacian_smoothing(0, p_ei_list[mood], la)
                if anst == 0:
                    ans = mood
                    anst = tmp
                elif tmp > anst:
                    ans = mood
                    anst = tmp

            if ans == line[1]:
                cur = cur + 1

    return cur/num


def laplacian_smoothing1(a, b, c, d):
    return (a + d)/(b + c)


def validation1(Mood, p_ei_list, n_w_xk_ei, N, dictionary, n_w_ei, v_ei, la):
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

            ans = ''
            anst = 0
            for mood in Mood:
                tmp = p_ei_list[mood] / N
                for word in words:
                    if (mood, word) in n_w_xk_ei:
                        tmp = tmp * laplacian_smoothing1(n_w_xk_ei[(mood, word)], n_w_ei[mood], v_ei[mood], la)
                    else:
                        tmp = tmp * laplacian_smoothing1(0, 0, v_ei[mood], la)
                if anst == 0:
                    ans = mood
                    anst = tmp
                elif tmp > anst:
                    ans = mood
                    anst = tmp

            if ans == line[1]:
                cur = cur + 1

        return cur / num


# 测试集部分
def test(Mood, p_ei_list, n_w_xk_ei, N, dictionary, n_w_ei, v_ei, pr):
    num = 0
    cur = 0
    fl = True
    stmp = ''
    with open('./result/20337228_pengchenhan_NB_classification.csv', 'w') as file_object1:
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
            ans = ''
            anst = 0
            for mood in Mood:
                tmp = p_ei_list[mood] / N
                for word in words:
                    if (mood, word) in n_w_xk_ei:
                        tmp = tmp * laplacian_smoothing1(n_w_xk_ei[(mood, word)], n_w_ei[mood], v_ei[mood], pr)
                    else:
                        tmp = tmp * laplacian_smoothing1(0, 0, v_ei[mood], pr)
                if anst == 0:
                    ans = mood
                    anst = tmp
                elif tmp > anst:
                    ans = mood
                    anst = tmp
            with open('./result/20337228_pengchenhan_NB_classification.csv', 'a') as file_object1:
                file_object1.write(stmp + ans + '\n')

