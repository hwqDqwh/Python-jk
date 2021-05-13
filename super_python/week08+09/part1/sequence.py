"""
区分以下类型哪些是容器序列哪些是扁平序列，哪些是可变序列哪些是不可变序列：

list
tuple
str
dict
collections.deque

答:
容器序列和扁平序列的区别是容器序列可以存储多种类型的元素，扁平序列只能容纳一种基础类型（因此在内存分配上更紧凑）
容器序列有: list, tuple, dict, collections.deque
扁平序列有: str

可变/不可变序列的区分方式主要有两个：
    1. 是否可以对序列进行修改
    2. 看似可以修改的序列，修改后的内存地址是否改变，改变了其实是说明另起一块内存进行保存而已
可变序列有: lise, dict, collections.deque
不可变序列有: str, tuple
"""

# 字符串的元素不允许修改
test_str = '12345'
# class 'str' dost define '__setitem__'
# TypeError: 'str' object does not support item assignment
test_str[0] = 6

# 元组的元素不允许修改
test_tuple = [1, 2]
test_tuple[0] = 3  # TypeError: 'tuple' object does not support item assignment


# collections.deque 的元素修改后，队列的内存地址没有改变
from collections import deque
d = deque('ghi')
print(id(d))  # 4510531376
d.append('a')
print(id(d))  # 4510531376
