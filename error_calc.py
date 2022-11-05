import modul
import neural_network

from global_data import out_val



def max_filter (inner, flag):
    if isinstance(inner, dict):
        f_list = modul.item_to_neur(inner)
    else: f_list = inner.copy()

    minimum = max(f_list)
    maximum = min(f_list)

    
    if flag == "in":
        minimum = maximum
        for i in range(len(f_list)):
            if f_list[i] < minimum*100:
                if f_list[i] > maximum:
                    maximum = f_list[i]
            else: f_list[i] = -1
    else:
        maximum = minimum
        for i in range(len(f_list)):
            if f_list[i] > maximum/100:
                if f_list[i] < minimum:
                    minimum = f_list[i]
            else: f_list[i] = -2

    for i in range(len(f_list)):
        if f_list[i] == -1: f_list[i] = 1
        elif f_list[i] == -2: f_list[i] = 0
        else: f_list[i] = f_list[i] / maximum

    return f_list


def out_err_calc (in_store:dict, out_store:dict):

    fi_list = max_filter(in_store, "in")
    fi_list = list(map(lambda x: x-0.5, fi_list))
    fi_list = modul.neuro_to_item(fi_list, in_store)
    # print("err in ", fi_list)
    fo_list = max_filter(out_store, "out")
    fo_list = list(map(lambda x: 0.5-x, fo_list))
    fo_list = modul.neuro_to_item(fo_list, out_store)
    # print("err out ", fo_list)

    for item in fo_list:
        for i in range(len(fo_list[item])):
            fo_list[item][i] = fo_list[item][i] + (fi_list[item][0] * out_val[item][i])
            # получили словарь ошибок на выходе в fo_list

    return fo_list
            



if __name__ == '__main__':
    # I = {'copper': [1], 'iron': [2], 'coal': [5], 'water': [4]}
    # O = {'copper': [0.453, 0.211, 0.29], 'iron': [0.776, 0.308], 'coal': [1.060], 'water': [1]}
    I = main.in_stores
    O = main.out_stores
    
    out_err = (out_err_calc(I,O))
    print (out_err)

    neural_network.input_data_upd(modul.item_to_neur(out_err), len(neural_network.neural_matrix)-1)
    print (neural_network.neural_matrix)
    for i in range(len(neural_network.neural_matrix)-1,0,-1):
        print(i)
        neural_network.backWards(i)    
        # получаем в матрице нейронов ошибки для каждого нейрона

    print (neural_network.neural_matrix)

    