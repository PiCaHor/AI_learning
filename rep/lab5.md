# 中山大学计算机学院人工智能实验报告

| 班级 | 冯诺依曼实验班 | 专业 | 计算机科学（系统结构) |
| :--- | -------------- | ---- | --------------------- |
| 学号 | 20337228       | 姓名 | 彭晨晗                |

### 0. 代码提交目录

|文件|说明|
|:---|----|
|function.py|封装的类和函数|
|main.py|主程序入口|

### 1. 实验题目

​	 五子棋博弈树

### 2. 实验内容

1. 算法原理

   ​	采用minmax加alphy-beta剪枝，对于一方而言是寻求最大值的结局而另一方就是最小值的结局从而进行搜索，由于深度问题，需要构建估价函数代替叶节点。 

2. 关键代码展示

   |函数|说明|
   |:---|----|
   |search|搜索主程序|
   |find_change|根据函数改变棋盘|
   |find_choice|预处理可以下子的位置|
   |assess|估值函数|
   |GA|遗传函数去找估值函数|

   1. 剪枝部分
``` python
                choice = self.find_choice(board,color)
                if len(choice)!=0:
                    a = -99999
                    b = 0
                    # 枚举可行解
                    for i in range(0,len(choice)):
                        newboard = self.find_change(board,color,choice[i])
                        # 递归
                        n = self.search(-color,newboard,deep+1,alpha,beta,t)
                        if n is not None:
                            if n>a:
                                a = n
                                b = i
                            # 剪枝部分
                            if a>=beta:
                                if deep==1:
                                    return choice[i]
                                return a
                            alpha = max(alpha,a)
                    if deep==1:
                        return choice[b]
                    return a
```

​            2.预处理可以落子的位置

```python
                if chessboard[i][j] == 0:
                    if i > 1 and chessboard[i - 1][j] == -color and ij == 0: 
                        i_temp = i - 2
                        while i_temp >= 0:
                            if chessboard[i_temp][j] == 0:
                                break
                            if chessboard[i_temp][j] == color:
                                choice.append((i, j))
                                ij = 1
                                break
                            i_temp = i_temp - 1
```

​			3.更改部分

```python
            if x > 1 and chessboard[x - 1][y] == -color:  # 向上
                x_temp = x - 2
                while x_temp >= 0:
                    if chessboard[x_temp][y] == 0:
                        break
                    if chessboard[x_temp][y] == color:
                        while x_temp<x:
                            x_temp = x_temp + 1
                            change[x_temp][y]=color
                        break
                    x_temp = x_temp - 1
```

​			4.估价函数

​	估价函数比较复杂，这个是函数计算的部分，根据一些技巧的显示，估价函数需要考虑已经落子的权和可以落子数目的权，可以落子数目的权在搜索函数部分返回值中给出

​	估值数组需要根据金角银边草肚皮的原则和对称性

​    同时角旁边的点的权值会因为角是否被占而产生变化

```python
        sum = 0
        for i in range(0,8):
            for j in range(0,8):
              sum = sum + assess[i][j]*board[i][j]
        if self.color==-1:
            sum = -sum
        return sum
```

​	5.GA	

​	效果一般，这里把遗传和编译合在一起，增加一个遗传率表示不同结果的影响。如果黑方能胜，说明基因很好，那么遗传率会比较大，然后通过随机数完成变异的过程

```python
def GA(assess,Len_rate):    
    Max = [[]for i in range(8)]
    for i in range(8):
        for j in range(8):
            Max[i].append(9999)

    Min = [[]for i in range(8)]
    for i in range(8):
        for j in range(8):
            Min[i].append(-9999)
    # random.random()
    for i in range(8):
        for j in range(8):
            assess[i][j] = assess[i][j]*Len_rate + (1-Len_rate)*(Max[i][j]*random.random() + Min[i][j]*random.random())
```



### 3. 实验结果及分析

​    和某个小程序最高难度下了一下，结果险胜，解给出的答案速度比较快，搜索深度为8

​    1.结果

    ```txt
    输入落子的地方:x,y
    3 7
    W W W W W W W W 
    B B W W W W E E 
    E B B B B B W E 
    W B W W W W E W 
    W W W W W E E E 
    W B E E E E E E 
    E E E E E E E E 
    E E E E E E E E 
    
    (1, 6)
    W W W W W W W W 
    B B B B B B B E 
    E B B B B B W E 
    W B W W W W E W 
    W W W W W E E E 
    W B E E E E E E 
    E E E E E E E E 
    E E E E E E E E 
    
    输入落子的地方:x,y
    5 2
    W W W W W W W W 
    B B B B B B B E 
    E B B B B B W E 
    W B W W W W E W 
    W W W W W E E E 
    W W W E E E E E 
    E E E E E E E E 
    E E E E E E E E 
    
    (2, 7)
    W W W W W W W W 
    B B B B B B B E 
    E B B B B B B B 
    W B W W W W E W 
    W W W W W E E E 
    W W W E E E E E 
    E E E E E E E E 
    E E E E E E E E 
    输入落子的地方:x,y
    1 7
    W W W W W W W W 
    B B B B B B B W 
    E B B B B B W W 
    W B W W W W E W 
    W W W W W E E E 
    W W W E E E E E 
    E E E E E E E E 
    E E E E E E E E 
    
    (3, 6)
    W W W W W W W W 
    B B B B B B B W 
    E B B B B B B W 
    W B B B B B B W 
    W W W W W E E E 
    W W W E E E E E 
    E E E E E E E E 
    E E E E E E E E 
    ```
