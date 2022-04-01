dx = [0, 1, -1, 0]
dy = [1, 0, 0, -1]
limit = 100


def init(graph):
    with open('test4.txt') as file_object:
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
