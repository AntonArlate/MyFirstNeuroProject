from .factory_config import flow
from .factory_config import flow_change
from .factory_config import flow_map2
from .factory_config import all_factoty_list
from .factory_config import in_stores
from .factory_config import out_stores

in_flow = in_stores.copy()


# перебираем заводы вычисляя сколько фактически они забрали ресурса из потока
def max_consumption():
    global flow
    
    for fac in all_factoty_list:


        request = [x for x in fac.request.values()]
        
        max_cicle = list(map(lambda i_flow, req : flow[i_flow] / req, fac.i_flow, request))
        minimum = min(max_cicle)
        fac.minimum = minimum


        for k, v in fac.produce.items(): # Добавляем сразу в склады продукцию, лучше конечно отдельно сделать

            out_stores[k][0] += (v*minimum)

        for i_flow in fac.i_flow:
            potr = fac.request[flow_map2[i_flow]] * minimum # фактическое потребление ресурса
            in_stores[flow_map2[i_flow]][0] -= potr # вычетаем из in складов
            flow_change[i_flow] = potr - flow[i_flow] # получили смещения потоков

    flow = list(map(lambda a, b : a+b, flow, flow_change)) # изначальный флоу больше не нужен, достаточно информации об изменении
    return flow

def pack_out_to_in():
    global flow

    for k in in_flow.keys():
        in_flow[k] = [0]

    for k, v in zip(flow_map2, flow):
        in_flow[k][0] += v
    
    return in_flow


