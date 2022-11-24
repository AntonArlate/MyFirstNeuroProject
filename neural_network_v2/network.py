
from math import exp
from random import random
# from global_val import neuron_matrix
# from .global_val import neuron_matrix


activationF = lambda x : 1 / (1 + exp(-1 * x))
neuron_scheme = [3, 4]
bias_map = [True, True, True, False]



class neuron:
    # def __init__(self, name:str, f_request:dict, produce:dict):
    def __init__(self):
        self.layer = None
        self.value = 1
        self.error_value = 1
        self.link_prev = []
        self.link_next = []
        self.its_bias = False

class neuron_layer:   
    def __init__(self):
        self.neurons = []


class link_neuron:
    def __init__(self, layer, first_neuron:neuron, second_neuron:neuron):
        self.value = random ()
        self.link_layer = layer
        self.first_neuron = first_neuron
        self.second_neuron = second_neuron

        first_neuron.link_next.append((self, second_neuron))
        second_neuron.link_prev.append((self, first_neuron))

class NeuronMatrix:
    def __init__(self, neural_matrix_init:list):    

        self.all_layers: neuron_layer = [] 
        self.all_neurons: neuron = []
        self.all_links: link_neuron = []

        for layer, neuron_total in enumerate(neural_matrix_init):
            neuron_total += bias_map[layer]
            self.all_neurons.append([])
            self.all_layers.append(neuron_layer())
            for i in range(neuron_total):
                n = neuron()
                n.layer = layer
                self.all_layers[layer].neurons.append(n)
                self.all_neurons[layer].append(n)
                if i == 0:
                    n.its_bias = bias_map[layer]

        for l in range(len(self.all_layers)):
            if l < len(self.all_layers)-1:
                self.all_links.append([])
                for first in self.all_layers[l].neurons:
                    for second in self.all_layers[l+1].neurons:
                        if not second.its_bias:
                            link = link_neuron(l, first, second)
                            self.all_links[l].append(link)


    def get_data (self, cur_lay, err = False):
        '''извлекает последовательные значения нейронов в слое (смещение не фильтруется)'''
        cur_lay : neuron = self.all_neurons[cur_lay]
        return list(map(lambda val: val.value, cur_lay))


    def data_upd (self, in_data, cur_lay, err = False):
        '''Запись данных на указанный слой нейронов \nerr - да/нет на слой ошибок'''
        cur_lay : neuron = [x for x in self.all_neurons[cur_lay] if not x.its_bias]

        for neu, data in zip(cur_lay, in_data):
            if neu.its_bias: continue
            if err:
                neu.err_value = data
            else:
                neu.value = data

      
    def forWards (self, cur_lay): 
        '''Прямое распространение. Вводим номер обрабатываемого слоя. Будет расчитан следующий'''
        neuron_out : neuron = self.all_layers[cur_lay+1].neurons
        for out_n in neuron_out:
            if out_n.its_bias: continue
            out_n.value = 0
            for p_link in out_n.link_prev:
                out_n.value += (p_link[0].value*p_link[1].value)
            out_n.value = activationF(out_n.value) # функция активации
            # print(out_n.value)


    def backWards (self, cur_lay, err = True): 
        '''обрвтное распространение. Вводим номер обрабатываемого слоя. Будет расчитан предыдущий.
         \nerr - записывать на слой ошибок. По умолчанияю True. Иначе на основной слой'''

        neuron_out : neuron = self.all_layers[cur_lay-1].neurons

        for out_n in neuron_out:
            if err:
                out_n.error_value = 0 # записываем на выходной нейрон 0
                for p_link in out_n.link_next:
                    if p_link[1].its_bias: continue
                    out_n.error_value += (p_link[0].value * p_link[1].error_value)
            else:
                out_n.value = 0 # записываем на выходной нейрон 0
                for p_link in out_n.link_next:
                    if p_link[1].its_bias: continue
                    out_n.value += (p_link[0].value * p_link[1].value)







if __name__ == '__main__':
    
    neuron_matrix = NeuronMatrix([3, 4, 5])
    neuron_matrix.forWards(0)
    neuron_matrix.backWards(2)
    print(neuron_matrix.all_layers[0].neurons[1].value)
    neuron_matrix.data_upd([1,2,3],0)
    print(neuron_matrix.all_layers[0].neurons[1].value)
    print()
    print(neuron_matrix.get_data(0))

    # print (matrix.all_layers.neurons)

    

        

            
            


    # l = neuron_layer
    # n = neuron
    # n.layer = l

    # print(l.a)
    # print(n.layer.a)