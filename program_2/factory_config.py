import program_2.factory_ob as factory_ob

in_stores = {}
out_stores = {}
err_out_stor = {}
flow = []
flow_map = {}
flow_map2 = [] # индекс имени ресурса = индексу потока
all_factoty_list : list[factory_ob.factory] = []
err_factory = []


f_name = "f_reinf_iron_plate_1"
f_request = {"iron":12}
f_produce = {"reinf_iron_plate":1}
reinf_iron_plate_1 = factory_ob.factory(f_name, f_request, f_produce)
all_factoty_list.append(reinf_iron_plate_1)

f_name = "f_reinf_iron_plate_2"
f_request = {"iron":5, "copper":3.33}
f_produce = {"reinf_iron_plate":1}
reinf_iron_plate_2 = factory_ob.factory(f_name, f_request, f_produce)
all_factoty_list.append(reinf_iron_plate_2)

f_name = "f_reinf_iron_plate_3"
f_request = {"iron":13.17}
f_produce = {"reinf_iron_plate":1}
reinf_iron_plate_3 = factory_ob.factory(f_name, f_request, f_produce)
all_factoty_list.append(reinf_iron_plate_3)

f_name = "f_rotor_1"
f_request = {"iron":11.25}
f_produce = {"rotor":1}
f_rotor_1 = factory_ob.factory(f_name, f_request, f_produce)
all_factoty_list.append(f_rotor_1)

f_name = "f_rotor_2"
f_request = {"iron":4.33, "copper":2}
f_produce = {"rotor":1}
f_rotor_2 = factory_ob.factory(f_name, f_request, f_produce)
all_factoty_list.append(f_rotor_2)

f_name = "f_rotor_3"
f_request = {"iron":3, "copper":3, "coal":3}
f_produce = {"rotor":1}
f_rotor_3 = factory_ob.factory(f_name, f_request, f_produce)
all_factoty_list.append(f_rotor_3)


def in_store_generator ():
    for fac in all_factoty_list:
        for item in fac.request:
            if item not in in_stores:
                in_stores[item] = [0]
    

def out_store_generator ():
    for fac in all_factoty_list:
        for item in fac.produce:
            if item not in out_stores:
                out_stores[item] = [0]
                

def flow_generator ():
    count = 0
    for fac in all_factoty_list:
        for item in fac.request: # перебираем попорядку все запросы всех заводов
            flow.append(0) # создаём новый поток
            fac.i_flow = fac.i_flow + (count,) # записываем индекс потока в кортеж индексов
            if item not in flow_map: flow_map[item] = [] # создаём итем в карте потоков если требуется
            flow_map[item] = flow_map[item] + [count] # прикрепляем к итему индекс его потока
            flow_map2.append(item)
            count += 1


for fac in all_factoty_list:
    err_factory.append(0)
mine = {"iron":[1], "copper":[1], "coal":[1]}

in_store_generator()
out_store_generator ()
flow_generator ()


flow_change = flow.copy()
err_flow = flow.copy()
temp_flow = flow.copy()

if __name__ == '__main__':

    print(flow)
    print(flow_map)

