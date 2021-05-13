# distutils: language=c++
import numpy as np
cimport numpy as np
import copy
from libcpp.unordered_map cimport unordered_map


cpdef target_mean_v3(data, y_name, x_name):
    """
    Mr. Wang's show
    """
    cdef long nrow = data.shape[0]
    cdef np.ndarray[double] result = np.asfortranarray(np.zeros(nrow), dtype=np.float64)
    cdef np.ndarray[double] y = np.asfortranarray(data[y_name], dtype=np.float64)
    cdef np.ndarray[double] x = np.asfortranarray(data[x_name], dtype=np.float64)

    target_mean_v3_impl(result, y, x, nrow)
    return result

cdef void target_mean_v3_impl(double[:] result, double[:] y, double[:] x, const long nrow):
    cdef dict value_dict = dict()
    cdef dict count_dict = dict()

    cdef long i
    for i in range(nrow):
        if x[i] not in value_dict.keys():
            value_dict[x[i]] = y[i]
            count_dict[x[i]] = 1
        else:
            value_dict[x[i]] += y[i]
            count_dict[x[i]] += 1

    i=0
    for i in range(nrow):
        result[i] = (value_dict[x[i]] - y[i])/(count_dict[x[i]]-1)

cpdef target_mean_v4(data, y_name, x_name):
    """
    My cython job.
    I try to optimize the data type of numpy and use unordered_map to speed up statistics
    """
    cdef long nrow = data.shape[0]
    cdef np.ndarray[long] result = np.asfortranarray(np.zeros(nrow), dtype=np.int64)
    cdef np.ndarray[int] y = np.asfortranarray(data[y_name], dtype=np.int32)
    cdef np.ndarray[long] x = np.asfortranarray(data[x_name], dtype=np.int64)

    target_mean_v4_impl(result, y, x, nrow)
    return result


cdef void target_mean_v4_impl(long[:] result, int[:] y, long[:] x, const long nrow):
    cdef unordered_map[int, int] value_dict
    cdef unordered_map[int, int] count_dict
    cdef long i

    for i in range(nrow):
        if value_dict.find(x[i]) == value_dict.end():
            value_dict[x[i]] = y[i]
            count_dict[x[i]] = 1
        else:
            value_dict[x[i]] += y[i]
            count_dict[x[i]] += 1

    result_2 = result.copy()
    i=0

    for i in range(nrow):
        # this is correct
        t = value_dict[x[i]] - y[i]
        p = count_dict[x[i]] - 1
        result[i] = t / p
        # result_2[i] = (value_dict[x[i]] - y[i]) / (count_dict[x[i]] - 1)

        """
        this is wrong, tips is "tm.pyx:139:45: Cannot assign type 'double' to 'long'" for compile
        https://stackoverflow.com/questions/64932145/cython-compile-error-cannot-assign-type-double-to-int-using-mingw64-in-win
        This explanation here show the reason for the compile exception, but there is another question about why the
        above writing can work normally? Does python do type conversion here?
        """
        # result[i] = (value_dict[x[i]] - y[i]) / (count_dict[x[i]] - 1)