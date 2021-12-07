from model import Model
from graphics import *


class Experiment:
    def __init__(self, id_start = 1, num_trials = 5, num_rows = 10, num_cols = 10, wrap = False, num_features = 5, num_traits = 5, onlineness = 0, prop_agent_online = 0, agent_online_val = 0, min_sioa_cnt = 0, max_sioa_cnt = 0, max_frames = 300000, patience = 10000, do_display = False):
        self.id_start = id_start 
        self.num_trials = num_trials
        self.num_rows = num_rows 
        self.num_cols = num_cols 
        self.wrap = wrap 
        self.num_features = num_features 
        self.num_traits = num_traits
        self.onlineness = onlineness
        self.prop_agent_online = prop_agent_online
        self.agent_online_val = agent_online_val
        self.min_sioa_cnt = min_sioa_cnt
        self.max_sioa_cnt = max_sioa_cnt
        self.sioa_descrips = [("min", min_sioa_cnt), ("max", max_sioa_cnt)]
        self.max_frames = max_frames
        self.patience = patience
        self.do_display = do_display

    def __str__(self):
        params = vars(self)
        out = ""
        for key in params: 
           out += f"{key}: {params[key]} "
        return out

    def generate_models(self):
        models = []
        for id in range(self.id_start, self.id_start + self.num_trials):
            model = Model(id = id, num_rows = self.num_rows, num_cols=self.num_cols, num_features = self.num_features, num_traits = self.num_traits, wrap = self.wrap, onlineness=self.onlineness, prop_agent_online=self.prop_agent_online, agent_online_val=self.agent_online_val, sioa_descrips=self.sioa_descrips, do_display=self.do_display)
            models.append(model)
        return models
    
    def get_cat_string(self) -> str:
        # cat_string = f"nF{num_features}nT{num_traits}PAO{prop_agent_online}AOV{agent_online_val}w{wrap_str}o{onlineness}nR{num_rows}nC{num_cols}"
        # return f"nF{self.num_features}nT{self.num_traits}nS_min{self.min_sioa_cnt}max{self.max_sioa_cnt}PAO{self.prop_agent_online}AOV{self.agent_online_val}"
       return f"nF{self.num_features}nT{self.num_traits}nS_min{self.min_sioa_cnt}max{self.max_sioa_cnt}PAO{self.prop_agent_online}AOV{self.agent_online_val}mf{self.max_frames}"
    
   

