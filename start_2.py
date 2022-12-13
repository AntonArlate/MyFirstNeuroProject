from queue import Queue
import threading
from time import sleep
from first_UI.UI_init import start_pyqt
import program_2.factory_config as factory_config
from program_2.factory_config import in_stores
from program_2.factory_config import flow
from program_2.FactoryCalc import max_consumption
from program_2.FactoryCalc import pack_out_to_in
import neural_network_v2.learning as learning



# import neural_network.network as network
import program_1.modul as modul

from neural_network_v2 import network


calc_starting = True
itera = 0


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

    learning.neuron_matrix = neuron_matrix

# рассчитываем сколько в какой поток направила ресурсов нейросеть

# пропускаем запасы складов через функцию активации чтобы потом использовать как множитель потребления
temp_in_stores = {}
def resource_flow():
    excess = 0.2  # на сколько мы можем привышать потребление
    a = 10000  # чем больше значение, тем больше будет накапливаться буфера в складах (будет стремиться к этому значению)
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
    out_neural_data = neuron_matrix.get_data(len(neuron_matrix.all_layers)-1)
    # print (out_neural_data)
    for item in factory_config.flow_map:
        sum_out_neural = 0
        for i in factory_config.flow_map[item]:
            sum_out_neural += out_neural_data[i]
        for i in factory_config.flow_map[item]:
            flow[i] = (out_neural_data[i] / sum_out_neural) * temp_in_stores[item][0]


# запускаем цикл нейросети
def cycle_run():
    
    global flow
    count = 1
    for i in range(1):
        count += 1
        store_filling(in_stores, factory_config.mine)  # наполняем склады

        neuron_matrix.data_upd (modul.in_data_to_neur(modul.item_to_neur(in_stores)), 0) # записываем во входные нейроны значения скаладов пропущеные через нормализатор
        for j in range(len(neuron_matrix.all_layers) - 1):  # проходимся по сети функцией прямого распространения.
            # На выходе получаем значения потоков 0,0..1,0
            neuron_matrix.forWards(j)
        
        # рассчитываем сколько в какой поток направила ресурсов нейросеть 
        resource_flow()
        flow_calc()
        # запрашиваем калькуляцию у заводов. Данные уже у них в листе "flow"
        flow = max_consumption() # после этого на flow записывается сколько фактически забрали заводы, избыточные остаются. В дальнейшем избыток будет генерировать отрицательную ошибку
        # store_filling(in_stores, pack_out_to_in(), "-") # вычитаем из складов, то что взяли заводы/ больше не надо, заводы сами вычитают при калькуляции
        # генерируем ошибку заводов. Состоит из:
        # + ошибка складов out если выходов несколько пропорционально умножаем каждый
        factory_config.err_out_stor = modul.maximal_alignment(factory_config.out_stores)
        factory_config.err_out_stor = modul.midle_shift(factory_config.err_out_stor, 1) # получаем ошибку согласно заполненности

        # доп. средняя ошибка пропорции ресурсов. Если один ресурс = 1 другой 2, но второй из-за первого был использован лишь 1, то средняя = 1,5
        
        for fac in factory_config.all_factoty_list:
            temp_arr = []
            for i in fac.i_flow: # берём карту нейронов завода
                temp_arr.append(factory_config.flow_change[i]) # по ней по сдвигу вычисляем ошибку
            fac.err_request = modul.midle_shift(temp_arr, 1)

        # прим у нас есть flow (сколько было израсходовано), minimum (в max_consumption(), склько было сделано циклов), flow_change (то на сколько изменились от исходного расчёта)
        # + на каждый поток передаём ошибку складов + соответствующего ресурса

        for fac in factory_config.all_factoty_list:
            for i, err_req in zip(fac.i_flow, fac.err_request):
                factory_config.err_flow[i] = err_req + factory_config.err_out_stor[list(fac.produce.keys())[0]][0] #пока расчитываем на 1 продукцию

        # считаем ошибку in складов (чем больше запас, тем больше ошибка)
        temp_modle_shift = modul.midle_shift(modul.maximal_alignment(in_stores), -1)
        for item in factory_config.flow_map:
            temp_sum = 0
            for i in factory_config.flow_map[item]:
                temp_sum += flow[i]

            for i in factory_config.flow_map[item]:
                factory_config.temp_flow[i] = flow[i] / temp_sum * temp_modle_shift[item][0]
        # ошибка in складов записана в factory_config.temp_flow (массив нейронов)
        # финализируем ошибку
        # берём ошибку складов в виде уже последовательности неронов
        # берем ошибку фактори
        # теперь сливаем сумму на еррор слой
        errArray = neuron_matrix.get_data(len(neuron_matrix.all_layers)-1, True)
        for i in range(len(errArray)):
            errArray[i] = factory_config.temp_flow[i] + factory_config.err_flow[i]
        neuron_matrix.data_upd(errArray,len(neuron_matrix.all_layers)-1, True)

        for j in range(len(neuron_matrix.all_layers) - 1, 0, -1):  # проходимся по сети функцией обратного распространения
            neuron_matrix.backWards(j)
        #запускаем модуль обучения
        learning.learn_program()

        #region тестовый вывод
        global itera
        print("\033[H\033[J")
        itera += 1
        # factory_config.out_stores['reinf_iron_plate'][0] -= 2
        # factory_config.out_stores['rotor'][0] -= 1

        print("итерация - ", itera)

        print("\nмайнинг")
        print(factory_config.mine)

        print("\nсклады сырья")
        print(factory_config.in_stores)

        print("\nсклады продукции")
        print(factory_config.out_stores)

        print("\nактивность фактори циклов")
        for fac in factory_config.all_factoty_list:
            print(fac.name)
            print([factory_config.flow_map2[x] for x in fac.i_flow], " - " , fac.minimum)
        #endregion
        

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
        sleep(1)
        if calc_starting:
            thr_1 = threading.Thread(target=cycle_run)
            thr_1.start()
            thr_1.join()     

def not_thread_runner():
    initialized()      

if __name__ == '__main__':
    thread_runner()