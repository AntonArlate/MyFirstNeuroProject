from functools import reduce


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


if __name__ == '__main__':
    item_to_neur({'copper': [10], 'iron': [30], 'coal': [40], 'water': [0]})    