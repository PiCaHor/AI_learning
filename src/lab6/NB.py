from function import init
from function import validation
from function import validation1
from function import test

Word = []
Label = []
Mood = set()
dictionary = set()
N = 0
p_ei_list = {}
n_ei_xk = {}
n_w_ei = {}
n_w_xk_ei = {}
v_ei = {}

if __name__ == '__main__':
    '''
    # train
    N = init(Word, Label, dictionary, Mood)
    Mood = list(Mood)
    dictionary = list(dictionary)
    for mood in Mood:
        p_ei_list[mood] = 0
    for label in Label:
        p_ei_list[label] = p_ei_list[label] + 1
    # 伯努利模型
    for mood in Mood:
        for diction in dictionary:
            n_ei_xk[(mood, diction)] = 0
            for i in range(N):
                if mood != Label[i]:
                    continue
                for word in Word[i]:
                    if word == diction:
                        n_ei_xk[(mood, diction)] = n_ei_xk[(mood, diction)] + 1
                        break
            # print(mood + " " + diction + ' ' + str(n_ei_xk[(mood, diction)])

    # 多项式模型
    for mood in Mood:
        n_w_ei[mood] = 0
        g = set()
        for i in range(N):
            if mood == Label[i]:
                n_w_ei[mood] = n_w_ei[mood] + len(Word[i])
                for word in Word[i]:
                    g.add(word)
                    if not (mood, word) in n_w_xk_ei:
                        n_w_xk_ei[(mood, word)] = 0
                    n_w_xk_ei[(mood, word)] = n_w_xk_ei[(mood, word)] + 1
        g = list(g)
        v_ei[mood] = len(g)

    # 测试合适的拉普拉斯平滑系数
    pr = 0.000001
    while pr != 0.00001:
        print(pr)

        res = validation(Mood, p_ei_list, n_ei_xk, N, dictionary, pr)
        print(res)

        res = validation1(Mood, p_ei_list, n_w_xk_ei, N, dictionary, n_w_ei, v_ei, pr)
        print(res)

        pr = pr + 0.000001
    '''
    # 运行测试集
    N = init(Word, Label, dictionary, Mood)
    Mood = list(Mood)
    dictionary = list(dictionary)

    for mood in Mood:
        p_ei_list[mood] = 0
    for label in Label:
        p_ei_list[label] = p_ei_list[label] + 1
    for mood in Mood:
        n_w_ei[mood] = 0
        g = set()
        for i in range(N):
            if mood == Label[i]:
                n_w_ei[mood] = n_w_ei[mood] + len(Word[i])
                for word in Word[i]:
                    g.add(word)
                    if not (mood, word) in n_w_xk_ei:
                        n_w_xk_ei[(mood, word)] = 0
                    n_w_xk_ei[(mood, word)] = n_w_xk_ei[(mood, word)] + 1
        g = list(g)
        v_ei[mood] = len(g)

    test(Mood, p_ei_list, n_w_xk_ei, N, dictionary, n_w_ei, v_ei, 0.000001)
