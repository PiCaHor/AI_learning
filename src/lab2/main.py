from FIOL_data import Message
from FIOL_data import Logic
from function import init
from function import classify
from function import cal
from function import cal_gain
from function import mod_map
from function import check
from function import find_l

relation_hub = []
message_hub = []
name_hub = []
question = Message()
p_example = []
n_example = []
p_cnt = 0
n_cnt = 0
logic_hub = []
logic_num = 0

if __name__ == '__main__':
    m_cnt, question = init(message_hub, name_hub)
    # question.printf()
    t = classify(message_hub, question, p_example, n_example, relation_hub)
    relation_hub = list(set(relation_hub))
    name_hub = list(set(name_hub))
    name_hub.remove('x')
    name_hub.remove('y')
    name_hub.sort()
    tmp = name_hub[1]
    name_hub[1] = name_hub[3]
    name_hub[3] = tmp
    p_cnt = t[0]
    n_cnt = t[1]
    fl = True
    output_message = "-> " + question.relat() + '(' + question.left() + "," + question.right() + ")"
    while fl:
        FOIL_Gain = 0
        FOIL_relation = ""
        FOIL_mode = 0
        FOIL_cnt = [0, 0]
        FOIL_t_new = []

        for relations in relation_hub:
            if relations == question.relat():
                continue
            for i in range(6):
                m = Logic(relations, i)
                if find_l(logic_hub, m):
                    continue
                p_used = [1] * p_cnt
                n_used = [1] * n_cnt
                t, t_new = cal(relations, i, p_example, n_example, message_hub, logic_hub, name_hub, question.relat())
                # print(relations)
                # print(t)
                # m = input()
                if t[0] != 0:
                    tmp = t[0] * (cal_gain(t[0], t[1]) - cal_gain(p_cnt, n_cnt))
                    if tmp >= FOIL_Gain:
                        FOIL_Gain = tmp
                        FOIL_relation = relations
                        FOIL_mode = i
                        FOIL_cnt = t
                        FOIL_t_new = t_new
        if output_message[0] == '-':
            output_message = FOIL_relation + mod_map(FOIL_mode) + output_message
        else:
            output_message = FOIL_relation + mod_map(FOIL_mode) + ' V ' + output_message
        # print(output_message)
        m = Logic(FOIL_relation, FOIL_mode)
        logic_hub.append(m)
        logic_num += 1
        p_cnt = FOIL_cnt[0]
        n_cnt = FOIL_cnt[1]
        if FOIL_cnt[1] == 0:
            fl = False
        if n_cnt != 0:
            n_example = FOIL_t_new[1]
        # p_example[0].printf()
        # print(n_cnt)
    print(output_message)
    used = [0] * m_cnt
    various = ['', '', '']
    check(logic_num, logic_hub, m_cnt, message_hub, 0, used, various, question)
