
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

import numpy as np
import pandas as pd

from simulation import Simulation
from methods import rk4

parameters_table = pd.read_csv('parameters.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

def generate_control_elements(parameters_table):
    master_list = []

    for group in parameters_table.group.unique():
        group_list = []
        group_list.append(html.Summary(children = group))

        param_table_selection = parameters_table[parameters_table.group == group]

        for index, row in param_table_selection.iterrows():
            group_list.append(dcc.Markdown(dangerously_allow_html = True,
                                                children = row['label']))
            group_list.append(dcc.Slider(id = row['id'], min = row['min'], max = row['max'], step = row['step'], value = row['default']))

        master_list.append(html.Details(children = group_list))

    return master_list

app.layout = html.Div(children = [
    html.H1(children = 'Mitotic oscilator'),
    html.Div(children = 'A mitotic oscilator demo'),
    html.Div(children = generate_control_elements(parameters_table), style = {}),
    dcc.Graph(id = 'time-graph', animate = True),
    dcc.Interval(
        id='graph-update',
        interval=0.6*1000,
        n_intervals = 0
    ),
])

input_list = [Input(component_id = parameter, component_property = 'value') for parameter in parameters_table['id']]

@app.callback(
        Output(component_id = 'time-graph', component_property = 'figure'),
        input_list
        # state = [State('v_i', 'value')]
)
def update_plot(*param_values):
    sim = Simulation(initial_state = np.array([0, 0.01 , 0.01, 0.01]), h = 0.01, logging_frequency = 100, method = rk4)
    parameters_dict = {key: parameter for key, parameter in zip(parameters_table['id'], param_values)}

    for i in range(10000):
        sim.step(parameters_dict)
    
    t = sim.get_history('t')

    return {
            'data': [
                {'x': t, 'y': sim.get_history('C'), 'name': 'C'},
                {'x': t, 'y': sim.get_history('M'), 'name': 'M'},
                {'x': t, 'y': sim.get_history('X'), 'name': 'X'},
            ],
            # 'layout': go.Layout(yaxis=dict(range = [0,1]))
            
        }



if __name__ == '__main__':
    app.run_server(debug = True)

