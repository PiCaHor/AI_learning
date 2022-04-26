from function import AI
from function import p_board
from function import GA

c_board = [[] for i in range(8)]

if __name__ == '__main__':
    ai = AI(8, -1)
    for i in range(8):
        for j in range(8):
            c_board[i].append(0)
    c_board[3][3] = 1
    c_board[4][4] = 1
    c_board[3][4] = -1
    c_board[4][3] = -1
    p_board(c_board)
    cnt = 0
    # # 人先下
    # while cnt<60:
    #     print('输入落子的地方:x,y')
    #     m = input()
    #     c_board = ai.find_change(c_board,-1,(int(m[0]),int(m[2])))
    #     p_board(c_board)
    #     tmp = [[] for i in range(8)]
    #     for i in range(8):
    #         for j in range(8):
    #             tmp[i].append(c_board[i][j])
    #     m = ai.go(tmp)
    #     print(m)
    #     c_board = ai.find_change(c_board, 1, m)
    #     p_board(c_board)
    #     cnt = cnt + 2
    # 机器先下
    while cnt<60:
        tmp = [[] for i in range(8)]
        for i in range(8):
            for j in range(8):
                tmp[i].append(c_board[i][j])
        m = ai.go(tmp)
        print(m)
        c_board = ai.find_change(c_board, -1, m)
        p_board(c_board)
        print('输入落子的地方:x,y')
        m = input()
        c_board = ai.find_change(c_board,1,(int(m[0]),int(m[2])))
        p_board(c_board)
        cnt = cnt + 2

    '''
    # train
    access = [[]for i in range(8)]
    for i in range(8):
        for j in range(8):
            access[i].append(0)
    ai_1 = AI(8,1)
    while True:
        while cnt<60:
            tmp = [[] for i in range(8)]
            for i in range(8):
                for j in range(8):
                    tmp[i].append(c_board[i][j])
            m = ai.go(tmp)
            print(m)
            c_board = ai.find_change(c_board, -1, m,access)
            p_board(c_board)
            
            tmp = [[] for i in range(8)]
            for i in range(8):
                for j in range(8):
                    tmp[i].append(c_board[i][j])
            m = ai.go(tmp)
            print(m)
            c_board = ai_1.find_change(c_board, 1, m,access)
            p_board(c_board)
            cnt = cnt + 2
        cnt = 0
        for i in range(8):
            for j in range(8):
                if c_board[i][j] == 'B':
                    cnt = cnt + 1
                else:
                    cnt = cnt - 1
        if cnt > 0:
            GA(access,0.6)
        else:
            GA(access,0.2)
    '''