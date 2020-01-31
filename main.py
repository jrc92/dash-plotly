# [START gae_python37_app]
from flask import Flask
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import chart_studio.plotly as py
import squarify
from dash.dependencies import Input, Output
from textwrap import dedent
from flask import jsonify

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
server = Flask(__name__)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server = server)

df_emo = pd.read_csv("/home/jiarongchua92/dash-plotly/consol_all_emotions_2018.csv", header = 0, index_col = 0)

# assuming that both have the same number of entities/topics

entities_emo = df_emo["entity"].unique()

emotions = ['love', 'happy', 'lol', 'surprised', 'sad', 'angry']

app.layout = html.Div([
    html.Div([
        html.Label("Choose an Entity"),
        dcc.Dropdown(
            id = 'entity-selection',
            options = [{'label': i, 'value': i} for i in entities_emo],
            value = 'hsbc'
        )
    ]),        
        dcc.Graph(id = 'emotion-time-bar')
    ])

@app.callback(
    Output('emotion-time-bar', 'figure'),
    [Input('entity-selection', 'value')])
 
def update_emotions_time(entity_name):
    dff_emo_pre = df_emo[df_emo['entity'] == entity_name]
    dff_emo_pre['dates'] = pd.to_datetime(dff_emo_pre.dates)
    emotions = ['love', 'happy', 'lol', 'surprised', 'sad', 'angry']
    dff_emo = dff_emo_pre.groupby('dates')[emotions].sum()
    return({
        'data': [
            go.Bar(
                x = dff_emo.index, 
                y = dff_emo["love"],
                name = "love",
                marker = dict(
                    color = "purple"
                )
            ),
            go.Bar(
                x = dff_emo.index,
                y = dff_emo["happy"],
                name = "happy",
                marker = dict(
                    color = "orange"
                )
            ),
            go.Bar(
                x = dff_emo.index,
                y = dff_emo["lol"],
                name = "lol",
                marker = dict(
                    color = "green"
                )
            ),
            go.Bar(
                x = dff_emo.index,
                y = dff_emo["surprised"],
                name = "surprised",
                marker = dict(
                    color = "yellow"
                )
            ),
            go.Bar(
                x = dff_emo.index,
                y = dff_emo["sad"],
                name = "sad",
                marker = dict(
                    color = "blue"
                )
            ),
            go.Bar(
                x = dff_emo.index,
                y = dff_emo["angry"],
                name = "angry",
                marker = dict(
                    color = "red"
                )
            )
        ],
        'layout': go.Layout(
            barmode = 'stack',
            title = 'News Reaction across Time for ' + str(entity_name),
            xaxis = {'title': 'dates'},
            yaxis = {'title': 'emotion counts'}
        )
    })

@server.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello! Welcome to my dashboard!'

@server.route('/name/<value>')
def name(value):
    val = {"value": value}
    return jsonify

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run_server(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]