# 中山大学计算机学院人工智能实验报告

| 班级 | 冯诺依曼实验班 | 专业 | 计算机科学（系统结构) |
| :--- | -------------- | ---- | --------------------- |
| 学号 | 20337228       | 姓名 | 彭晨晗                |

### 0. 代码提交目录

|文件|说明|
|:---|----|
|PLA.py|朴素贝叶斯主函数|
|PLA_function.py|功能函数汇总|
|LR.py|KNN主函数|
|LR_functon.py|KNN函数|

### 1. 实验题目

​	 机器学习

### 2. 实验内容

1.  

   PLA

​	任务：训练一个二分类器

令y = wx+b 

初始化参数，然后根据失配的点对这条直线进行调整，调整的过程时根据随机梯度下降的过程。 

随机梯度下降即每一项加上一个随机的梯度。 

​	LR

LR过程主要是通过sigmoid函数作为评估项，通过批量梯度下降的方法更新参数直至达到一定的收敛条件


2. 流程及伪代码

```
数据输入

设置学习率并初始化

选择误分点，更新w和b

重复
```

```txt
数据输入

添加常数项

初始化

计算当前的梯度并更新w直至收敛

```



3. 关键代码展示

   1. 误分过程

``` python
        for i in range(n):
            tmp = sign(w, charactor[i], 41)
            if tmp * label[i] <= 0:
                change(w, charactor[i], label[i], learn_rat, 41)
                # print("Change w")
                # print(w)
                count += 1
```

​            2.sign函数

```python
def sign(a, b, n):
    res = 0
    for i in range(n):
        res += a[i] * b[i]
    if res > 0:
        return 1
    else:
        return -1
```

​			3.验证集过程

```python
    cur = 0
    lenth = validation_end - validation_begin
    for i in range(lenth):
        y = sign(w, charactor[validation_begin + i], 41)
        if y == label[validation_begin + i]:
            cur += 1
    print(cur/lenth)
```



####  LR：

1. 批量梯度下降

   ``` python
       for i in range(circle_time):
           print('train: ' + str(i))
           update = []
           for j in range(41):
               update.append(0)
           for j in range(n):
               tmp = sigmoid(w, charactor[j], 41)
               for k in range(41):
                   update[k] += (label[j] - tmp) * charactor[j][k]
           for j in range(41):
               w[j] += learn_rat * update[j]
   ```
   
   
   
   sigmoid函数
   
   ```python
   def sigmoid(a, b, n):
       res = 0
       for i in range(n):
           res += a[i] * b[i]
       # print(res)
       return 1.0/(1.0 + math.exp(-res))
   ```
   
   
   
   2.验证集部分
   
   ``` python
       for i in range(lenth):
           y = sigmoid(w, charactor[validation_begin + i], 41)
           if y > 0.5:
               ans = 1
           else:
               ans = 0
           if ans == label[validation_begin + i]:
               cur += 1
       print(cur/lenth)
   ```

   
   

### 3. 实验结果及分析

​    1.PLA结果

![1653448810(1)](F:\Code\AI_learning\img\1653448810(1).png)

​	2.LR结果

![1653449637(1)](F:\Code\AI_learning\img\1653449637(1).png)



#### 结果分析：

两者稍微调了一下参后都达到了70%以上的正确率，故不采用交叉验证

##### 评测指标展示与分析：

结果显示的还是比较满意的，对于学习率设置的比较小，迭代次数比较多，然后在分的验证集上的结果有比较好的展示。学习率较大时整个模型的表现只有50%左右。



### 4.思考题

• 1. 不同学习率的影响

一个比较小的学习率带来的是更容易收敛，但是收敛速度更慢。而大的学习率很快的会收敛，但是有可能会没有办法收敛。类似爬山，在山的两侧来回跳转

• 2. 模长为0的问题

不合适，因为通常情况下模长为零太苛刻了，同时会因为存在鞍点而导致陷入局部最优解

一般训练过程中Loss一开始有个极速下降的过程，然后开始斜坡缓慢下降，最后通过学习率衰减再得到一个快速下降完成训练。即loss比较平滑了之后
