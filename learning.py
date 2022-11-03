from copy import deepcopy
import neural_network
import error_calc
import main
import modul

weight_matrix = neural_network.weight_matrix # импортируем матрицу весов
neural_matrix = neural_network.neural_matrix # импортируем матрицу нейронов
err_matrix = deepcopy(neural_matrix) # проверить копируются значения или ссылки. Нужны значения

learn_k = 0.001 # коофициент обучения

# weight_upd = lambda w, k, nN, nP, de


def learn_program ():
    err_fill_neuromatrix()



def err_fill_neuromatrix ():
    out_err = error_calc.out_err_calc (main.in_stores, main.out_stores)
    neural_network.input_data_upd(modul.item_to_neur(out_err), len(neural_network.neural_matrix)-1, err_matrix)

    for i in range(len(neural_network.neural_matrix)-1,1,-1):
            print(i)
            neural_network.backWards(i, out_err)  

