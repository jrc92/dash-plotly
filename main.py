# [START gae_python37_app]
from flask import Flask
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import os


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
server = Flask(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server = server)

script_dir = os.path.dirname(__file__)
rel_path_1 = 'artworks.csv'
rel_to_cwd_path_1 = os.path.join(script_dir, rel_path_1) 
df_moma_1 = pd.read_csv(rel_to_cwd_path_1, header = 0, index_col = 0)

# assuming that both have the same number of entities/topics

moma_dept = df_moma_1["Department"].unique()

app.layout = html.Div([
    html.H1('The Moma Collection'),
    html.Div([
        html.Div([
            html.P("Filter by Department"),
            dcc.Dropdown(
                id='dept-selection',
                options=[{'label': i, 'value': i} for i in moma_dept],
                value='Architecture & Design'
            )
        ])
    ]),
        dcc.Graph(id = 'moma-dept-time-chart')
])

@app.callback(
    Output('moma-dept-time-chart', 'figure'),
    [Input('dept-selection', 'value')])
 
def update_dept_time(dept):
    dff_dept_pre = df_moma_1[df_moma_1['Department'] == dept]
    dff_dept_pre.dropna(subset = ['Acquisition Date'], inplace = True)
    dff_dept_pre['Year'] = pd.to_datetime(dff_dept_pre['Acquisition Date']).apply(lambda x: x.year)
    dff_dept = dff_dept_pre.groupby('Year')['Title'].count()
    dff_dept = pd.DataFrame(dff_dept)
    return({
        'data': [
            go.Bar(
                x = dff_dept.index, 
                y = dff_dept.Title,
                name = 'count',
                marker = dict(  
                    color = "purple"
                )
            )],
        'layout': go.Layout(
            barmode = 'stack',
            title = 'Number of Art Pieces by Year of Creation: ' + str(dept),
            xaxis = {'title': 'dates'},
            yaxis = {'title': 'art pieces created'}
        )
    })


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run_server(port=8080, debug=True)
# [END gae_python37_app]
