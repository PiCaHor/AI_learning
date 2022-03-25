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
