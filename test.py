import dash
from dash import html, dcc, Input, Output, callback, State, ALL, MATCH
import dash_bootstrap_components as dbc
import uuid

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 初始标签数据
initial_tabs = [
    {"id": "tab-1", "label": "数据源", "content": "这是数据源标签的内容"},
    {"id": "tab-2", "label": "sheet1", "content": "这是sheet1标签的内容"},
]

app.layout = dbc.Container([
    # 存储标签状态
    dcc.Store(id="tabs-store", data=initial_tabs),
    
    # 存储当前活动标签ID
    dcc.Store(id="active-tab-store", data=initial_tabs[0]["id"] if initial_tabs else "add-tab-button"),
    
    html.H1("动态 Tab 管理", className="mb-4"),
    
    # Tab 容器
    html.Div(id="tabs-container"),
    
    # 当前活动标签内容显示区域
    dbc.Card([
        dbc.CardHeader("标签内容"),
        dbc.CardBody(id="tab-content-area")
    ], className="mt-3")
], fluid=True, id="app-layout-container")

def create_tabs_component(tabs_data, active_tab_id):
    """创建包含动态标签和 + 按钮的 Tabs 组件"""
    
    # 创建常规标签
    tab_components = []
    for tab in tabs_data:
        # 为前两个标签（数据源和sheet1）不显示关闭按钮
        show_close_button = tab["id"] not in ["tab-1", "tab-2"]
        tab_components.append(
            dbc.Tab(
                label=tab["label"],
                tab_id=tab["id"],
                labelClassName="d-flex align-items-center",
                className="position-relative"
            )
        )
    
    # 添加 + 标签（始终在最后）
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
        active_tab=active_tab_id
    )

def create_tab_content(tab_id, tabs_data):
    """根据标签 ID 创建对应的内容"""
    for tab in tabs_data:
        if tab["id"] == tab_id:
            return html.Div([
                html.H4(tab["label"]),
                html.P(tab["content"]),
                # 只为非固定标签显示编辑按钮
                dbc.Button("编辑内容", color="primary", size="sm") if tab["id"] not in ["tab-1", "tab-2"] else None
            ])
    
    # 如果是 + 标签，显示添加说明
    if tab_id == "add-tab-button":
        return html.Div([
            html.H4("添加新标签"),
            html.P("点击上方的 '+' 标签来添加新的标签页")
        ])
    
    return html.Div("标签内容未找到")

# 渲染标签容器
@callback(
    Output("tabs-container", "children"),
    Input("tabs-store", "data"),
    Input("active-tab-store", "data")
)
def update_tabs_container(tabs_data, active_tab_id):
    return create_tabs_component(tabs_data, active_tab_id)

# 处理标签内容显示
@callback(
    Output("tab-content-area", "children"),
    Input("dynamic-tabs", "active_tab"),
    State("tabs-store", "data")
)
def update_tab_content(active_tab, tabs_data):
    return create_tab_content(active_tab, tabs_data)

# 处理添加新标签
@callback(
    Output("tabs-store", "data", allow_duplicate=True),
    Output("active-tab-store", "data", allow_duplicate=True),
    Input("dynamic-tabs", "active_tab"),
    State("tabs-store", "data"),
    prevent_initial_call=True
)
def handle_add_tab(active_tab, tabs_data):
    # 只有当点击的是 + 标签时才添加新标签
    if active_tab == "add-tab-button":
        # 计算当前已有的 sheet 标签的数量
        sheet_count = 0
        for tab in tabs_data:
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
        updated_tabs = tabs_data + [new_tab]
        
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
def handle_close_tab(close_clicks, tabs_data, active_tab):
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
        updated_tabs = [tab for tab in tabs_data if tab["id"] != tab_id_to_close]
        
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
