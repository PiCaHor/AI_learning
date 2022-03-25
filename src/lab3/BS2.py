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
