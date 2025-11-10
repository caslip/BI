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

# 创建示例数据 (原始数据保留，尽管在test.py应用中未直接使用)
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# 初始化主应用
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

default_content = dbc.Container([
    html.Div([sidebar], id="sidebar-div"),
    html.Div([
        html.H3(children="初始标题"),
        html.P("请使用左侧边栏导入数据以开始分析。"),
    ], style={"margin-left": "18rem", "padding": "2rem 1rem"}, id="content-div"),
], fluid=True, id="main-container")

workshop_content = dbc.Container([
    workshop
], fluid=True, id="workshop-container")

# 应用布局
app.layout = html.Div([
    dcc.Location(id='url', refresh=True),  # refresh=True 会完全刷新页面
    dcc.Store(id="uploaded-data-store", storage_type="session"),     # 用于在页面间共享数据
    html.Div(id='page-content')
])

@app.callback(
    Output('url', 'pathname'),  # 同时更新Store和跳转URL
    Input('close-modal', 'n_clicks'),
    State('uploaded-data-store', 'data'),
    prevent_initial_call=True
)
def process_data_and_redirect(n_clicks, data):
    if n_clicks > 0 and data is not None:
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


# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
