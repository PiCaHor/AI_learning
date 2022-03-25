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
