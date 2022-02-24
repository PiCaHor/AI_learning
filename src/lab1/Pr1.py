max_dis = 99999

print('input m and n')
message = input().split()
m = int(message[0])
n = int(message[1])
graph = [[] for i in range(m)]
for i in range(m):
    for j in range(m):
        if i == j:
            graph[i].append(0)
        else:
            graph[i].append(max_dis)
# print(graph)

city_num = 0
city_map = {}
city_remap = {}
print("input start, end and value")
for i in range(n):
    message = input().split()
    start = message[0]
    end = message[1]
    value = int(message[2])
    if not city_map.__contains__(start):
        city_map[start] = city_num
        city_remap[city_num] = start
        city_num = city_num + 1
    if not city_map.__contains__(end):
        city_map[end] = city_num
        city_remap[city_num] = end
        city_num = city_num + 1
    graph[city_map[start]][city_map[end]] = value
    graph[city_map[end]][city_map[start]] = value
# print(graph)


print("input start and end with 0 0 to exit")
while 1:
    dis = [max_dis]*m
    pre = [i for i in range(m)]
    vis = [0] * m
    message = input().split()
    start = message[0]
    end = message[1]
    if start + end == '00':
        break
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
        # print(nxt)
        vis[nxt] = 1
        for i in range(m):
            if dis[i] > dis[nxt] + graph[nxt][i]:
                dis[i] = dis[nxt] + graph[nxt][i]
                pre[i] = nxt

    print(dis[city_map[end]])

    tmp = city_map[end]
    step = end
    while tmp != city_map[start]:
        step = city_remap[pre[tmp]] + '->' + step
        tmp = pre[tmp]
    print(step)

'''
test data1 
6 8
a b 2
a c 3
b d 5
b e 2
c e 5
d e 1
d z 2
e z 4
a z
'''
