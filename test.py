import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 创建响应式工具栏
responsive_toolbar = html.Div([
    # 桌面版工具栏（大屏幕显示完整工具栏）
    dbc.Row([
        dbc.Col(
            dbc.ButtonGroup([
                dbc.Button("文件", id="btn-file", color="primary"),
                dbc.Button("编辑", id="btn-edit", color="primary"),
                dbc.Button("视图", id="btn-view", color="primary"),
                dbc.Button("工具", id="btn-tools", color="primary"),
                dbc.Button("帮助", id="btn-help", color="primary"),
            ], className="d-none d-md-flex"),  # 中等屏幕以上显示
            width="auto"
        ),
        
        # 移动版工具栏（小屏幕显示折叠菜单）
        dbc.Col(
            dbc.DropdownMenu(
                label="菜单",
                children=[
                    dbc.DropdownMenuItem("文件", id="mobile-file"),
                    dbc.DropdownMenuItem("编辑", id="mobile-edit"),
                    dbc.DropdownMenuItem("视图", id="mobile-view"),
                    dbc.DropdownMenuItem("工具", id="mobile-tools"),
                    dbc.DropdownMenuItem("帮助", id="mobile-help"),
                ],
                color="primary",
                className="d-md-none",  # 中等屏幕以下显示
            ),
            width="auto"
        ),
        
        # 搜索框（自适应宽度）
        dbc.Col(
            dbc.InputGroup([
                dbc.Input(placeholder="搜索...", id="responsive-search"),
                dbc.Button("搜索", id="btn-search", color="secondary"),
            ], size="sm"),
            width=True
        ),
        
    ], className="g-2 align-items-center")
], className="p-3 bg-light border rounded mb-3")

app.layout = dbc.Container([
    responsive_toolbar,
    html.Div(id="responsive-output", className="mt-3 p-3 border rounded")
], fluid=True)

# 回调函数
@app.callback(
    Output('responsive-output', 'children'),
    [Input('btn-file', 'n_clicks'),
     Input('btn-edit', 'n_clicks'),
     Input('btn-view', 'n_clicks'),
     Input('btn-tools', 'n_clicks'),
     Input('btn-help', 'n_clicks'),
     Input('mobile-file', 'n_clicks'),
     Input('mobile-edit', 'n_clicks'),
     Input('mobile-view', 'n_clicks'),
     Input('mobile-tools', 'n_clicks'),
     Input('mobile-help', 'n_clicks'),
     Input('btn-search', 'n_clicks'),
     Input('btn-login', 'n_clicks'),
     Input('btn-register', 'n_clicks'),
     Input('responsive-search', 'n_submit')]
)
def handle_responsive_toolbar(file, edit, view, tools, help, 
                             m_file, m_edit, m_view, m_tools, m_help,
                             search, login, register, search_enter):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "点击工具栏按钮进行操作"
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    actions = {
        'btn-file': '打开文件菜单',
        'btn-edit': '打开编辑菜单',
        'btn-view': '打开视图菜单',
        'btn-tools': '打开工具菜单',
        'btn-help': '打开帮助菜单',
        'mobile-file': '移动版 - 文件',
        'mobile-edit': '移动版 - 编辑',
        'mobile-view': '移动版 - 视图',
        'mobile-tools': '移动版 - 工具',
        'mobile-help': '移动版 - 帮助',
        'btn-search': '执行搜索',
        'btn-login': '用户登录',
        'btn-register': '用户注册',
        'responsive-search': '按回车搜索'
    }
    
    return f"执行操作: {actions.get(button_id, '未知操作')}"

if __name__ == '__main__':
    app.run_server(debug=True)