import math

from FIOL_data import Message
from FIOL_data import Logic


def init(message_hub, name_hub):
    fl = 0
    cnt = 0
    with open('./test.txt') as file_object:
        for lines in file_object.readlines():
            line = lines.split()
            if fl == 0:
                n = int(line[0])
                fl = 1
                # print(n)
            else:
                line = line[0].split('(')
                relation = line[0]
                line = line[1].split(')')
                line = line[0].split(',')
                t = Message(line[0], relation, line[1])
                name_hub.append(line[0])
                name_hub.append(line[1])
                # print(cnt)
                # t.printf()
                if cnt == n:
                    return n, t
                else:
                    message_hub.append(t)
                cnt = cnt + 1


def classify(message_hub, question, p_example, n_example, relation_hub):
    p_cnt = 0
    n_cnt = 0
    for message in message_hub:
        t = Message(message.left(), question.relat(), message.right())
        if message.relat() == question.relat():
            p_example.append(t)
            p_cnt += 1
        else:
            n_example.append(t)
            n_cnt += 1
            relation_hub.append(message.relat())
    return [p_cnt, n_cnt]


def check_in(logic, x1, x2, x3, message_hub, t_mod):
    mod = logic.get_mod()
    x = ''
    y = ''
    z = ''
    if t_mod == 0:
        x = x1
        y = x2
        z = x3
    elif t_mod == 1:
        x = x2
        y = x1
        z = x3
    elif t_mod == 2:
        x = x1
        y = x3
        z = x2
    elif t_mod == 3:
        x = x2
        y = x3
        z = x1
    elif t_mod == 4:
        x = x3
        y = x1
        z = x2
    elif t_mod == 5:
        x = x3
        y = x2
        z = x1

    t = Message()
    if mod == 0:
        t = Message(x, logic.get_relate(), y)
    elif mod == 1:
        t = Message(y, logic.get_relate(), x)
    elif mod == 2:
        t = Message(x, logic.get_relate(), z)
    elif mod == 3:
        t = Message(z, logic.get_relate(), x)
    elif mod == 4:
        t = Message(y, logic.get_relate(), z)
    elif mod == 5:
        t = Message(z, logic.get_relate(), y)

    if not find(message_hub, t):
        return False
    else:
        return True


def find(message_hub, t, new=[]):
    fl = False
    for message in message_hub:
        if (t.left() == '' or message.left() == t.left()) and (t.right() == '' or message.right() == t.right()) and message.relat() == t.relat():
            new.append(message)
            fl = True
    return fl


def cal(relations, mod, p_example, n_example, message_hub, logic_hub, name_hub, question_relation):
    p_cnt = 0
    p_new = []
    n_cnt = 0
    n_new = []
    left = ''
    right = ''
    for name1 in name_hub:
        for name2 in name_hub:
            left = name1
            right = name2
            t = Message(left, relations, right)
            if not find(message_hub, t):
                continue
            t_name3 = ''
            name3 = ''
            mfl = True
            lfl = False
            for name3 in name_hub:
                if len(logic_hub) == 0:
                    mfl = False
                    break
                if lfl:
                    break
                for logic in logic_hub:
                    if check_in(logic, name1, name2, name3, message_hub, mod):
                        mfl = False
                        t_name3 = name3
                        lfl = True
                        break
            name3 = t_name3
            if mfl:
                continue
            if len(logic_hub) == 0:
                if mod == 0:
                    t = Message(name1, question_relation, name2)
                elif mod == 1:
                    t = Message(name2, question_relation, name1)
                elif mod == 2:
                    t = Message(name1, question_relation, '')
                elif mod == 3:
                    t = Message(name2, question_relation, '')
                elif mod == 4:
                    t = Message('', question_relation, name1)
                elif mod == 5:
                    t = Message('', question_relation, name2)
                if find(p_example, t):
                    p_cnt += 1
                    p_new.append(t)
                if find(n_example, t):
                    n_cnt += 1
                    n_new.append(t)
            else:
                if mod == 0:
                    t = Message(name1, question_relation, name2)
                elif mod == 1:
                    t = Message(name2, question_relation, name1)
                elif mod == 2:
                    t = Message(name1, question_relation, name3)
                elif mod == 3:
                    t = Message(name2, question_relation, name3)
                elif mod == 4:
                    t = Message(name3, question_relation, name1)
                elif mod == 5:
                    t = Message(name3, question_relation, name2)
                t_n = t
                if find(p_example, t, p_new):
                    p_cnt += 1
                if find(n_example, t_n, n_new):
                    n_cnt += 1
    return [p_cnt, n_cnt], [p_new, n_new]


def cal_gain(a, b):
    return math.log2(a / (a + b))


def mod_map(i):
    if i == 0:
        return '(x,y)'
    elif i == 1:
        return '(y,x)'
    elif i == 2:
        return '(x,z)'
    elif i == 3:
        return '(z,x)'
    elif i == 4:
        return '(y,z)'
    elif i == 5:
        return '(z,y)'


def check(logic_num, logic_hub, n, message_hub, step, used, various, question):
    if step == logic_num:
        t = Message(various[0], question.relat(), various[1])
        if not find(message_hub, t):
            print(question.relat() + "(" + various[0] + ',' + various[1] + ")")
        return
    for i in range(n):
        if used[i]:
            continue
        if message_hub[i].relat() == logic_hub[step].get_relate():
            mod = logic_hub[step].get_mod()
            if mod == 0:
                if various[0] != '' and various[1] != '' and various[0] == message_hub[i].left() and various[1] == \
                        message_hub[i].right():
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                elif various[0] == '' and various[1] != '' and various[1] == message_hub[i].right():
                    various[0] = message_hub[i].left()
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                    various[0] = ''
                elif various[0] != '' and various[1] == '' and various[0] == message_hub[i].left():
                    various[1] = message_hub[i].right()
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                    various[1] = ''
                elif various[0] == '' and various[1] == '':
                    various[0] = message_hub[i].left()
                    various[1] = message_hub[i].right()
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                    various[1] = ''
                    various[0] = ''
            elif mod == 1:
                if various[0] != '' and various[1] != '' and various[1] == message_hub[i].left() and various[0] == \
                        message_hub[i].right():
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                elif various[1] == '' and various[0] != '' and various[0] == message_hub[i].right():
                    various[1] = message_hub[i].left()
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                    various[1] = ''
                elif various[1] != '' and various[0] == '' and various[1] == message_hub[i].left():
                    various[0] = message_hub[i].right()
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                    various[0] = ''
                elif various[0] == '' and various[1] == '':
                    various[1] = message_hub[i].left()
                    various[0] = message_hub[i].right()
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                    various[1] = ''
                    various[0] = ''
            elif mod == 2:
                if various[0] != '' and various[2] != '' and various[0] == message_hub[i].left() and various[2] == \
                        message_hub[i].right():
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                elif various[0] == '' and various[2] != '' and various[2] == message_hub[i].right():
                    various[0] = message_hub[i].left()
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                    various[0] = ''
                elif various[0] != '' and various[2] == '' and various[0] == message_hub[i].left():
                    various[2] = message_hub[i].right()
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                    various[2] = ''
                elif various[0] == '' and various[2] == '':
                    various[0] = message_hub[i].left()
                    various[2] = message_hub[i].right()
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                    various[2] = ''
                    various[0] = ''
            elif mod == 3:
                if various[0] != '' and various[2] != '' and various[2] == message_hub[i].left() and various[0] == \
                        message_hub[i].right():
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                elif various[2] == '' and various[0] != '' and various[0] == message_hub[i].right():
                    various[2] = message_hub[i].left()
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                    various[2] = ''
                elif various[0] != '' and various[2] == '' and various[2] == message_hub[i].left():
                    various[0] = message_hub[i].right()
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                    various[0] = ''
                elif various[0] == '' and various[2] == '':
                    various[2] = message_hub[i].left()
                    various[0] = message_hub[i].right()
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                    various[2] = ''
                    various[0] = ''
            elif mod == 4:
                if various[1] != '' and various[2] != '' and various[1] == message_hub[i].left() and various[2] == \
                        message_hub[i].right():
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                elif various[1] == '' and various[2] != '' and various[2] == message_hub[i].right():
                    various[1] = message_hub[i].left()
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                    various[1] = ''
                elif various[1] != '' and various[2] == '' and various[1] == message_hub[i].left():
                    various[2] = message_hub[i].right()
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                    various[2] = ''
                elif various[1] == '' and various[2] == '':
                    various[1] = message_hub[i].left()
                    various[2] = message_hub[i].right()
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                    various[1] = ''
                    various[2] = ''
            elif mod == 5:
                if various[1] != '' and various[2] != '' and various[2] == message_hub[i].left() and various[1] == \
                        message_hub[i].right():
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                elif various[2] == '' and various[1] != '' and various[1] == message_hub[i].right():
                    various[2] = message_hub[i].left()
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                    various[2] = ''
                elif various[2] != '' and various[1] == '' and various[2] == message_hub[i].left():
                    various[1] = message_hub[i].right()
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                    various[1] = ''
                elif various[1] == '' and various[2] == '':
                    various[2] = message_hub[i].left()
                    various[1] = message_hub[i].right()
                    used[i] = 1
                    check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                    used[i] = 0
                    various[1] = ''
                    various[2] = ''


def find_l(logic_hub, l):
    for logic in logic_hub:
        if logic.get_relate() == l.get_relate() and logic.get_mod() == l.get_mod():
            return True
    return False
