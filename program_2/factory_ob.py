from urllib import request


class factory:
    def __init__(self, name:str, f_request:dict, produce:dict):
        self.name = name
        self.request = f_request
        self.produce = produce
        self.i_flow = tuple()

        self.request_coef = {}
        maximum = max(f_request.values())
        for item in f_request:
            self.request_coef[item] = f_request[item] / maximum

        