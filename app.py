# Import packages
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input, ctx
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
from components import sidebar, SIDEBAR_STYLE ,workshop




# 创建示例数据
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# 初始化应用
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# 应用布局
app.layout = dbc.Container([
    html.Div([sidebar], id="sidebar-div"),
    html.Div([
        # html.H3(children="初始标题"),
        # html.P("请使用左侧边栏导入数据以开始分析。"),
        workshop
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
            return html.Div(workshop, style={"margin-top": "8rem", "padding": "2rem 1rem"}), {"display": "none"}, {"display": "none"}
        elif button_id == "db-button":
            return {"display": "none"}, {"display": "none"}
        elif button_id == "url-button":
            return {"display": "none"}, {"display": "none"}
        
@callback(
    Output("workshop-tabs", "children"),
    Input("workshop-tabs", "active_tab"),
)
def add_new_sheet(active_tab):
    
    # 如果点击了"+"按钮，添加新工作表
    if active_tab == "add-sheet-button":
        # 计算新工作表的ID和标签
        new_tab_id = f"tab-{len(current_tabs)}"
        new_tab_label = f"Sheet{len(current_tabs)-1}"
        
        # 创建新工作表内容
        new_tab_content = html.Div([
            html.H4(f"Content for {new_tab_label}"),
            html.P("This is a new sheet. Add your content here."),
            # 这里可以添加更多内容，比如数据表格、图表等
        ])
        
        # 创建新工作表
        new_tab = dbc.Tab(
            label=new_tab_label, 
            tab_id=new_tab_id, 
            label_style={"color": "#00AEF9"},
            children=new_tab_content
        )
        
        # 在"+"按钮前插入新工作表
        current_tabs.insert(-1, new_tab)
    
    return current_tabs


# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
