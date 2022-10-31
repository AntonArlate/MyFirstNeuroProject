import Neural_network

# алгоритм наполнения складов
def mine (in_stores, mine_value):
    
    for item in in_stores:
        in_stores[item] = in_stores[item] + mine_value[item]


# создаём склады в виде словаря (название ресурса : значение)
in_stores = dict(copper=0, iron=0, coal=0, water=0) # список объектов
mine_value = dict(in_stores)
mine_value.update (copper=1, iron=3, coal=4) # список "прихода"
out_stores = dict(copper=0, iron=0, coal=0) # список выхода (может отличаться от прихода)


Neural_network.weight_init (len(in_stores))
Neural_network.neural_init (len(in_stores))

for i in range(10):
    mine(in_stores, mine_value)


Neural_network.input_data_upd(list (in_stores.values()))

print(Neural_network.neural_matrix)    
for i in range(len(Neural_network.neural_matrix)-1):
    print(i)
    Neural_network.forWards(i)
    print(Neural_network.neural_matrix)
