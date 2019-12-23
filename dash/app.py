
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

import numpy as np

from simulation import Simulation
from methods import rk4

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

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
    dcc.Slider(
        id = 'v_i',
        min = 0,
        max = 1,
        step = 0.001,
        value = 0.025
    ),
    dcc.Graph(id = 'time-graph', animate = True),
    dcc.Interval(
        id='graph-update',
        interval=0.6*1000,
        n_intervals = 0
    ),
])



sim = Simulation(initial_state = np.array([0, 0.01 , 0.01, 0.01]), h = 0.01, logging_frequency = 100, method = rk4)

@app.callback(
        Output(component_id = 'time-graph', component_property = 'figure'),
        [Input(component_id = 'graph-update', component_property = 'n_intervals')],
        state = [State('v_i', 'value')]
)
def update_plot(n_intervals, v_i):
    global sim

    for i in range(500):
        sim.step({'v_i': v_i})
    
    LAST_N = 100

    t = sim.get_history('t', last_n = LAST_N)

    return {
            'data': [
                {'x': t, 'y': sim.get_history('C', last_n = LAST_N), 'name': 'C'},
                {'x': t, 'y': sim.get_history('M', last_n = LAST_N), 'name': 'M'},
                {'x': t, 'y': sim.get_history('X', last_n = LAST_N), 'name': 'X'},
            ],
            'layout': go.Layout(xaxis=dict(range=[min(t),max(t)]),
                                yaxis=dict(range=[0,1]),)
        }



if __name__ == '__main__':
    app.run_server(debug = True)

