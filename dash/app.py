
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

import numpy as np

from simulation import Simulation
from methods import rk4

parameters_list = [
    'v_i',       
    'v_d',       
    'K_d',
    'k_d',
    'K_c',
    'V_M1',
    'K_1',
    'V_2',
    'K_2',
    'V_M3',
    'K_3',
    'V_4',
    'K_4'
    ]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

sliders_list = [dcc.Slider(id = parameter, min = 0, max = 1, step = 0.01, value = 0.05) for parameter in parameters_list]


app.layout = html.Div(children = [
    html.H1(children = 'Mitotic oscilator'),
    html.Div(children = 'A mitotic oscilator demo'),
    dcc.Slider(
        id = 'C_init',
        min = 0,
        max = 1,
        step = 0.01,
        value = 0.5
    ),
    html.Div(children = sliders_list),
    dcc.Graph(id = 'time-graph', animate = True),
    dcc.Interval(
        id='graph-update',
        interval=0.6*1000,
        n_intervals = 0
    ),
])

input_list = [Input(component_id = parameter, component_property = 'value') for parameter in parameters_list]

@app.callback(
        Output(component_id = 'time-graph', component_property = 'figure'),
        input_list
        # state = [State('v_i', 'value')]
)
def update_plot(*param_values):
    sim = Simulation(initial_state = np.array([0, 0.01 , 0.01, 0.01]), h = 0.01, logging_frequency = 100, method = rk4)
    parameters_dict = {key: parameter for key, parameter in zip(parameters_list, param_values)}

    for i in range(10000):
        sim.step(parameters_dict)
    
    t = sim.get_history('t')

    return {
            'data': [
                {'x': t, 'y': sim.get_history('C'), 'name': 'C'},
                {'x': t, 'y': sim.get_history('M'), 'name': 'M'},
                {'x': t, 'y': sim.get_history('X'), 'name': 'X'},
            ],
        }



if __name__ == '__main__':
    app.run_server(debug = True)

