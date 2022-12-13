from functools import reduce
from multipledispatch import dispatch
from statistics import mean


def neuro_to_item (neur_array, item_dict):
    it=0
    temp = 0
    res_dict = {}
    for item in item_dict:
        temp = len(item_dict[item])
        res_dict[item]=neur_array[it:it+len(item_dict[item])]
        it += temp    
    return res_dict

def item_to_neur(item_dict, neur_array=[]):
    neur_array = list(reduce(lambda x, y : x + y, list(item_dict.values())))
    return neur_array

def in_data_to_neur (data_array):
    maximum = max(data_array)
    neur_array = data_array.copy()
    for i in range(len(neur_array)):
        neur_array[i] = neur_array[i] / maximum
    return neur_array

@dispatch(dict)
def maximal_alignment(arr):
    '''на выходе макс = 1, остальные относительно ниже'''
    maximum = max(item_to_neur (arr))
    temp_dict = {}
    for item in arr:
        temp_dict[item] = list(map(lambda x : x / maximum, arr[item])) 
    return (temp_dict)

@dispatch(list)
def maximal_alignment(arr):
    '''на выходе макс = 1, остальные относительно ниже'''
    maximum = max(arr)
    temp_arr = []
    temp_arr = list(map(lambda x : x / maximum, arr)) 
    print (temp_arr)

@dispatch(dict, int)
def midle_shift(arr, m=1):
    '''на выходе смещения относительно среднего'''
    avg = mean(item_to_neur (arr))
    temp_dict = {}
    for item in arr:
        temp_dict[item] = list(map(lambda x : (avg - x) * m, arr[item])) 
    return (temp_dict)

@dispatch(list, int)
def midle_shift(arr, m=1):
    '''на выходе смещения относительно среднего'''
    avg = mean(arr)
    temp_arr = []
    temp_arr = list(map(lambda x : (x - avg) * m, arr)) 
    return (temp_arr)

if __name__ == '__main__':
    a = maximal_alignment({'copper': [10], 'iron': [30], 'coal': [40], 'water': [0]})    
    print (a)
    a = midle_shift (a)
    print(a)