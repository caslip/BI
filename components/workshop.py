import dash
from dash import html, dcc, Input, Output, callback, State, ALL, MATCH, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import uuid
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 初始标签数据
initial_sheets = [
    {"id": "sheet-1", "label": "sheet1", "x": "column_x", "y": "column_y", "graph_type": "histogram"},
]

workshop = dbc.Container([
    dcc.Store(id="tabs-store", data=initial_sheets),
    
    # 存储当前活动标签ID
    dcc.Store(id="active-tab-store", data=initial_sheets[0]["id"] if initial_sheets else "add-tab-button"),
    
    html.H1("WorkSpace", className="mb-3"),
    
    # Tab 容器
    html.Div(id="tabs-container"),
    
    # 当前活动标签内容显示区域
    dbc.Card([
        dbc.CardHeader("标签内容"),
        dbc.CardBody(id="tab-content-area")
    ], className="mt-3")
], fluid=True, id="app-layout-container")

def create_sheet_tools(data):
    sheet_tools = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("图类型"),
                            dbc.RadioItems(
                                id="graph-type-radio",
                                options=[
                                    {"label": "直方图", "value": "histogram"},
                                    {"label": "饼图", "value": "pie"},
                                    {"label": "散点图", "value": "scatter"},
                                    {"label": "折线图", "value": "line"},
                                ],
                                value="histogram",
                                inline=False,
                            ),
                            html.Label("X轴"),
                            dbc.RadioItems(
                                id="x-axis-radio",
                                options={},
                                value="column_a",
                                inline=False,
                            ),
                            html.Label("Y轴"),
                            dbc.RadioItems(
                                id="y-axis-radio",
                                options={},
                                value="column_x",
                                inline=False,
                            ),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(figure={}, id='controls-and-graph')
                        ],
                        width=9,
                    )
                ]
            )
        ]
    )
    return sheet_tools

@callback(
    Output("x-axis-radio", "options"),
    Output("y-axis-radio", "options"),
    Input("uploaded-data-store", "data")
)
def update_axis_options(data):
    if not data:
        return [], []
    
    df = pd.DataFrame.from_dict(data)
    columns = df.head()
    
    options = [{"label": col, "value": col} for col in columns]
    
    return options, options

@callback(
    Output("tabs-store", "data"),
    Output("controls-and-graph", "figure"),
    Input("graph-type-radio", "value"),
    Input("x-axis-radio", "value"),
    Input("y-axis-radio", "value"),
    State("uploaded-data-store", "data"),
)
def update_graph(graph_type, x_axis, y_axis, data):
    if not data:
        return dash.no_update
    
    df = pd.DataFrame.from_dict(data)
    
    if x_axis not in df.columns or (graph_type != "pie" and y_axis not in df.columns):
        return dash.no_update
    
    if graph_type == "histogram":
        fig = px.histogram(df, x=x_axis, y=y_axis, histfunc='avg')
    elif graph_type == "pie":
        fig = px.pie(df, names=x_axis, values=y_axis)
    elif graph_type == "scatter":
        fig = px.scatter(df, x=x_axis, y=y_axis)
    elif graph_type == "line":
        fig = px.line(df, x=x_axis, y=y_axis)
    else:
        fig = {}
    
    return fig

@callback(
    Output("tabs-container", "children"),
    Input("tabs-store", "data"),
    Input("active-tab-store", "data")
)
def initialize_workshop(sheets_data, active_tab_id):
    
    # 创建常规标签
    tab_components = []
    tab_components.append(
        dbc.Tab(
            label="Data Source",
            tab_id="data-source-tab",
            labelClassName="d-flex align-items-center",
            className="position-relative"
        )
    )

    for tab in sheets_data:
        tab_components.append(
            dbc.Tab(
                label=tab["label"],
                tab_id=tab["id"],
                labelClassName="d-flex align-items-center",
                className="position-relative"
            )
        )
    
    tab_components.append(
        dbc.Tab(
            label="+",
            tab_id="add-tab-button",
            label_style={"fontSize": "18px", "fontWeight": "bold"}
        )
    )
    
    return dbc.Tabs(
        id="dynamic-tabs",
        children=tab_components,
        active_tab="data-source-tab"
    )


# 处理标签内容显示
@callback(
    Output("tab-content-area", "children"),
    Input("dynamic-tabs", "active_tab"),
    State("tabs-store", "data"),
    State("uploaded-data-store", "data")
)
def update_tab_content(active_tab, sheets_data, uploaded_data):
    """根据当前活动标签更新内容区域"""
    # 如果是 Data Source 标签，显示数据源内容
    if active_tab == "data-source-tab":
        return create_data_source(uploaded_data)
    
    # 查找当前活动标签的内容
    for tab in sheets_data:
        if tab["id"] == active_tab:
            # 如果是sheet标签，显示图表工具和图表
            return create_sheet_tools(uploaded_data)
    

@callback(
    Output("data-source-tab", "children"),  # 这个回调实际上不需要，因为数据显示在tab-content-area中
    Input("dynamic-tabs", "active_tab"),
    State("uploaded-data-store", "data") 
)
def create_data_source(data):
    """创建数据源表格显示组件"""
    if not data:
        print("No data available for display.")
        return html.Div("没有上传的数据。")
    
    try:
        # 直接使用上传的数据，确保类型正确
        formatted_data = []
        for row in data:
            formatted_row = {}
            for key, value in row.items():
                # 确保键是字符串
                str_key = str(key)
                # 确保值是基本类型
                if isinstance(value, (int, float, str, bool)):
                    formatted_row[str_key] = value
                else:
                    formatted_row[str_key] = str(value)
            formatted_data.append(formatted_row)
        
        # 获取所有列名
        columns = list(formatted_data[0].keys()) if formatted_data else []
        
        return html.Div([
            html.H4("上传的数据"),
            dash_table.DataTable(
                data=formatted_data,
                columns=[{'name': col, 'id': col} for col in columns],
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '5px'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
            )
        ])
    except Exception as e:
        return html.Div([
            html.H4("数据错误"),
            html.P(f"无法显示数据: {str(e)}")
        ])
    
# 处理添加新标签
@callback(
    Output("tabs-store", "data"),
    Output("active-tab-store", "data"),
    Input("dynamic-tabs", "active_tab"),
    State("tabs-store", "data"),
    prevent_initial_call=True
)
def handle_add_tab(active_tab, sheets_data):
    # 只有当点击的是 + 标签时才添加新标签
    if active_tab == "add-tab-button":
        # 计算当前已有的 sheet 标签的数量
        sheet_count = 0
        for tab in sheets_data:
            if tab["label"].startswith("sheet"):
                sheet_count += 1
        
        # 生成新的标签名称
        new_sheet_name = f"sheet{sheet_count + 1}"
        
        # 生成新的标签 ID
        new_tab_id = f"tab-{str(uuid.uuid4())[:8]}"
        
        # 创建新标签数据
        new_tab = {
            "id": new_tab_id,
            "label": new_sheet_name,
            "content": f"这是{new_sheet_name}标签的内容"
        }
        
        # 将新标签插入到 + 标签之前
        updated_tabs = sheets_data + [new_tab]
        
        # 激活新添加的标签
        return updated_tabs, new_tab_id
    
    return dash.no_update, dash.no_update

# 处理关闭标签
@callback(
    Output("tabs-store", "data", allow_duplicate=True),
    Output("active-tab-store", "data", allow_duplicate=True),
    Input({"type": "close-tab", "tab_id": ALL}, "n_clicks"),
    State("tabs-store", "data"),
    State("dynamic-tabs", "active_tab"),
    prevent_initial_call=True
)
def handle_close_tab(close_clicks, sheets_data, active_tab):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update, dash.no_update
    
    # 获取被点击的关闭按钮对应的标签 ID
    triggered_id = ctx.triggered[0]["prop_id"]
    if "tab_id" in triggered_id:
        import json
        tab_id_to_close = json.loads(triggered_id.split(".")[0])["tab_id"]
        
        # 检查要关闭的标签是否是固定标签（数据源或sheet1）
        if tab_id_to_close in ["tab-1", "tab-2"]:
            return dash.no_update, dash.no_update
        
        # 过滤掉要关闭的标签
        updated_tabs = [tab for tab in sheets_data if tab["id"] != tab_id_to_close]
        
        # 如果关闭的是当前活动标签，则激活第一个标签或+标签
        new_active_tab = active_tab
        if active_tab == tab_id_to_close:
            if updated_tabs:
                new_active_tab = updated_tabs[0]["id"]
            else:
                new_active_tab = "add-tab-button"
        
        return updated_tabs, new_active_tab
    
    return dash.no_update, dash.no_update

# 示例回调：将整个应用布局作为另一个容器的子元素
@callback(
    Output("outer-container", "children"),
    Input("trigger-button", "n_clicks")
)
def embed_app_in_outer_container(n_clicks):
    if n_clicks:
        # 返回应用布局的容器
        return app.layout
    else:
        # 初始状态或未点击时显示提示信息
        return html.Div([
            dbc.Button("加载应用", id="trigger-button", color="primary"),
            html.Div(id="app-container")
        ])

if __name__ == '__main__':
    app.run(debug=True)
