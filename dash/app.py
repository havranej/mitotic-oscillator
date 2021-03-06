
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

import numpy as np
import pandas as pd

from simulation import Simulation
from methods import rk4

parameters_table = pd.read_csv('parameters.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.GRID]

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

def generate_control_elements(parameters_table):
    master_list = []

    for group in parameters_table.group.unique():
        group_list = []
        group_list.append(html.Summary(children = group))

        param_table_selection = parameters_table[parameters_table.group == group]

        for index, row in param_table_selection.iterrows():
            slider_label = dcc.Markdown(dangerously_allow_html = True,
                                            children = row['label'])
            marks_dict = {i: str(round(i, ndigits = 4)) for i in np.linspace(row['min'], row['max'], num = 5)}
            slider = dcc.Slider(id = row['id'],
                                    min = row['min'],
                                    max = row['max'],
                                    step = row['step'],
                                    value = row['default'],
                                    marks = marks_dict)
            group_list.append(dbc.Row([dbc.Col(slider_label, width = 1), dbc.Col(slider, width = 10)]))
            

        master_list.append(html.Details(children = group_list))

    return master_list


app.layout = html.Div(children = [
    html.H1(children = 'Mitotic oscilator'),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div(children = generate_control_elements(parameters_table), style = {})
            ], width = 4),
            dbc.Col([
                dcc.Graph(id = 'time-graph', animate = True)
            ], width = 8)
        ])
    ], fluid = True)
])

input_slider_list = [Input(component_id = parameter, component_property = 'value') for parameter in parameters_table['id']]

@app.callback(
        Output(component_id = 'time-graph', component_property = 'figure'),
        input_slider_list
)
def update_plot(*param_values):
    parameters_dict = {key: parameter for key, parameter in zip(parameters_table['id'], param_values)}

    step = 10**parameters_dict['h']
    logging_frequency = 10**parameters_dict['log_f']

    sim = Simulation(initial_state = np.array([0, parameters_dict['C_init'] , parameters_dict['M_init'], parameters_dict['X_init']]), 
                        h = step, logging_frequency = logging_frequency, method = rk4)

    for i in range(int(100 / step)):
        sim.step(parameters_dict)
    
    t = sim.get_history('t')

    return {
            'data': [
                {'x': t, 'y': sim.get_history('C'), 'name': 'Cyclin'},
                {'x': t, 'y': sim.get_history('M'), 'name': 'CDC2 kinase'},
                {'x': t, 'y': sim.get_history('X'), 'name': 'Cyclin protease'},
            ],
            'layout': {
                'xaxis': {'title': 'Time (min)'},
                'yaxis': {'title': 'Cyclin concentration (μM) || Fraction of active kinase/protease',
                          'range': [0,1]}
                }
            # 'layout': go.Layout(yaxis=dict(range = [0,1]))
            
        }


if __name__ == '__main__':
    app.run_server(debug = True)

