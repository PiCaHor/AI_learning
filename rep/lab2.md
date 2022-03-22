# 中山大学计算机学院人工智能实验报告

| 班级 | 冯诺依曼实验班 | 专业 | 计算机科学（系统结构) |
| :--- | -------------- | ---- | --------------------- |
| 学号 | 20337228       | 姓名 | 彭晨晗                |

### 0. 代码提交目录

|文件|说明|
|:---|----|
|FIOL_data.py|数据存储结构|
|function.py|用的的函数|
|main.py|主程序|
|test.txts| 数据         |
### 1. 实验题目

​	 知识图谱-FIOL算法

### 2. 实验内容

1. 算法原理

   算法的思路有点类似与A*，通过枚举一阶谓词并将其添加到逻辑中，再通过以正例和反例的为计算因子的估价函数进行学习，最终不再覆盖反例则说明找到了推理逻辑。（序贯覆盖）

   伪代码

```
初始化与数据输入（从文件数据）
分离谓词和动词便于后续处理

开始循环
  枚举所有的关系
	枚举所有的下x,y,z关系
		计算正例和反例数
		通过正例和反例数计算FOIL_gain
		更新最大值并记录相关的信息
  更新被加入的谓词
  更新例子集
  返回循环
  
输出关系
递归检查所有符合的逻辑并输出


计算正反例的过程：
	枚举所有的x,y,z
		检查被加入的谓词是否成立
		检查前缀的逻辑是否成立
		
		在例子集中进行遍历更新正例数和反例数
		同时更新例子集
	返回结果
	
关于mod的解释：
0： x,y->x,y
1： y,x->x,y
2： x,z->x,y
3： z,x->x,y
4： y,z->x,y
5： z,y->x,y
```

3. 关键代码展示
   1. 算法实现
``` python
def cal(relations, mod, p_example, n_example, message_hub, logic_hub, name_hub, question_relation):
    p_cnt = 0
    p_new = []
    n_cnt = 0
    n_new = []
    left = ''
    right = ''
    # 枚举新增逻辑的两个谓词
    for name1 in name_hub:
        for name2 in name_hub:
            left = name1
            right = name2
            t = Message(left, relations, right)
            # 检查新增逻辑是否在背景知识中
            if not find(message_hub, t):
                continue
            t_name3 = ''
            name3 = ''
            mfl = True
            lfl = False
            # 枚举剩下的一个谓词
            for name3 in name_hub:
                if len(logic_hub) == 0:
                    mfl = False
                    break
                if lfl:
                    break
                # 检查在已有逻辑中是否成立
                for logic in logic_hub:
                    if check_in(logic, name1, name2, name3, message_hub, mod):
                        mfl = False
                        t_name3 = name3
                        lfl = True
                        break
            name3 = t_name3
            # 计算正反例
            if mfl:
                continue
            if len(logic_hub) == 0:
                if mod == 0:
                    t = Message(name1, question_relation, name2)
                elif mod == 1:
                    t = Message(name2, question_relation, name1)
                elif mod == 2:
                    t = Message(name1, question_relation, '')
                elif mod == 3:
                    t = Message(name2, question_relation, '')
                elif mod == 4:
                    t = Message('', question_relation, name1)
                elif mod == 5:
                    t = Message('', question_relation, name2)
                if find(p_example, t):
                    p_cnt += 1
                    p_new.append(t)
                if find(n_example, t):
                    n_cnt += 1
                    n_new.append(t)
            else:
                if mod == 0:
                    t = Message(name1, question_relation, name2)
                elif mod == 1:
                    t = Message(name2, question_relation, name1)
                elif mod == 2:
                    t = Message(name1, question_relation, name3)
                elif mod == 3:
                    t = Message(name2, question_relation, name3)
                elif mod == 4:
                    t = Message(name3, question_relation, name1)
                elif mod == 5:
                    t = Message(name3, question_relation, name2)
                t_n = t
                if find(p_example, t, p_new):
                    p_cnt += 1
                if find(n_example, t_n, n_new):
                    n_cnt += 1
    return [p_cnt, n_cnt], [p_new, n_new]
```

​            2. 比对是否存在在背景或者例子集中

```python
def find(message_hub, t, new=[]):
    fl = False
    # 枚举
    for message in message_hub:
        # 需要进行空判断
        if (t.left() == '' or message.left() == t.left()) and (t.right() == '' or message.right() == t.right()) and message.relat() == t.relat():
            new.append(message)
            fl = True
    return fl
```

​			3.前缀的判断

```python
def check_in(logic, x1, x2, x3, message_hub, t_mod):
    mod = logic.get_mod()
    x = ''
    y = ''
    z = ''
    # 根据mod方式对x，y，z赋值
    if t_mod == 0:
        x = x1
        y = x2
        z = x3
    elif t_mod == 1:
        x = x2
        y = x1
        z = x3
    elif t_mod == 2:
        x = x1
        y = x3
        z = x2
    elif t_mod == 3:
        x = x2
        y = x3
        z = x1
    elif t_mod == 4:
        x = x3
        y = x1
        z = x2
    elif t_mod == 5:
        x = x3
        y = x2
        z = x1

    t = Message()
    # 建立需要检查的逻辑
    if mod == 0:
        t = Message(x, logic.get_relate(), y)
    elif mod == 1:
        t = Message(y, logic.get_relate(), x)
    elif mod == 2:
        t = Message(x, logic.get_relate(), z)
    elif mod == 3:
        t = Message(z, logic.get_relate(), x)
    elif mod == 4:
        t = Message(y, logic.get_relate(), z)
    elif mod == 5:
        t = Message(z, logic.get_relate(), y)
	# 检查是否在逻辑中
    if not find(message_hub, t):
        return False
    else:
        return True
```

​			4.估值函数计算

```python
def cal_gain(a, b):
    return math.log2(a / (a + b))
```

   5. 输出的递归分析

      这部分代码比较多，但都是由于mod不同导致的类似的部分，只截取部分，其他的都是类似的逻辑

      ```python
      def check(logic_num, logic_hub, n, message_hub, step, used, various, question):
          # 已经完成递归找到了
          if step == logic_num:
              t = Message(various[0], question.relat(), various[1])
              # 要避免生成的逻辑已经在背景知识中
              if not find(message_hub, t):
                  print(question.relat() + "(" + various[0] + ',' + various[1] + ")")
              return
          # 枚举所有的背景知识
          for i in range(n):
              if used[i]:
                  continue
              如果逻辑符合
              if message_hub[i].relat() == logic_hub[step].get_relate():
                  mod = logic_hub[step].get_mod()
                  if mod == 0:
                      # 根据x,y,z是否有空进行递归
                      if various[0] != '' and various[1] != '' and various[0] == message_hub[i].left() and various[1] == \
                          message_hub[i].right():
                          # 没有空的话且没有冲突，直接跳入下一次
                          used[i] = 1
                          check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                          used[i] = 0
                      elif various[0] == '' and various[1] != '' and various[1] == message_hub[i].right():
                          # 有一个是空的先复制在做下一次，然后结束后还原
                          various[0] = message_hub[i].left()
                          used[i] = 1
                          check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                          used[i] = 0
                          various[0] = ''
                      elif various[0] != '' and various[1] == '' and various[0] == message_hub[i].left():
                          various[1] = message_hub[i].right()
                          used[i] = 1
                          check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                          used[i] = 0
                          various[1] = ''
                      # 两个都是空的
                      elif various[0] == '' and various[1] == '':
                          various[0] = message_hub[i].left()
                          various[1] = message_hub[i].right()
                          used[i] = 1
                          check(logic_num, logic_hub, n, message_hub, step + 1, used, various, question)
                          used[i] = 0
                          various[1] = ''
                          various[0] = ''
      ```

      

3. 实验结果及分析

​		输出结果： 

​		这里没有前面的部分因为通过文件输入了，结果的输出和要求的相同![image-20220322103411814](C:\Users\86139\AppData\Roaming\Typora\typora-user-images\image-20220322103411814.png)

[仓库地址](https://github.com/PiCaHor/AI_learning)
