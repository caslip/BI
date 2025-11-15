# Import packages
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input, ctx, State, ALL, MATCH
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
from components.import_file import sidebar, SIDEBAR_STYLE
from components.workshop import workshop
import uuid # Required for test.py logic

# Initialize main application
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

default_content = dbc.Container([
    html.Div([sidebar], id="sidebar-div"),
    html.Div([
        html.H3(children="Initial Title"),
        html.P("Please use the sidebar to import data to start the analysis."),
    ], style={"margin-left": "18rem", "padding": "2rem 1rem"}, id="content-div"),
], fluid=True, id="main-container")

workshop_content = dbc.Container([
    workshop
], fluid=True, id="workshop-container")

# Application layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=True),  # refresh=True will completely refresh the page
    dcc.Store(id="uploaded-data-store", storage_type="session"),     # Used to share data between pages
    html.Div(id='page-content')
])

# 替代的跳转回调 - 直接监听数据存储的变化
@app.callback(
    Output('url', 'pathname'),
    Input('uploaded-data-store', 'data'),
    prevent_initial_call=True
)
def redirect_when_data_ready(data):
    # If there is data, then redirect
    if data and len(data) > 0:
        print(f"Data is ready, redirecting to processing page, data length: {len(data)}")
        return '/process'
    
    return dash.no_update

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/':
        return default_content
    elif pathname == '/process':
        return workshop
    else:
        return default_content


# Run application
if __name__ == '__main__':
    app.run(debug=True)
