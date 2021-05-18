import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from flask import Flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


external_stylesheets = [dbc.themes.BOOTSTRAP]

flask_app = Flask(__name__)
app = dash.Dash(__name__, server=flask_app, external_stylesheets=external_stylesheets)
app.title = 'Bee Colonies'
df = pd.read_csv("intro_bees.csv")

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)

app.layout = html.Div([

    html.H1("Méhek pusztulása az USA-ban az ázsai méhetkák által", style={'text-align': 'center'}),

    dcc.Dropdown(id="select_year",
                 options=[
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018}],
                 multi=False,
                 value=2015,
                 style={'width': "45%", 'font-weight': "bold"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='bee_bar', figure={})

])

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='bee_bar', component_property='figure')],
    [Input(component_id='select_year', component_property='value')]
)
def update_graph(option_selected):    

    container = "Kiválasztott év: {}".format(option_selected)

    dff = df.copy()
    dff = dff[dff["Year"] == option_selected]
    dff = dff[dff["Affected by"] == "Varroa_mites"]

    fig = px.bar(
        data_frame=dff, 
        x='State', 
        y='Pct of Colonies Impacted',
        color='Pct of Colonies Impacted')

    return container, fig


if __name__ == '__main__':
    app.run_server(debug=True)