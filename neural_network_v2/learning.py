import neural_network_v2.network as network

learn_k = 0.001 # коофициент обучения

derivativeF = lambda y : y * (1 - y)
weight_upd = lambda w, k, nN, inN, nN_val : (w + k * nN * derivativeF(nN_val) * inN)
# w = старое значение веса
# k = коофициент обучения
# nN = neuronNext = ошибка следующего за весом нейрона (выход)
# inN = входной сигнал (с предыдущего нейрона) (вход) (либо входные данные)
# de = производная функции активации
# nN_val = значение выхода выходного нейрона

neuron_matrix : network.NeuronMatrix = None

def learn_program ():
    all_Links = neuron_matrix.all_links
    
    for link_lay in all_Links: # перебираем слои связей
        for cur_link in link_lay: # перебираем отдельные связи в слоях
            cur_link.value = weight_upd(
                cur_link.value, 
                learn_k, 
                cur_link.second_neuron.error_value, 
                cur_link.first_neuron.value, 
                cur_link.second_neuron.value)


