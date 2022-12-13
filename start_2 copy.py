from queue import Queue
import threading
from time import sleep
from first_UI.UI_init import start_pyqt
import program_2.factory_config as factory_config
from program_2.factory_config import in_stores
from program_2.factory_config import flow

# import neural_network.network as network
import program_1.modul as modul

from neural_network_v2 import network


calc_starting = True


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
                    stores[item] = list(map(lambda x, y: x - y, stores[item], fill_value[item]))
                else:
                    stores[item] = list(map(lambda x, y: x + y, stores[item], fill_value[item]))


def initialized():   
    # запуск
    # инициализируем нейроны
    global neuron_matrix

    neural_config = network.neuron_scheme.copy()  # схема перцептрона хранится в модуле нейросети
    neural_config.insert(0, len(in_stores))  # входными нейронами будут in_stores
    neural_config.append(len(factory_config.flow))  # выходными нейронами будут потоки
    neuron_matrix = network.NeuronMatrix(neural_config)  # передаём получившуюся схему в конструктор нейрсети. Сохраняем ссылку на результат


# рассчитываем сколько в какой поток направила ресурсов нейросеть

# пропускаем запасы складов через функцию активации чтобы потом использовать как множитель потребления
temp_in_stores = {}
def resource_flow():
    excess = 0.1  # на сколько мы можем привышать потребление
    a = 20  # чем больше значение, тем больше будет накапливаться буфера в складах (будет стремиться к этому значению)
    for item in in_stores:
        temp = in_stores[item][0] / a
        if temp > 1:
            temp = 1
        temp_in_stores[item] = [temp + excess]
        # изначально потребление будет стремиться к приходу ресурсов.
        # перемнажаем приход на полученые коофициенты запасов
        temp_in_stores[item] = [temp_in_stores[item][0] * factory_config.mine[item][0]]


# расчитываем сколько ресурса пришло в поток
def flow_calc():
    out_neural_data = network.neural_matrix[len(network.neural_matrix) - 1]
    # print (out_neural_data)
    sum_out_neural = sum(out_neural_data)
    for item in factory_config.flow_map:
        for i in factory_config.flow_map[item]:
            flow[i] = (out_neural_data[i] / sum_out_neural) * temp_in_stores[item][0]


# запускаем цикл нейросети
def cycle_run():
    count = 1
    for i in range(2):
        count += 1
        store_filling(in_stores, factory_config.mine)  # наполняем склады

        neuron_matrix.data_upd (modul.in_data_to_neur(modul.item_to_neur(in_stores)), 0) # записываем во входные нейроны значения скалодов пропущеные через нормализатор
        for j in range(len(network.neural_matrix) - 1):  # проходимся по сети функцией прямого распространения.
            # На выходе получаем значения потоков 0,0..1,0
            network.forWards(j)

        # рассчитываем сколько в какой поток направила ресурсов нейросеть 
        resource_flow()
        flow_calc()

# запускаем потоки
def thread_runner():
    initialized()

    q = Queue()
    print("инициализация UI")
    q.put("инициализация UI")
    thr_2 = threading.Thread(target=start_pyqt, args=("pyqt", q))
    thr_2.start()
    q.join()
    print("UI загружен")

    while thr_2.is_alive():
        if calc_starting:
            thr_1 = threading.Thread(target=cycle_run)
            thr_1.start()
            sleep(2)
            thr_1.join()      

def not_thread_runner():    
    initialized() 
    cycle_run()

if __name__ == '__main__':
    thread_runner()