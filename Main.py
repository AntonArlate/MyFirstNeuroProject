from copy import deepcopy
from functools import reduce
from operator import add
from time import sleep
import neural_network
import modul


from global_data import out_val
from global_data import in_stores
from global_data import out_stores


import learning

# алгоритм наполнения складов
def mine(in_stores, mine_value):
    for item in in_stores:
        in_stores[item] = in_stores[item] + mine_value[item]

# алгоритм наполнения складов (попытка унифицировать, если будет работать - убрать метод mine)
def store_filling(stores, fill_value, indication="+"):
    if isinstance(stores, list):
        for i in range(len(stores)):
            if indication == "-":
                stores[i] = stores[i] - fill_value[i]
            else: 
                stores[i] = stores[i] + fill_value[i]    
    else:
        for item in stores:
            if item in fill_value:
                if indication == "-":
                    stores[item] = list(map(lambda x, y: x-y, stores[item], fill_value[item]))
                else: 
                    stores[item] = list(map(lambda x, y: x+y, stores[item], fill_value[item]))



# Применяем коофициенты потоков к результату нейросети
def app_flow_k (out_value=None, result_neuron=None):
    if (out_value == None):
        out_value = out_val.copy()
    if (result_neuron == None):
        result_neuron=neural_network.neural_matrix[len(neural_network.neural_matrix)-1]

    res_in = []
    res_in = list(reduce(lambda x, y : x + y, list(out_value.values())))
    # print(list(map(lambda x, y : x*y , result_neuron, res_in)))
    res_in = list(map(lambda x, y : x*y , result_neuron, res_in)).copy()
    for i in range(len(res_in)-1):
        result_neuron[i] = res_in[i]


def flow_value_generator(): # нужен для создания тестового списка максимального потребления ресурсов # изменено на вход
    global flow_gen
    flow_gen = mine_value.copy()
    # flow_gen = modul.item_to_neur(flow_gen)
    # for i in range(len(flow_gen)):
    #     flow_gen[i] = flow_gen[i] * flow_value
    # flow_gen = modul.neuro_to_item(flow_gen, mine_value)
    # print(flow_gen)


    
# Считаем на сколько изменились in_store по команде неёросети
def in_flow ():
    # res_in = out_val.copy()
    res_in={}
    #перемножить каждое значение согласно итему из out_val с итемом flow_gen
    for item in flow_gen:
        if item in out_val:
            res_in[item] = out_val[item].copy()
            for j in range(len(out_val[item])):
                res_in[item][j] = out_val[item][j] * flow_gen[item][0]
    # print(list(reduce(lambda x, y : x + y, list(res_in.values()))))
    #Получим то на сколько макс должны увеличиться склады out
    #перемножаем с результатом сети и получаем расчитаное изменение out

    # Neural_network.neural_matrix[len(Neural_network.neural_matrix)-1] = [1,1,1,1,1]

    # print(Neural_network.neural_matrix[len(Neural_network.neural_matrix)-1])

    res_out = list(map(
        lambda x, y : x*y ,
        list(reduce(lambda x, y : x + y, list(res_in.values()))),
        neural_network.neural_matrix[len(neural_network.neural_matrix)-1]
    ))

    res_in = modul.neuro_to_item(res_out, res_in)
    store_filling(out_stores, res_in)

    #cумировать все итемы из предыдущего результата чтобы получить уменьшение складов in 
    for item in res_in:
        res_in[item] = [sum(res_in[item])]
    store_filling(in_stores, res_in,"-")

    # for item in res_in:
    #     res_in[item] = sum(res_in[item])


flow_gen = []
flow_value = 0.9999 # временный коофициент максимального "оттока" из входящих складов
# создаём склады в виде словаря (название ресурса : значение)
in_stores.update({'copper':[0], 'iron':[0], 'coal':[0], 'water':[0]})  # список объектов
mine_value = dict(in_stores)
mine_value.update(copper=[3], iron=[2], coal=[1], water=[1])  # список "прихода"
# список выхода (может отличаться от прихода). 

# создаём списки потоков в которых будут перечислены коофициенты. В дальнейшем можно будет реализовать вычисление из суммы всех запросов
copper_val = [0.25, 0.55, 0.20]
iron_val = [0.6, 0.4]
coal_val=[1]
water_val=[1]

out_val.update({'copper':copper_val, 'iron':iron_val, 'coal':coal_val, 'water':water_val})
# print(out_val)


# пока генерируем список складов на выход, потом возможно будет список продукции
for item in out_val:
    out_stores[item] = [0]
    # out_stores[item] = 0
    for j in range(len(out_val[item])-1):
        out_stores[item] = out_stores[item] + [0]
# print (out_stores)

# out_neuro_count = reduce(add, [len(out_val[ox]) for ox in out_val])
out_neuro_count = sum([len(out_val[ox]) for ox in out_val])
neural_network.neural_init(len(in_stores), out_neuro_count) # индексы выходных нейронов будут соответствовать порядку в славаре out_val 


learning.err_matrix = deepcopy(neural_network.neural_matrix) # передаём копию матрицы нейронов в калькулятор ошибки

# for i in range(1):
#     store_filling(in_stores, mine_value)

# neural_network.input_data_upd(modul.in_data_to_neur(modul.item_to_neur(in_stores)),0)

# for i in range(len(neural_network.neural_matrix)-1):
#     neural_network.forWards(i)

# app_flow_k(out_val)

flow_value_generator()
# in_flow()

count = 1
for i in range(20000):
    count += 1
    store_filling(in_stores, mine_value)
    neural_network.input_data_upd(modul.in_data_to_neur(modul.item_to_neur(in_stores)),0)

    for i in range(len(neural_network.neural_matrix)-1):
        neural_network.forWards(i)
    
    app_flow_k(out_val)
    in_flow()

    learning.learn_program() # запуск обучения на текущем состоянии

    if count == 20:
        count = 0
        print('in -> ', in_stores)
        print('out -> ', out_stores)
        print()
        # sleep(0.05)