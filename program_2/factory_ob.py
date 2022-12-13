class factory:
    def __init__(self, name:str, f_request:dict, produce:dict):
        self.name = name # имя завода
        self.request = f_request # потребление на 1 цикл
        self.produce = produce # производство на 1 цикл
        self.i_flow = tuple() # Используется для генерации потоков и связывает завод с ними
        self.err_request = [] # для записи ошибки запросов. Согласовано с i_flow

        self.request_coef = {} # соотношения между потребляемыми ресурсами
        maximum = max(f_request.values())
        for item in f_request:
            self.request_coef[item] = f_request[item] / maximum

        self.prod_coef = {}
        maximum = max(produce.values())
        for item in produce:
            self.prod_coef[item] = produce[item] / maximum

        