# coding = 'utf-8'
import numpy as np
import pandas as pd
from time import time
import tm

def target_mean_v1(data, y_name, x_name):
    result = np.zeros(data.shape[0])
    for i in range(data.shape[0]):
        groupby_result = data[data.index != i].groupby([x_name], as_index=False).agg(['mean', 'count'])
        result[i] = groupby_result.loc[groupby_result.index == data.loc[i, x_name], (y_name, 'mean')]
    return result


def target_mean_v2(data, y_name, x_name):
    result = np.zeros(data.shape[0]) # 行数
    value_dict = dict()
    count_dict = dict()
    for i in range(data.shape[0]):
        # 第 i 行
        if data.loc[i, x_name] not in value_dict.keys():
            value_dict[data.loc[i, x_name]] = data.loc[i, y_name]
            count_dict[data.loc[i, x_name]] = 1
        else:
            value_dict[data.loc[i, x_name]] += data.loc[i, y_name]
            count_dict[data.loc[i, x_name]] += 1\

    for i in range(data.shape[0]):
        result[i] = (value_dict[data.loc[i, x_name]] - data.loc[i, y_name]) / (count_dict[data.loc[i, x_name]] - 1)

    return result


def main():
    size = 100000
    print(f'{size} test data start in {time()}, please wait.')
    y = np.random.randint(2, size=(size, 1))
    x = np.random.randint(10, size=(size, 1))
    data = pd.DataFrame(np.concatenate([y, x], axis=1), columns=['y', 'x'])

    start_2 = time()
    target_mean_v2(data, 'y', 'x')
    end_2 = time()
    print(f'v2 is the python version, use time: {end_2 - start_2}')

    start_3 = time()
    tm.target_mean_v3(data, 'y', 'x')
    end_3 = time()
    print(f'v3 is the version showed by Mr.Wang, use time: {end_3 - start_3}')

    start_4 = time()
    tm.target_mean_v4(data, 'y', 'x')
    end_4 = time()
    print(f'v4 is my job, use time: {end_4 - start_4}')

if __name__ == '__main__':
    main()
