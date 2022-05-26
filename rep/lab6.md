# 中山大学计算机学院人工智能实验报告

| 班级 | 冯诺依曼实验班 | 专业 | 计算机科学（系统结构) |
| :--- | -------------- | ---- | --------------------- |
| 学号 | 20337228       | 姓名 | 彭晨晗                |

### 0. 代码提交目录

|文件|说明|
|:---|----|
|NB.py|朴素贝叶斯主函数|
|function.py|功能函数汇总|
|KNN_classfication.py|KNN主函数|
|KNN_functon|KNN函数|

### 1. 实验题目

​	 文本情感分类

### 2. 实验内容

​	Update：2022.5.5 朴素贝叶斯

1. 算法原理

   基于条件概率的假设，朴素贝叶斯的原理主要是利用样本（训练集）形成一个条件概率矩阵，基于这个矩阵形成对于后验概率的预测。
   
   主要的公式：
   $$
   y = argmax_yp(x|y)p(y)
   $$
   x是一个条件向量，在我们需要的问题中就变成了：
   $$
   令 ei 表示某种情绪,x_k为某个词条
   $$
   
   $$
   argmax_{e_i}\prod p(x_k|e_i)p(e_i)
   $$
   
   根据这个最大值推测情绪
   
   两种模型：
   
   伯努利模型：
   $$
   p(x_k|e_i) = \frac {n_{e_i}(x_k)}{N_{e_i}} \\
   p(e_i) = \frac {N_{e_i}}{N}
   $$
   统计的是文本的频率，即出现关键词的文本的数量
   
   多项式模型：
   $$
   p(x_k|e_i) = \frac {nW_{e_i}(x_k)}{nW_{e_i}} \\
   p(e_i) = \frac {N_{e_i}}{N}
   $$
   统计的是单词的频率，即出现关键词的文本中的单词的数量
   
   拉普拉斯平滑：
   
   这部分主要是为了去除0
   
   主要是给分子分母分别加上一个数
   
   其中在多项式的拉普拉斯平滑中，我们通常会给分母加上一个$ V_{e_i} $ 表示不重复的单词 
   
   Update：2022.5.8 KNN
   
   KNN即k近邻算法，通过将文本转换为向量，然后找到向量周围k个最近Label作为结果。
   
   文本转换方式：
   
   one-hot： 以是否出现为标签
   
   tf-idf： 用词在文本值中出现次数作为权值，用归一化的出现次数作为数值相乘得到的向量


2. 流程及伪代码

```
数据输入

模型的参数提取 分别计算N，Nei等

循环拉普拉斯平滑的超参数
	通过验证集选取模型
	
整合训练集和验证集

完成测试集
```

```txt
数据输入

文本向量化

KNN过程

循环K
	通过验证集选取模型
	
整合训练集和验证集

完成测试集
```



3. 关键代码展示

   1. 概率矩阵计算

      两部分是类似的，枚举情绪分别统计需要的内容

``` python
    # 伯努利模型
    for mood in Mood:
        for diction in dictionary:
            n_ei_xk[(mood, diction)] = 0
            for i in range(N):
                if mood != Label[i]:
                    continue
                for word in Word[i]:
                    if word == diction:
                        n_ei_xk[(mood, diction)] = n_ei_xk[(mood, diction)] + 1
                        break
                        
    # 多项式模型
    for mood in Mood:
        n_w_ei[mood] = 0
        g = set()
        for i in range(N):
            if mood == Label[i]:
                n_w_ei[mood] = n_w_ei[mood] + len(Word[i])
                for word in Word[i]:
                    g.add(word)
                    if not (mood, word) in n_w_xk_ei:
                        n_w_xk_ei[(mood, word)] = 0
                    n_w_xk_ei[(mood, word)] = n_w_xk_ei[(mood, word)] + 1
        g = list(g)
        v_ei[mood] = len(g)
```

​            2.测试合适的拉普拉斯平滑系数

```python
    # 测试合适的拉普拉斯平滑系数
    pr = 0.000001
    while pr != 0.00001:
        print(pr)

        res = validation(Mood, p_ei_list, n_ei_xk, N, dictionary, pr)
        print(res)

        res = validation1(Mood, p_ei_list, n_w_xk_ei, N, dictionary, n_w_ei, v_ei, pr)
        print(res)

        pr = pr + 0.000001
```

​			3.验证集部分

​			核心部分就是枚举每一种情绪根据公式进行计算，然后找到最大的那个，同验证集的label进行对比

```python
            for mood in Mood:
                tmp = p_ei_list[mood]/N
                for word in words:
                    if word in dictionary:
                        tmp = tmp * laplacian_smoothing(n_ei_xk[(mood, word)], p_ei_list[mood], la)
                    else:
                        tmp = tmp * laplacian_smoothing(0, p_ei_list[mood], la)
                if anst == 0:
                    ans = mood
                    anst = tmp
                elif tmp > anst:
                    ans = mood
                    anst = tmp

            if ans == line[1]:
                cur = cur + 1
```

​			4.拉普拉斯平滑

```python
def laplacian_smoothing(a, b, d):
    return (a + d)/(b + 2)
```

####  KNN：

1. 计算one-hot 

   ``` python
       for i in range(n):
           tmp = {}
           for word in dictionary:
               tmp[word] = 0
           for word in Word[i]:
               tmp[word] = tmp[word] + 1
           for word in dictionary:
               if tmp[word] != 0:
                   tmp[word] = 1
           one_hot.append(tmp)
   ```

   

   计算tf-idf

   ```python
       for word in dictionary:
           idf[word] = 0
       for i in range(n):
           lenth = len(Word[i])
           tf_tmp = {}
           for word in dictionary:
               tf_tmp[word] = 0
           for word in Word[i]:
               tf_tmp[word] = tf_tmp[word] + 1
           for word in dictionary:
               if tf_tmp[word] != 0:
                   idf[word] = idf[word] + 1
               tf_tmp[word] = tf_tmp[word]/lenth
           tf.append(tf_tmp)
   
       for word in dictionary:
           idf[word] = math.log(n / (1 + idf[word]))
   ```

   这个过程就是一个统计的过程

   2.knn部分

   分别去计算每个向量和当前判断的距离，然后产生一个距离表，查询前k个，完成结果范围

   ``` python
       for i in range(n):
           distance = cal_dis(idf, tf[i], test_tf, dictionary)
           dis.append((distance, Label[i]))
       dis = sorted(dis, key=lambda x: x[0], reverse=True)
       cnt = {}
       for mood in Mood:
           cnt[mood] = 0
       ans = ''
       anst = 0
       for i in range(K):
           cnt[dis[i][1]] += 1
           if ans == '':
               ans = dis[i][1]
               anst = cnt[dis[i][1]]
           elif anst < cnt[dis[i][1]]:
               ans = dis[i][1]
               anst = cnt[dis[i][1]]
   ```

   计算距离部分
   ```python
   def cal_dis(idf, tf, test_tf, dictionary):
       res = 0
       for word in dictionary:
           res += idf[word] * idf[word] * (tf[word] - test_tf[word]) * (tf[word] - test_tf[word])
       res = math.sqrt(res)
       return res
   ```

   

### 3. 实验结果及分析

​    1.实验命令行结果图片 

​    最终的结果这里展示

![1](F:\Code\AI_learning\img\lab6\1.png)

​	2.KNN结果

![1651997965(1)](F:\Code\AI_learning\img\lab6\1651997965(1).png)

K计算结果：

![1651998026(1)](F:\Code\AI_learning\img\lab6\1651998026(1).png)

测试集结果：

​	![2](F:\Code\AI_learning\img\lab6\2.png)



![1651998988(1)](F:\Code\AI_learning\img\lab6\1651998988(1).png)

#### 结果分析：

​	正确率达到了40%左右，开始的正确率不高只有5%，关于优化放到下一部分去阐述

关于模型：

在开始时伯努利模型更好，当正确率上升时结果呈现时多项式模型更好。选定为多项式模型。 



​	KNN的部分正确率是36%

##### 评测指标展示与分析：

按照ppt的过程，最后达到的正确率只有5%左右，为了优化这个正确率，从算法出发，算法过程没有什么能够优化的部分，是一类统计的方法，那么只能考虑某一些系数问题，根据ta上课的提醒，考虑从拉普拉斯平滑部分入手，那么考虑拉普拉斯平滑的作用是为了让0数据可靠，这里基于的先验经验是没有出现的单词以均匀分布的概率计算，也就是有$\frac {1}{2}$ 的概率是该情绪，同样的也有可能不是。但是这个先验的经验其实是有问题的，对于没有统计过的单词，更大的概率是取否，例如姓名，额外的修饰词，地名，或者很多不相关的内容，个性化的设计等等的影响，所以，考虑调小分子的。结果支持了这个猜想，当分别设置0.1，0.01，0.001时结果逐渐变好，通过上面对于拉普拉斯平滑系数的枚举过程，发现当取1e-6时基本不再有增长。那么超参数便选择完毕。 效果的截图如上图所示。

KNN部分用K去跑超参数，结果不是很适用，在大于8的部分已经不再增长。 



### 4.思考题

• 1. 朴素贝叶斯中，伯努利模型和多项式模型分别有什么优缺点？

伯努利模型注重的是词在文本中出现的文本的频率，而多项式注重的是词的频率。伯努利必要能反映词和文本的关系，但容易受到一些惯用词例如I之类的影响，多项式则相反

• 2. IDF数值有什么含义？TF-IDF数值有什么含义？

IDF表示的是词在文本中的普遍性，作为一种权值的存在，tf-idf值让tf的值能够以文本普遍性作为权值，从而将单词的文本频率纳入考量

• 3. kNN中为什么是距离的倒数？如果要求同一测试样本的各个情感概率总和为1，应该如何处理？

距离越近，数值越小，越相似

概率综合为1的话就要做归一化处理，将相似度累加后在做
