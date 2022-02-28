from lab1 import init
from lab1 import Message

max_city_num = 50
max_dis = 99999
graph = []
city_num = 0
city_map = {}
city_remap = {}
city_name_map = {}
m = 0
n = 0

if __name__ == '__main__':
    graph = init(max_city_num, max_dis)
    fl = 0
    with open('./Romania.txt') as file_object:
        for lines in file_object.readlines():
            line = lines.split()
            if fl == 0:
                m = int(line[0])
                n = int(line[1])
                fl = 1
            else:
                value = int(line[2])
                if not city_map.__contains__(line[0][0]):
                    city_map[line[0][0]] = city_num
                    city_remap[city_num] = line[0][0]
                    city_name_map[line[0][0]] = line[0]
                    city_num = city_num + 1
                if not city_map.__contains__(line[1][0]):
                    city_map[line[1][0]] = city_num
                    city_remap[city_num] = line[1][0]
                    city_name_map[line[1][0]] = line[1]
                    city_num = city_num + 1
                graph[city_map[line[0][0]]][city_map[line[1][0]]] = value
                graph[city_map[line[1][0]]][city_map[line[0][0]]] = value
    print("input start and end with 0 0 to exit")
    while 1:
        message = input().split()
        start = message[0][0].upper()
        end = message[1][0].upper()
        if start + end == '00':
            break
        dis = [max_dis] * m
        pre = [i for i in range(m)]
        vis = [0] * m
        vis[city_map[start]] = 1
        dis[city_map[start]] = 0
        for i in range(m):
            if dis[i] > dis[city_map[start]] + graph[city_map[start]][i]:
                dis[i] = dis[city_map[start]] + graph[city_map[start]][i]
                pre[i] = city_map[start]
        # print(dis)
        while vis[city_map[end]] == 0:
            nxt = -1
            nxt_dis = max_dis
            for i in range(m):
                if vis[i] == 0 and dis[i] < nxt_dis:
                    nxt = i
                    nxt_dis = dis[i]
            vis[nxt] = 1
            for i in range(m):
                if vis[i] == 0 and dis[i] > dis[nxt] + graph[nxt][i]:
                    dis[i] = dis[nxt] + graph[nxt][i]
                    pre[i] = nxt
        print(dis[city_map[end]])
        tmp = city_map[end]
        step = city_name_map[end]
        while tmp != city_map[start]:
            step = city_name_map[city_remap[pre[tmp]]] + '->' + step
            tmp = pre[tmp]
        print(step)
        t = Message(dis[city_map[end]], step)
        t.add_Info(city_name_map[start], city_name_map[end])

