"""
map 的定义:
map 第一个参数是函数的对象,第二个参数是 iterable 对象表示处理的数据范围
逻辑是依次传入第二个参数队列的数据给第一个参数代表的函数进行处理并返回
参考 yield, map 返回的是一个迭代器
"""


def simple_map(func, sequence):
    # map_list = []

    for i in sequence:
        # print(i)
        yield func(i)
        # map_list.append(func(i))

    # return map_list


def square(x):
    return x**2


res = simple_map(square, [1, 2, 3])
print(res)
next(res)
list(res)


