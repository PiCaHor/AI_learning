lab4实验

代码主程序：

```python
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

    with open('./out_put.txt', 'w') as file_object:
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

```

函数实现部分

```python
dx = [0, 1, -1, 0]
dy = [1, 0, 0, -1]
limit = 50


def init(graph):
    with open('test1.txt') as file_object:
        for line in file_object.readlines():
            g = []
            line = line.split(' ')
            for i in range(4):
                n = int(line[i])
                g.append(n)
            graph.append(g)
    return


def h(graph, target):
    cost = 0
    for i in range(4):
        for j in range(4):
            num = graph[i][j]
            x, y = target[num]
            cost += abs(x - i) + abs(y - j)
    return cost


def is_goal(node):
    index = 1
    for row in node:
        for col in row:
            if index != col:
                break
            index += 1
    return index == 16


def successors(node, target):
    x, y = 0, 0
    for i in range(4):
        for j in range(4):
            if node[i][j] == 0:
                x, y = i, j
    success = []
    for i in range(4):
        a = x + dx[i]
        b = y + dy[i]
        if -1 < a < 4 and -1 < b < 4:
            temp = [[num for num in col] for col in node]
            temp[x][y] = temp[a][b]
            temp[a][b] = 0
            success.append(temp)

    return sorted(success, key=lambda xx: h(xx, target))


def search(path, g, bound, target):
    node = path[-1]
    f = g + h(node, target)
    if f > bound:
        return f
    if is_goal(node):
        return -1

    Min = 9999
    for succ in successors(node, target):
        if succ not in path:
            path.append(succ)
            t = search(path, g + 1, bound, target)
            if t == -1:
                return -1
            if t < Min:
                Min = t
            path.pop()
    return Min


def IDAstar(graph, target):
    bound = h(graph, target)
    path = [graph]
    while True:
        t = search(path, 0, bound, target)
        if t == -1:
            return path
        if t > limit:
            return []
        bound = t

```

测试样例一：

```txt
1 2 4 8
5 7 11 10
13 15 0 3
14 6 9 12

```

output:

```txt
step: 1
[1, 2, 4, 8]
[5, 7, 11, 10]
[13, 15, 0, 3]
[14, 6, 9, 12]
step: 2
[1, 2, 4, 8]
[5, 7, 11, 10]
[13, 15, 3, 0]
[14, 6, 9, 12]
step: 3
[1, 2, 4, 8]
[5, 7, 11, 0]
[13, 15, 3, 10]
[14, 6, 9, 12]
step: 4
[1, 2, 4, 8]
[5, 7, 0, 11]
[13, 15, 3, 10]
[14, 6, 9, 12]
step: 5
[1, 2, 4, 8]
[5, 7, 3, 11]
[13, 15, 0, 10]
[14, 6, 9, 12]
step: 6
[1, 2, 4, 8]
[5, 7, 3, 11]
[13, 0, 15, 10]
[14, 6, 9, 12]
step: 7
[1, 2, 4, 8]
[5, 7, 3, 11]
[13, 6, 15, 10]
[14, 0, 9, 12]
step: 8
[1, 2, 4, 8]
[5, 7, 3, 11]
[13, 6, 15, 10]
[14, 9, 0, 12]
step: 9
[1, 2, 4, 8]
[5, 7, 3, 11]
[13, 6, 0, 10]
[14, 9, 15, 12]
step: 10
[1, 2, 4, 8]
[5, 7, 3, 11]
[13, 6, 10, 0]
[14, 9, 15, 12]
step: 11
[1, 2, 4, 8]
[5, 7, 3, 0]
[13, 6, 10, 11]
[14, 9, 15, 12]
step: 12
[1, 2, 4, 0]
[5, 7, 3, 8]
[13, 6, 10, 11]
[14, 9, 15, 12]
step: 13
[1, 2, 0, 4]
[5, 7, 3, 8]
[13, 6, 10, 11]
[14, 9, 15, 12]
step: 14
[1, 2, 3, 4]
[5, 7, 0, 8]
[13, 6, 10, 11]
[14, 9, 15, 12]
step: 15
[1, 2, 3, 4]
[5, 0, 7, 8]
[13, 6, 10, 11]
[14, 9, 15, 12]
step: 16
[1, 2, 3, 4]
[5, 6, 7, 8]
[13, 0, 10, 11]
[14, 9, 15, 12]
step: 17
[1, 2, 3, 4]
[5, 6, 7, 8]
[13, 9, 10, 11]
[14, 0, 15, 12]
step: 18
[1, 2, 3, 4]
[5, 6, 7, 8]
[13, 9, 10, 11]
[0, 14, 15, 12]
step: 19
[1, 2, 3, 4]
[5, 6, 7, 8]
[0, 9, 10, 11]
[13, 14, 15, 12]
step: 20
[1, 2, 3, 4]
[5, 6, 7, 8]
[9, 0, 10, 11]
[13, 14, 15, 12]
step: 21
[1, 2, 3, 4]
[5, 6, 7, 8]
[9, 10, 0, 11]
[13, 14, 15, 12]
step: 22
[1, 2, 3, 4]
[5, 6, 7, 8]
[9, 10, 11, 0]
[13, 14, 15, 12]
step: 23
[1, 2, 3, 4]
[5, 6, 7, 8]
[9, 10, 11, 12]
[13, 14, 15, 0]

Total step: 23

```

测试样例二：

```txt
5 1 3 4
2 7 8 12
9 6 11 15
0 13 10 14

```

output:

```txt
step: 1
[5, 1, 3, 4]
[2, 7, 8, 12]
[9, 6, 11, 15]
[0, 13, 10, 14]
step: 2
[5, 1, 3, 4]
[2, 7, 8, 12]
[9, 6, 11, 15]
[13, 0, 10, 14]
step: 3
[5, 1, 3, 4]
[2, 7, 8, 12]
[9, 6, 11, 15]
[13, 10, 0, 14]
step: 4
[5, 1, 3, 4]
[2, 7, 8, 12]
[9, 6, 11, 15]
[13, 10, 14, 0]
step: 5
[5, 1, 3, 4]
[2, 7, 8, 12]
[9, 6, 11, 0]
[13, 10, 14, 15]
step: 6
[5, 1, 3, 4]
[2, 7, 8, 0]
[9, 6, 11, 12]
[13, 10, 14, 15]
step: 7
[5, 1, 3, 4]
[2, 7, 0, 8]
[9, 6, 11, 12]
[13, 10, 14, 15]
step: 8
[5, 1, 3, 4]
[2, 0, 7, 8]
[9, 6, 11, 12]
[13, 10, 14, 15]
step: 9
[5, 1, 3, 4]
[0, 2, 7, 8]
[9, 6, 11, 12]
[13, 10, 14, 15]
step: 10
[0, 1, 3, 4]
[5, 2, 7, 8]
[9, 6, 11, 12]
[13, 10, 14, 15]
step: 11
[1, 0, 3, 4]
[5, 2, 7, 8]
[9, 6, 11, 12]
[13, 10, 14, 15]
step: 12
[1, 2, 3, 4]
[5, 0, 7, 8]
[9, 6, 11, 12]
[13, 10, 14, 15]
step: 13
[1, 2, 3, 4]
[5, 6, 7, 8]
[9, 0, 11, 12]
[13, 10, 14, 15]
step: 14
[1, 2, 3, 4]
[5, 6, 7, 8]
[9, 10, 11, 12]
[13, 0, 14, 15]
step: 15
[1, 2, 3, 4]
[5, 6, 7, 8]
[9, 10, 11, 12]
[13, 14, 0, 15]
step: 16
[1, 2, 3, 4]
[5, 6, 7, 8]
[9, 10, 11, 12]
[13, 14, 15, 0]

Total step: 16

```

测试样例三

```txt
14 10 6 0
4 9 1 8
2 3 5 11
12 13 7 15

```

output:

```txt
step: 1
[14, 10, 6, 0]
[4, 9, 1, 8]
[2, 3, 5, 11]
[12, 13, 7, 15]
step: 2
[14, 10, 0, 6]
[4, 9, 1, 8]
[2, 3, 5, 11]
[12, 13, 7, 15]
step: 3
[14, 0, 10, 6]
[4, 9, 1, 8]
[2, 3, 5, 11]
[12, 13, 7, 15]
...
step: 48
[1, 2, 3, 4]
[5, 6, 7, 8]
[9, 10, 0, 12]
[13, 14, 11, 15]
step: 49
[1, 2, 3, 4]
[5, 6, 7, 8]
[9, 10, 11, 12]
[13, 14, 0, 15]
step: 50
[1, 2, 3, 4]
[5, 6, 7, 8]
[9, 10, 11, 12]
[13, 14, 15, 0]

Total step: 50
```

测试样例四：

```txt
6 10 3 15
14 8 7 11
5 1 0 2
13 12 9 4
```

output:

```txt
step: 1
[6, 10, 3, 15]
[14, 8, 7, 11]
[5, 1, 0, 2]
[13, 12, 9, 4]
step: 2
[6, 10, 3, 15]
[14, 8, 7, 11]
[5, 1, 2, 0]
[13, 12, 9, 4]
step: 3
[6, 10, 3, 15]
[14, 8, 7, 0]
[5, 1, 2, 11]
[13, 12, 9, 4]

step: 49
[1, 2, 3, 4]
[5, 6, 7, 8]
[9, 10, 0, 11]
[13, 14, 15, 12]
step: 50
[1, 2, 3, 4]
[5, 6, 7, 8]
[9, 10, 11, 0]
[13, 14, 15, 12]
step: 51
[1, 2, 3, 4]
[5, 6, 7, 8]
[9, 10, 11, 12]
[13, 14, 15, 0]

Total step: 51

```

