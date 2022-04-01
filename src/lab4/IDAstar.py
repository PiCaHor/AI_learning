from function import init
from function import IDAstar

graph = []
sx = 0
sy = 0
target = {}
num = 1

if __name__ == '__main__':
    init(graph)
    # print(sx, sy, graph)
    for i in range(4):
        for j in range(4):
            target[num] = (i, j)
            num += 1
    target[0] = (3, 3)

    path = IDAstar(graph, target)

    with open('./out_put4.txt', 'w') as file_object:
        step = 1
        for p in path:
            file_object.write('step: ' + str(step) + '\n')
            step += 1
            for row in p:
                file_object.write(str(row))
                file_object.write('\n')

        file_object.write('\nTotal step: ' + str(step-1) + '\n')
'''
    step = 1
    for p in path:
        print('step', step)
        step += 1
        for row in p:
            print(str(row))
    print('\nTotal step ', step-1)
'''

