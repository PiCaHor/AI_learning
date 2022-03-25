lab3实验

这里是BFS部分

```python
def init(start, end, graph):
    with open('./MazeData.txt') as file_object:
        line = 0
        for lines in file_object.readlines():
            g = []
            for i in range(36):
                g.append(lines[i])
                if lines[i] == 'S':
                    start.append(line)
                    start.append(i)
                if lines[i] == 'E':
                    end.append(line)
                    end.append(i)
            line += 1
            graph.append(g)
    return

```

```python
from BS_function import init

graph = []
# 18*36
start = []
end = []
vis = []
q = []
path = []
dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]

if __name__ == '__main__':
    init(start, end, graph)
    for i in range(18):
        g = []
        p = []
        for j in range(36):
            p.append([0, 0])
            g.append(0)
        vis.append(g)
        path.append(p)
    vis[start[0]][start[1]] = 1
    vis[end[0]][end[1]] = -1

    q.append(start)
    while vis[end[0]][end[1]] == -1:
        t = q[0]
        del q[0]
        for i in range(4):
            tx = t[0] + dx[i]
            ty = t[1] + dy[i]
            if tx < 0 or tx > 17 or ty < 0 or ty > 35:
                continue
            if (vis[tx][ty] == 0 and graph[tx][ty] == '0') or graph[tx][ty] == 'E':
                path[tx][ty] = t
                vis[tx][ty] = vis[t[0]][t[1]] + 1
                q.append([tx, ty])

    px = end[0]
    py = end[1]
    while True:
        qx = path[px][py][0]
        qy = path[px][py][1]
        if qx == start[0] and qy == start[1]:
            break
        graph[qx][qy] = '2'
        px = qx
        py = qy
    with open('./out_graph.txt', 'w') as file_object:
        for i in range(18):
            g = ''
            for j in range(36):
                g += graph[i][j]
            g += '\n'
            file_object.write(g)

```

output:

```txt
111111111111111111111111111111111111
1000000000000000000000000222222222S1
101111111111111111111111121111111101
101100010001000000111111122211000001
101101010101011110111111111211011111
101101010101000000002222211211000001
101101010101010111102111222211111101
101001010100010000112111111110000001
101101010111111110112222222211011111
101101000110000000111111111211000001
100001111110111111100000011211111101
111111000000100000001111011210000001
100000011111101111101000011211011111
101111110000001000000011111211000001
100000000111111011111111111211001101
111111111122222222222222222211111101
1E2222222221111111111111111000000001
111111111111111111111111111111111111

```

迭代加深算法

```python
from BS_function import init
from BS_function import dfs
graph = []
# 18*36
start = []
end = []
vis = []
q = []
path = []
dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]

if __name__ == '__main__':
    init(start, end, graph)
    for i in range(18):
        g = []
        p = []
        for j in range(36):
            p.append([0, 0])
            g.append(0)
        vis.append(g)
        path.append(p)
    vis[start[0]][start[1]] = 1
    vis[end[0]][end[1]] = -1

    fl = True
    limit = 1
    while fl:
        dep = 1
        fl = dfs(start, limit, graph, vis, path, dep, dx, dy)
        limit += 1

    px = end[0]
    py = end[1]
    while True:
        qx = path[px][py][0]
        qy = path[px][py][1]
        if qx == start[0] and qy == start[1]:
            break
        graph[qx][qy] = '2'
        px = qx
        py = qy
    with open('./out_graph1.txt', 'w') as file_object:
        for i in range(18):
            g = ''
            for j in range(36):
                g += graph[i][j]
            g += '\n'
            file_object.write(g)

```

函数文件：

``` python
def init(start, end, graph):
    with open('./MazeData.txt') as file_object:
        line = 0
        for lines in file_object.readlines():
            g = []
            for i in range(36):
                g.append(lines[i])
                if lines[i] == 'S':
                    start.append(line)
                    start.append(i)
                if lines[i] == 'E':
                    end.append(line)
                    end.append(i)
            line += 1
            graph.append(g)
    return


def dfs(now, limit, graph, vis, path, dep, dx, dy):
    if dep > limit:
        return True
    if graph[now[0]][now[1]] == 'E':
        return False
    for i in range(4):
        tx = now[0] + dx[i]
        ty = now[1] + dy[i]
        if tx < 0 or tx > 17 or ty < 0 or ty > 35:
            continue
        if graph[tx][ty] == 'E' or (vis[tx][ty] == 0 and graph[tx][ty] == '0'):
            path[tx][ty] = now
            vis[tx][ty] = vis[now[0]][now[1]] + 1
            if not dfs([tx, ty], limit, graph, vis, path, dep + 1, dx, dy):
                return False
            vis[tx][ty] = 0
    return True

```

结果

``` txt
111111111111111111111111111111111111
1000000000000000000000000222222222S1
101111111111111111111111121111111101
101100010001000000111111122211000001
101101010101011110111111111211011111
101101010101000000002222211211000001
101101010101010111102111222211111101
101001010100010000112111111110000001
101101010111111110112222222211011111
101101000110000000111111111211000001
100001111110111111100000011211111101
111111000000100000001111011210000001
100000011111101111101000011211011111
101111110000001000000011111211000001
100000000111111011111111111211001101
111111111122222222222222222211111101
1E2222222221111111111111111000000001
111111111111111111111111111111111111
```

