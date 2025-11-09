# Import packages
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input, ctx
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
from components import sidebar, SIDEBAR_STYLE


# 创建示例数据
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# 初始化应用
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# 应用布局
app.layout = dbc.Container([
    html.Div([sidebar], id="sidebar-div"),
    html.Div([
        html.H3(children="初始标题"),
        html.P("请使用左侧边栏导入数据以开始分析。"),
    ], style={"margin-left": "18rem", "padding": "2rem 1rem"}, id="content-div"),
], fluid=True, id="main-container"
)

@callback(
    Output("main-container", "children"),
    Output("sidebar-div", "style"),
    Output("content-div", "style"),
    Input("csv-button", "n_clicks"),
    Input("db-button", "n_clicks"),
    Input("url-button", "n_clicks"),
)
def Refresh_content(csv_clicks, db_clicks, url_clicks):
    if not ctx.triggered:
        return SIDEBAR_STYLE, {"margin-left": "18rem", "padding": "2rem 1rem"}
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == "csv-button":
           table = dash_table.DataTable(data=df.to_dict('records'), page_size=6)
           graph = dcc.Graph(figure=px.histogram(df, x='continent', y='lifeExp', histfunc='avg'))
           return [table, graph], {"display": "none"}, {"display": "none"}
        elif button_id == "db-button":
            return {"display": "none"}, {"display": "none"}
        elif button_id == "url-button":
            return {"display": "none"}, {"display": "none"}
# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
