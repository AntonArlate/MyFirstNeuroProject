from copy import deepcopy
import neural_network.network as network
import neural_network.error_calc as error_calc
import program_1.modul as modul

from program_1.global_data import in_stores
from program_1.global_data import out_stores

weight_matrix = network.weight_matrix # импортируем матрицу весов
neural_matrix = network.neural_matrix # импортируем матрицу нейронов
err_matrix = deepcopy(neural_matrix) # проверить копируются значения или ссылки. Нужны значения

learn_k = 0.01 # коофициент обучения

derivativeF = lambda y : y * (1 - y)
weight_upd = lambda w, k, nN, inN, nN_val : (w + k * nN * derivativeF(nN_val) * inN)
# w = старое значение веса
# k = коофициент обучения
# nN = neuronNext = ошибка следующего за весом нейрона (выход)
# inN = входной сигнал (с предыдущего нейрона) (вход) (либо входные данные)
# de = производная функции активации
# nN_val = значение выхода выходного нейрона



def learn_program ():
    err_fill_neuromatrix() # получили матрицу ошибок в err_matrix
    for a in range(len(weight_matrix)):
        for b in range(len(weight_matrix[a])): 
            for c in range(len(weight_matrix[a][b])): 
                if -0.01 > weight_matrix[a][b][c] < 0: weight_matrix[a][b][c] -= 0.0001 # сдвиг от затухания
                if 0 > weight_matrix[a][b][c] < 0.01: weight_matrix[a][b][c] += 0.0001
                weight_matrix[a][b][c] = weight_upd(weight_matrix[a][b][c], learn_k, err_matrix[a+1][c], neural_matrix[a][b], neural_matrix[a+1][c])


def err_fill_neuromatrix ():
    out_err = error_calc.out_err_calc (in_stores, out_stores) # получаем ошибки выхода
    network.input_data_upd(modul.item_to_neur(out_err), len(network.neural_matrix)-1, err_matrix) # передаём ошибки выхода в матрицу ошибок

    # заполняем матрицу ошибок    
    # print(err_matrix)
    for i in range(len(network.neural_matrix)-1,1,-1): 
            network.backWards(i, err_matrix)  


