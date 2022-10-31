# описание переменных и правил
# входные данные берутся из вне
# матрица нейронов
from math import exp
from random import random


neural_matrix_init = [3, 3] # сколько нейронов на каждом слое
neural_matrix = [] # двумерный массив с данными всех нейронов [слой][значение нейрона n]
weight_matrix = [] # здесь будут все связи
activationF = lambda x : 1 / (1 + exp(-1 * x))

#обновление входных значений
def input_data_upd (input_data):
    global neural_matrix
    neural_matrix[0] = input_data

# создаём список нейронов с их значениями
def neural_init(input_count, out_count):
    '''Создаёт список значений всех нейронов. требуется количество входных и кол-во выходных данных'''
    global neural_matrix_init
    neural_matrix_init.insert(0, input_count)
    neural_matrix_init.append(out_count)
    global neural_matrix

    n=len(neural_matrix_init)

    neural_matrix = [[0] * neural_matrix_init[i] for i in range(n)]

    weight_init()

    # neural_matrix_init.pop(0)

# первичная инициализация весов (потом сделать хранение в файле)
def weight_init(): 
    '''Создаёт список значений всех весов.'''
    global neural_matrix_init
    # neural_matrix_init.insert(0, input_count)
    global weight_matrix

    for l in range (0,len(neural_matrix_init)-1):
        current_lay = []
        for current_lay_n in range (neural_matrix_init [l]):
            next_lay = []
            for next_lay_n in range (neural_matrix_init [l+1]):
                next_lay.append(random ()) # random () /\ next_lay_n
            current_lay.append(next_lay)
        weight_matrix.append(current_lay)
        # print (weight_matrix)

    # neural_matrix_init.pop(0)
 # создаём многомерный массив связей [номер обрабатываемого слоя[номер нейрона на обрабатываемом слое[номер нейрона на следующем слое]]]                
                                                               # [l1[n1l1[n1l2, n2l2], n2l1[n1l2, n2l2], l2[[n1l1[n1l2, n2l2], n2l1[n1l2, n2l2]]]
                # print (prev_lay, " <-> ", current_lay)

def forWards (cur_lay): 
    '''Прямое распространение. Вводим номер обрабатываемого слоя. Будет использован следующий'''
    global neural_matrix
    global weight_matrix

    neuron_in = neural_matrix[cur_lay]
    neuron_out = neural_matrix[cur_lay+1]
    cur_lay_weight = weight_matrix [cur_lay]

    in_neu_len = len(cur_lay_weight)
    out_neu_len = len(cur_lay_weight[0])

    for i in range(out_neu_len):
        neuron_out[i] = 0
        for j in range(in_neu_len):
            weight = cur_lay_weight[j][i]
            neuron_out[i] = neuron_out[i] + (neuron_in[j]*weight)
        neuron_out[i] = activationF(neuron_out[i]) # функция активации
    

if __name__ == '__main__':
    weight_init (4)
    neural_init (4)
    # print(weight_matrix[0][1][2]) # [слой][n нейрона на слое][значение связи с m нейроном на следующем слое]
    forWards (0)
