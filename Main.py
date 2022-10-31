from functools import reduce
from operator import add
import Neural_network
import modul

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
def app_flow_k (out_val, result_neuron=None):
    if (result_neuron == None):
        result_neuron=Neural_network.neural_matrix[len(Neural_network.neural_matrix)-1]

    res_in = []
    res_in = list(reduce(lambda x, y : x + y, list(out_val.values())))
    print(list(map(lambda x, y : x*y , result_neuron, res_in)))
    res_in = list(map(lambda x, y : x*y , result_neuron, res_in)).copy()
    for i in range(len(res_in)-1):
        result_neuron[i] = res_in[i]


def flow_value_generator(): # нужен для создания тестового списка максимального потребления ресурсов
    global flow_gen
    flow_gen = mine_value.copy()
    flow_gen = modul.item_to_neur(flow_gen)
    for i in range(len(flow_gen)):
        flow_gen[i] = flow_gen[i] * flow_value
    flow_gen = modul.neuro_to_item(flow_gen, mine_value)


    
# Считаем на сколько изменились in_store по команде неёросети
def in_flow ():
    res_in = out_val.copy()
    #перемножить каждое значение согласно итему из out_val с итемом flow_gen
    for item in flow_gen:
        if item in out_val:
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
        Neural_network.neural_matrix[len(Neural_network.neural_matrix)-1]
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
in_stores = dict(copper=[0], iron=[0], coal=[0], water=[0])  # список объектов
mine_value = dict(in_stores)
mine_value.update(copper=[1], iron=[3], coal=[4])  # список "прихода"
# список выхода (может отличаться от прихода). 
out_stores = {}
# создаём списки потоков в которых будут перечислены коофициенты. В дальнейшем можно будет реализовать вычисление из суммы всех запросов
copper_val = [0.25, 0.55, 0.20]
iron_val = [0.6, 0.4]

out_val = dict(copper=copper_val, iron=iron_val)

# пока генерируем список складов на выход, потом возможно будет список продукции
for item in out_val:
    out_stores[item] = [0]
    # out_stores[item] = 0
    for j in range(len(out_val[item])-1):
        out_stores[item] = out_stores[item] + [0]
print (out_stores)

# out_neuro_count = reduce(add, [len(out_val[ox]) for ox in out_val])
out_neuro_count = sum([len(out_val[ox]) for ox in out_val])
Neural_network.neural_init(len(in_stores), out_neuro_count) # индексы выходных нейронов будут соответствовать порядку в славаре out_val 

for i in range(10):
    store_filling(in_stores, mine_value)

Neural_network.input_data_upd(modul.item_to_neur(in_stores))

print(Neural_network.neural_matrix)
for i in range(len(Neural_network.neural_matrix)-1):
    # print(i)
    Neural_network.forWards(i)

print(Neural_network.neural_matrix)

app_flow_k(out_val)
print(Neural_network.neural_matrix)

flow_value_generator()

in_flow()
