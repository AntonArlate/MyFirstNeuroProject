class factory:
    def __init__(self, name:str, f_request:dict, produce:dict):
        self.name = name # имя завода
        self.request = f_request # потребление на 1 цикл
        self.produce = produce # производство на 1 цикл
        self.i_flow = tuple() # Используется для генерации потоков и связывает завод с ними

        self.request_coef = {} # соотношения между потребляемыми ресурсами
        maximum = max(f_request.values())
        for item in f_request:
            self.request_coef[item] = f_request[item] / maximum

        