# описание переменных и правил
# входные данные берутся из вне
# матрица нейронов
from math import exp
from random import random
import program_1.modul as modul


neural_matrix_init = [3, 4] # сколько нейронов на каждом слое
neural_matrix = [] # двумерный массив с данными всех нейронов [слой][значение нейрона n]
weight_matrix = [] # здесь будут все связи
activationF = lambda x : 1 / (1 + exp(-1 * x))
bias_map = [True, True, True, False]

# derivativeF = lambda 


def in_activation (inner):
    if isinstance(inner, dict):
        f_list = modul.item_to_neur(inner)
    else: f_list = inner.copy()

    maximum = max(f_list)
    f_list = list(map(lambda x: x / maximum, f_list))
    return f_list


#обновление входных значений
def input_data_upd (input_data, layer, n_matr=[]):
    '''n_matr оставить пустым для передачи в neural_matrix'''
    if n_matr == []:
        n_matr = neural_matrix
    # n_matr[layer] = input_data
    n_matr[layer] = input_data + [1] * bias_map[layer]

# создаём список нейронов с их значениями
def neural_init(neural_config):
    '''Создаёт список значений всех нейронов. требуется количество входных и кол-во выходных данных'''
    global neural_matrix_init
    global neural_matrix

    neural_config = list(map(lambda x, y : x+y, neural_config, bias_map))

    n=len(neural_config)

    neural_matrix.extend ( [[1] * neural_config[i] for i in range(n)])

    # print ("Neural -->> ", neural_matrix)
    # print()

    weight_init(neural_config)

    # neural_matrix_init.pop(0)

# первичная инициализация весов (потом сделать хранение в файле)
def weight_init(neural_config): 
    '''Создаёт список значений всех весов.'''
    global neural_matrix_init
    # neural_matrix_init.insert(0, input_count)
    global weight_matrix

    for l in range (0,len(neural_config)-1):
        current_lay = []
        for current_lay_n in range (neural_config [l]):
            next_lay = []
            # for next_lay_n in range (neural_config [l+1]):
            for next_lay_n in range (neural_config [l+1] - bias_map[l+1]):
                next_lay.append(random ()) # random () /\ next_lay_n
            current_lay.append(next_lay)
        weight_matrix.append(current_lay)
        # print ("Weight L",l,"->L",l+1, "==>> ", weight_matrix[l])
    
        # print (weight_matrix, ' W_matrix')

    # neural_matrix_init.pop(0)
 # создаём многомерный массив связей [номер обрабатываемого слоя[номер нейрона на обрабатываемом слое[номер нейрона на следующем слое]]]                
                                                               # [l1[n1l1[n1l2, n2l2], n2l1[n1l2, n2l2], l2[[n1l1[n1l2, n2l2], n2l1[n1l2, n2l2]]]
                # print (prev_lay, " <-> ", current_lay)

def forWards (cur_lay): 
    '''Прямое распространение. Вводим номер обрабатываемого слоя. Будет использован следующий'''
    global neural_matrix
    global weight_matrix

    neuron_in = neural_matrix[cur_lay]
    # print(neuron_in)
    neuron_out = neural_matrix[cur_lay+1]
    cur_lay_weight = weight_matrix [cur_lay]

    in_neu_len = len(cur_lay_weight) - bias_map[cur_lay+1]
    # out_neu_len = len(cur_lay_weight[0])
    out_neu_len = len(cur_lay_weight[0]) - bias_map[cur_lay+1]


    for i in range(out_neu_len):
        neuron_out[i] = 0
        for j in range(in_neu_len):
            weight = cur_lay_weight[j][i]
            neuron_out[i] = neuron_out[i] + (neuron_in[j]*weight)
            if bias_map[cur_lay]: neuron_out[i] = neuron_out[i] + (1 * cur_lay_weight[in_neu_len-1][i])
        neuron_out[i] = activationF(neuron_out[i]) # функция активации

def backWards (cur_lay, n_matr=[]): 
    '''обрвтное распространение. Вводим номер обрабатываемого слоя. Будет использован предыдущий
    n_matr оставить пустым для передачи в neural_matrix'''
    if n_matr == []:
        n_matr = neural_matrix

    global weight_matrix

    neuron_in = n_matr[cur_lay]
    neuron_out = n_matr[cur_lay-1]
    cur_lay_weight = weight_matrix [cur_lay-1]

    # in_neu_len = len(neuron_in)
    in_neu_len = len(neuron_in) - bias_map[cur_lay-1]
    out_neu_len = len(neuron_out)

    for i in range(out_neu_len):
        neuron_out[i] = 0
        for j in range(in_neu_len):
            weight = cur_lay_weight[i][j]
            neuron_out[i] = neuron_out[i] + (neuron_in[j]*weight)
        # neuron_out[i] = activationF(neuron_out[i]) # функция активации
    

if __name__ == '__main__':
    weight_init (4)
    neural_init (4)
    # print(weight_matrix[0][1][2]) # [слой][n нейрона на слое][значение связи с m нейроном на следующем слое]
    forWards (0)
