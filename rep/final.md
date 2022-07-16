## 人工智能大作业实验报告

-----CS-20337228-彭晨晗

### 代码介绍

| 代码     | 说明                   |
| -------- | ---------------------- |
| clean.py | 进行文本清洗和初步降维 |
|KNN.py & KNN_function.py|KNN实现|
|LR.py & LR_function.py|LR实现|
|tf-idf.py|转换tf-idf矩阵|
|lstm_train.py|训练文件|
|test_train.py|测试文件|
|other_test.py|库测试文件（可忽略）|

### 一：概述

本次实验的核心内容是对反事实陈述建立模型，进行二分类的内容，主要尝试了KNN，LR.最后采取了lstm的神经网络策略. 

### 二：实验原理

对于KNN和LR这里不过多的赘述，主要解释lstm模型的部分

#### 预训练部分- word2vec

文本处理部分尝试了很多方法，包括bow之后直接算tf-idf，one-hot矩阵，但是形成的内容太多庞大，确实形成了维度灾难的问题，于是打算首先尝试word2vec算法：

这个思路的出发点是每个词语赋予唯一的编号1,2,3,4...，然后把句子看成是编号的集合，比如假设1,2,3,4分别代表“我”、“你”、“爱”、“恨”，那么“我爱你”就是[1, 3, 2]，“我恨你”就是[1, 4, 2]。但是这种标号会导致某一些不太重要的因素影响结果，所以word2vec调整算法为把相近的词语编号放在一起.同时用多维的数字来表征每个词的特征，也就是向量，示例如图：

![12](C:\Users\86139\Desktop\12.png)

类似如此Word2Vec用高维向量表示词语，并把相近意思的词语放在相近的位置，而且用的是实数向量。我们只需要有大量的某语言的语料，就可以用它来训练模型，获得词向量。

#### 神经网络lstm

lstm是在rnn的基础上，为了解决rnn在长时状态下维度消失问题（长期依赖）而出现的。其核心是遗忘机制，加入了忘记门、输入门和输出门让神经网络随机性遗忘某一些内容。神经元如图：

![aa](C:\Users\86139\Desktop\aa.webp)

门的结构很简单，就是一个sigmoid层和一个点乘操作的组合，因为sigmoid层的输出是0-1的值，这代表有多少信息能够流过sigmoid层。0表示都不能通过，1表示都能通过。

### 三：方法

KNN和LR和之前的实验报告类似，方法相同，不做过多赘述，优化部分全部写在最后面

#### 清洗部分

clean部分的作用：

```
去除字符，规整格式
形如 I’ve 形式的 变成 Ive单词
结果保存至 tidy_train.csv

停用词除去
低频词除去-低于2的去除
全部保存成小写
结果保存至 high_time.csv
```

#### 模型

模型类似下图，只在节点数上有一定的优化，算法的思想已经在上面一个过程介绍

![asa](C:\Users\86139\Desktop\asa.png)

第一部分采用的无监督学习，代码中是调用**Gensim库**中的Word2Vec子库。

```python
def word2vec_train(combined):
    model = Word2Vec(vector_size=vocab_dim, window=window_size, workers=cpu_count)
    model.build_vocab(combined)
    model.train(combined, total_words=model.corpus_count, epochs=50)
    model.save('./lstm/Word2vec_model.pkl')
    index_dict, word_vectors, combined = create_dictionaries(model=model, combined=combined)
    return index_dict, word_vectors, combined
```

lstm库用keras搭建

```python
def train_lstm(n_symbols,embedding_weights,x_train,y_train,x_test,y_test):
    print('Defining a Simple Keras Model...')
    model = Sequential()
    model.add(Embedding(output_dim=vocab_dim,
                        input_dim=n_symbols,
                        mask_zero=True,
                        weights=[embedding_weights],
                        input_length=input_length))
    model.add(LSTM(units=50, activation='tanh'))
    model.add(Dropout(0.5))
    model.add(Dense(2, activation='softmax'))
    model.add(Activation('softmax'))

    print('Compiling the Model...')
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy', f1])

    print("Train...") # batch_size=32
    model.fit(x_train, y_train, batch_size=batch_size, epochs=n_epoch, verbose=1)

    print("Evaluate...")
    score = model.evaluate(x_test, y_test, batch_size=batch_size)

    model_json = model.to_json()
    with open('./lstm/lstm.json', 'w') as outfile:
        outfile.write(model_json)
    model.save_weights('./lstm/lstm.h5')
    print('Test score:', score)
```

#### 创新与优化

选取lstm的思路是这个分类和文本情感分类很像，所以上下文的影响从先验来看我认为会产生影响，所以选取会考虑上下文关系的rnn算法，但是为了化解依赖问题，进而选取lstm

思路：考虑这个问题的切入点和虚拟语气很像，换而言之，某一些关键的词语会对是否反事实产生巨大的影响，所以对于停用词做了一些调整

原本的停用词库去除了打两个常用词，但是基于上述的先验判断have，were等词会对结果产生影响，所以重构的停用词库，只对a，in这种词做了删除。结果在下一部分展示

同时，在时间允许下，增大word2vec最后的维度，对结果有提升

另外，我们的样本有13k个，所以，对于词频的限制从5变成10，删除词频为10一下的单词，进而可以删除某些类似姓名等内容的无关因素。



由于时间原因还有一些内容没有实现

未完成的优化：

加入bert：因为word2vec没有考虑label的影响，所以结果没有很完美，会有过拟合的问题，加入bert修正，从结果来看影响很大

修正类似，因为lstm考虑上下文关系更多，同时由于虚拟语气这种考虑算法的局限性，有一些虚拟语气并不是反事实的，但是对于现实的一种假设，这种思路有局限性，对于结果的几个预测也可以看到，某一些虚拟语气被判断为反事实的，所以想要考虑加入cnn或者knn来帮助做相似性判断，通过两个神经网络综合判断是否为反事实陈述。

### 四：实验结果与分析

最后的实验结果：

![1](C:\Users\86139\Desktop\1.png)

未加入上述优化的实验结果：

![2](C:\Users\86139\Desktop\2.png)

结果提升比较明显

上述结果的运行速度每一个epoch的平均时间为31s，效果不错。

输出结果从上图中也可以看出稳步提升

但是通过最后的测试部分可以发现存在过拟合问题



KNN和LR部分的结果比较糟糕，由于维度灾难，整个程序的运行时间令人发指，所以不做结果的展示，但是KNN的结果显示正确率还是比较高的，考虑的原因是通过考虑句子的相似度，从而对学习到的虚假事实进行匹配，结果会比较好。但是即使加上了kd-tree优化时间压力还是巨大。

### 五：总结

这次实验做的工作有很多，一开始从原初学习的算法开始入手,大概尝试了一下这个项目,也发现了局限性,然后通过一点一点的通过先验的考虑去整合模型,最终确定通过word2vec+lstm来实现项目,虽然最终test结果没有非常的好,但是这个思考的过程和余下的优化是整个项目收获的部分.整个项目的完成度还是很高的,更多的工作就是对于结果的优化和对模型的调整

### 六：参考文献

基于LSTM三分类的文本情感分析-https://github.com/Edward1Chou/SentimentAnalysis
