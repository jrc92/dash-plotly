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

moma_dept = df_moma_1["Department"].unique()[:-2]

app.layout = html.Div([
    html.H1('The MoMa Collection'),
    html.Div([
        html.Div([
            html.P("Filter by Department:"),
            dcc.Dropdown(
                id='dept-selection',
                options=[{'label': i, 'value': i} for i in moma_dept],
                value='Architecture & Design'
            )
        ])
    ]),
        dcc.Graph(id = 'moma-dept-time-chart'),
        html.Div([
            html.Div([
                dcc.Graph(id = 'moma-dept-dim-chart'),
            ], className = 'six columns'),
            html.Div([
                dcc.Graph(id = 'moma-dept-artist-chart')
            ], className = 'six columns')
        ], className = 'row')
])

@app.callback(
    Output('moma-dept-time-chart', 'figure'),
    [Input('dept-selection', 'value')])
 
def update_dept_time(dept):
    dff_dept_pre = df_moma_1[df_moma_1['Department'] == dept]
    dff_dept_pre.dropna(subset = ['Acquisition Date'], inplace = True)
    dff_dept_pre['Year'] = pd.to_datetime(dff_dept_pre['Acquisition Date'], errors = 'coerce').apply(lambda x: x.year)
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
            title = 'Number of Art Pieces by Year of Creation: ' + str(dept),
            xaxis = {'title': 'dates'},
            yaxis = {'title': 'art pieces created'}
        )
    })

@app.callback(
    Output('moma-dept-dim-chart', 'figure'),
    [Input('dept-selection', 'value')])
 
def update_dept_dim(dept):
    dff_dept = df_moma_1[df_moma_1['Department'] == dept]
    return({
        'data': [
            go.Scatter(
                x = dff_dept['Width (cm)'], 
                y = dff_dept['Height (cm)'],
                mode = 'markers',
                name = 'data',
                marker = dict(  
                    color = "blue"
                )
            )],
        'layout': go.Layout(
            title = 'Art Pieces by Width (cm) and Height (cm): ' + str(dept),
            xaxis = {'title': 'Width (cm)'},
            yaxis = {'title': 'Height (cm)'}, 
            font = dict(size = 8)
        )
    })

@app.callback(
    Output('moma-dept-artist-chart', 'figure'),
    [Input('dept-selection', 'value')])
 
def update_dept_artist(dept):
    dff_dept_pre = df_moma_1[df_moma_1['Department'] == dept]
    dff_dept_artist = dff_dept_pre['Name'].value_counts()[:20]
    return({
        'data': [
            go.Bar(
                x = dff_dept_artist.index, 
                y = dff_dept_artist.values,
                name = 'count',
                marker = dict(  
                    color = "orange"
                )
            )],
        'layout': go.Layout(
            title = 'Top 20 Artists: ' + str(dept),
            xaxis = {'title': 'Artists'},
            yaxis = {'title': 'Number of Art Pieces'}, 
            font = dict(size = 8)
        )
    })


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run_server(port=8080, debug=True)
# [END gae_python37_app]
