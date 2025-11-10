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
    dcc.Store(id="uploaded-data-store", storage_type="session"),
    html.Div([sidebar], id="sidebar-div"),
    html.Div([
        html.H3(children="初始标题"),
        html.P("请使用左侧边栏导入数据以开始分析。"),
    ], style={"margin-left": "18rem", "padding": "2rem 1rem"}, id="content-div"),
], fluid=True, id="main-container")

# 应用布局
app.layout = html.Div([
    default_content,
],
    id="app-div"
)


# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
