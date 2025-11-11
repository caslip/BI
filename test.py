import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H4("Label与输入框水平排列问题解决", className="mb-4"),
    
    html.H5("❌ 问题示例：宽度总和超过12"),
    dbc.Row([
        dbc.Label("Host:", width=3),
        dbc.Col(dcc.Input(type="text", placeholder="Localhost"), width=10)
    ], className="mb-3 p-2 border rounded bg-light"),
    
    html.H5("✅ 解决方案1：调整宽度使总和≤12"),
    dbc.Row([
        dbc.Label("Host:", width=2),  # 减小Label宽度
        dbc.Col(dcc.Input(type="text", placeholder="Localhost"), width=10)
    ], className="mb-3 p-2 border rounded bg-light"),
    
    html.H5("✅ 解决方案2：使用更合理的宽度分配"),
    dbc.Row([
        dbc.Label("Host:", width=3),
        dbc.Col(dcc.Input(type="text", placeholder="Localhost"), width=9)  # 3+9=12
    ], className="mb-3 p-2 border rounded bg-light"),
    
    html.H5("✅ 解决方案3：使用auto宽度"),
    dbc.Row([
        dbc.Label("Host:", width="auto"),  # 自动宽度
        dbc.Col(dcc.Input(type="text", placeholder="Localhost"), width=True)  # 剩余空间
    ], className="mb-3 p-2 border rounded bg-light"),
    
    html.H5("✅ 解决方案4：使用InputGroup（推荐）"),
    dbc.InputGroup([
        dbc.InputGroupText("Host:"),
        dbc.Input(type="text", placeholder="Localhost")
    ], className="mb-3"),
    
    html.H5("✅ 解决方案5：使用FormFloating"),
    dbc.FormFloating([
        dcc.Input(type="text", placeholder="Localhost", id="host-input"),
        html.Label("Host")
    ], className="mb-3"),
    
    html.H5("完整表单示例"),
    dbc.Form([
        dbc.Row([
            dbc.Label("Host:", width=3),
            dbc.Col(dcc.Input(type="text", placeholder="localhost"), width=9)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Label("Port:", width=3),
            dbc.Col(dcc.Input(type="number", placeholder="5432", value=5432), width=9)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Label("Database:", width=3),
            dbc.Col(dcc.Input(type="text", placeholder="mydb"), width=9)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Label("Username:", width=3),
            dbc.Col(dcc.Input(type="text", placeholder="user"), width=9)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Label("Password:", width=3),
            dbc.Col(dcc.Input(type="password", placeholder="password"), width=9)
        ], className="mb-3"),
    ])
], fluid=True)

if __name__ == '__main__':
    app.run(debug=True)