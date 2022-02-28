# 中山大学计算机学院人工智能实验报告

| 班级 | 冯诺依曼实验班 | 专业 | 计算机科学（系统结构) |
| :--- | -------------- | ---- | --------------------- |
| 学号 | 20337228       | 姓名 | 彭晨晗                |

### 0. 代码提交目录

|文件|说明|
|:---|----|
|lab1.py|封装的类和函数|
|lab_main.py|第一次实验的主程序入口|
|Lesson 1.py|测试与实验文件，包括思考题和上课练习|
|Pr1.py|第一周实验代码|
|log.txt|日志输出文件|
### 1. 实验题目

​	 最短路径搜索

### 2. 实验内容

1. 算法原理

   算法采用Dijstra算法，算法基本流程如下，所有的点分为两个集合，其中一个为已经确定最短路的点集S1，另一个为不确定S2，设一个dis数组为当前状态下到达各个点的最短距离。 初始时只有起始点在S1中，并通过起始点更新dis数组，接下来是循环一下步骤，直至找到终点最短路

   	1. 在dis数组中找到最小的S2集合的点k
   	1. 将k移入S1
   	1. 通过k更新dis数组

2. 伪代码

```
初始化与建图
输入
将start加入S1中
for 所有的点集 
  if graph[start][i] 存在路径
  	更新dis[i]
 while end不在S1中
 	for S2
 		更新最短路径点k
 	将k加入S1
 	for 所有点集 
 		if dis[i] < 通过k到i
 			更新dis
 
 输出
```

3. 关键代码展示
   1. 算法实现
``` python
# start 加入S1并更新距离        
vis[city_map[start]] = 1
dis[city_map[start]] = 0
for i in range(m):
	if dis[i] > dis[city_map[start]] + graph[city_map[start]][i]:
    	dis[i] = dis[city_map[start]] + graph[city_map[start]][i]
        pre[i] = city_map[start]
        
# 循环end未找到
while vis[city_map[end]] == 0:
    # 找到最短路径的点k
    nxt = -1
    nxt_dis = max_dis
    for i in range(m):
        if vis[i] == 0 and dis[i] < nxt_dis:
            nxt = i
            nxt_dis = dis[i]
     # 将新点加入S1
    vis[nxt] = 1
    # 更新距离
    for i in range(m):
        if vis[i] == 0 and dis[i] > dis[nxt] + graph[nxt][i]:
            dis[i] = dis[nxt] + graph[nxt][i]
            pre[i] = nxt
```

​            2.答案输出及日志记载

```python
        # 输出距离
    	print(dis[city_map[end]])
        # 回溯寻找路径
        tmp = city_map[end]
        step = city_name_map[end]
        while tmp != city_map[start]:
            step = city_name_map[city_remap[pre[tmp]]] + '->' + step
            tmp = pre[tmp]
        print(step)
        # 写日志
        t = Message(dis[city_map[end]], step)
        t.add_Info(city_name_map[start], city_name_map[end])
```

​			3.建图

```python
    with open('./Romania.txt') as file_object:
        for lines in file_object.readlines():
            line = lines.split()
            if fl == 0:
                m = int(line[0])
                n = int(line[1])
                fl = 1
            else:
                value = int(line[2])
                # 建立城市名字和数字之间的映射，建立首字母与原城市名字的映射
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
                # 更新距离
                graph[city_map[line[0][0]]][city_map[line[1][0]]] = value
                graph[city_map[line[1][0]]][city_map[line[0][0]]] = value
```

​			4.类与函数引用

```python
from lab1 import init
from lab1 import Message

# 打印方法类
class Message:
    def __init__(self, dis, path):
        self.dis = dis
        self.path = path

    def add_Info(self, start, end):
        with open('./log.txt', 'a') as file_object:
            file_object.write('Query node from ' + start + ' to ' + end + '\n')
            file_object.write('Distance is ' + str(self.dis) + '\n')
            file_object.write('Path is ' + self.path + '\n\n')

# 初始化函数
def init(m, max_dis):
    t = [[] for i in range(m)]
    for i in range(m):
        for j in range(m):
            if i == j:
                t[i].append(0)
            else:
                t[i].append(max_dis)
    return t
```



### 3. 实验结果及分析

​    1.实验命令行结果图片

​	![1646009624(1)](F:\Code\AI_learning\img\1646009624(1).png)

2. 日志打印

![1646009728(1)](F:\Code\AI_learning\img\1646009728(1).png)

#### 结果分析：

##### 地图全貌：

![1646009937(1)](F:\Code\AI_learning\img\1646009937(1).png)

通过输入（无论全称还是首字母，不区分大小写）上述城市的最短路和路径符合答案。



##### 评测指标展示与分析：

算法没有做特别多的优化，运行速度没有出现比较慢的情况。 



### 4.思考题

1. 列表不能作为字典的键，因为这个会产生一个不确定的映射，等于是说，列表的键是不确定的，多维映射单个。而元组能解决这个问题，产生一个高维内容的映射。

2. 列表和字典是可变类型，但是字典中的key值必须是不可变类型

   整型，字符串，布尔类型，元组都是不可变类型

```python
a = 1
print(id(a), type(a))
a = 2
print(id(a), type(a))
a = "aaa"
print(id(a), type(a))
a = 'bbb'
print(id(a), type(a))
b = [1, 2, 3]
a = (1, 2, b)
print(id(a), type(a))
b[1] = 'aaa'
print(id(a), type(a))
a = [1, 2, 3]
print(id(a), type(a))
a.append(4)
print(id(a), type(a))
a = {1:2}
print(id(a), type(a))
a[3] = 4
print(id(a), type(a))

```

结果：

![1646011052(1)](F:\Code\AI_learning\img\1646011052(1).png)

Tips:

所有源码与截图已经上传到github仓库：

[仓库地址](https://github.com/PiCaHor/AI_learning)