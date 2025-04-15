from param import Param

class ParamManager:
    def __init__(self, api_instance):
        self.params = []
        self.api = api_instance

    def add_param_list(self, params):
        for p in params:
            self.add_param(p.name, p.wave_type, p.min_val, p.max_val)

    #todo only initiaze the param object. Either that object makes/ updates the param in vtube studio. Or we have an update function here
    def add_param(self, name, wave_type, min_val, max_val):
        param = Param(name, wave_type, min_val, max_val)
        self.params.append(param)
        self.api.create_param(param.name, param.min, param.max)  # Optional hook for API to know
        # todo add update functionality

    def get_all_waves(self):
        return [param.wave for param in self.params]
    
    def get_all_params(self):
        return self.params