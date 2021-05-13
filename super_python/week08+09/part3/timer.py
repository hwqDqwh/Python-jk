"""
实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数。
"""

import time
from functools import wraps
import random


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        time_begin = time.time()
        func(*args, **kwargs)
        time_end = time.time()
        print(f"{func.__name__} execution time: {time_end - time_begin}")
    return wrapper


@timer
def square(a):
    res = a**2
    print(f'square: {res}')

    sleep_second = random.random() * 10
    print(f'sleep {sleep_second} second')
    time.sleep(sleep_second)

    return res


if __name__ == '__main__':
    square(5)
