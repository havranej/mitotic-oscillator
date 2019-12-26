
import pandas as pd
import numpy as np
from methods import rk4
from mitotic_oscilator import mitotic_oscilator

class Simulation():
    def __init__(self, initial_state, h = 0.01, method = rk4, logging_frequency = 100):
        self.history = pd.DataFrame(data = np.expand_dims(initial_state, axis = 0),
                                    columns = ['t', 'C', 'M', 'X'],
                                    index = [0])
        self.state = initial_state
        
        self.h = h
        self.method = method
        self.logging_frequency = logging_frequency
        self.log_counter = 0
        
    def step(self, params = {}):
        self.state = self.method(self.state, mitotic_oscilator, self.h, params)
        self.state = np.maximum(self.state, 0)

        self.log_counter += 1
        
        if self.log_counter == self.logging_frequency:
            self.add_current_state_to_history()
            self.log_counter = 0
            
        
    def add_current_state_to_history(self):
        self.history = self.history.append(dict(zip(self.history.columns, self.state)), ignore_index = True)

    def get_history(self, variable, last_n = None):
        if last_n is not None:
            return self.history[variable][-last_n:]
        else:
            return self.history[variable]
