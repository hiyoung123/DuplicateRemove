# DuplicateRemove
基于simhash的文本去重算法

## 算法思路
* 使用 SimHash 计算两个文档的相似度
* 存储使用倒排索引, 根据抽屉定理（如果向三个抽屉中放四个苹果，那么一定有某个抽屉包含两个苹果），建立 num + 1 （num 为 hamming 距离的阈值）个倒排索引。
* 将文档通过 SimHash 得到的编码分为 num+1 份，每份作为 key 存入倒排索引中。
* 划分的方法并不是连续划分，而是间隔划分。因为现在的 SimHash 算法，编码出的 hash 值，大多数情况下，前面 32 位都是 0。所以如果使用连续划分的话，那么会有很多文档都会划分到 0000 的 key 中，这样很有召回大量的候选文档，违背了使用倒排索引的意义。
* 两个文档只要有一份 key 相同，那么两个文档就有可能相似。

## 使用
```python
    with open('../data/document1', 'r', encoding='utf-8') as f:
        text1 = f.read()
    with open('../data/document2', 'r', encoding='utf-8') as f:
        text2 = f.read()
    with open('../data/document3', 'r', encoding='utf-8') as f:
        text3 = f.read()

    dr = DuplicateRemove(64, 4)
    if not dr.contains(text1):
        dr.insert(text1, 1)
    print(dr.contains(text1))
    print(dr.contains(text2))
    print(dr.contains(text3))
```
结果
```python
True
True
False
```