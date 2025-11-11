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

# 替代的跳转回调 - 直接监听数据存储的变化
@app.callback(
    Output('url', 'pathname'),
    Input('uploaded-data-store', 'data'),
    State('submit-csv', 'n_clicks'),
    State('submit-db', 'n_clicks'),
    State('submit-url', 'n_clicks'),
    prevent_initial_call=True
)
def redirect_when_data_ready(data, csv_clicks, db_clicks, url_clicks):
    # 如果有数据并且有任一按钮被点击过，则跳转
    if data and len(data) > 0 and (csv_clicks or db_clicks or url_clicks):
        print(f"数据已准备就绪，跳转到处理页面，数据长度: {len(data)}")
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
