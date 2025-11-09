from dash import html
import dash_bootstrap_components as dbc

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

workshop = html.Div(
    [
        dbc.Tabs(
            id="workshop-tabs",
            active_tab="tab-1",
            children=[
                dbc.Tab(label="Data Source", tab_id="tab-1", label_style={"color": "#00AEF9"}),
                dbc.Tab(label="Sheet1", tab_id="tab-2", label_style={"color": "#00AEF9"}),
                dbc.Tab(label="+", tab_id="add-sheet-button", label_style={"color": "#00AEF9"}),
            ]
        ),
    ],
    id = "workshop-div"
)

sidebar = html.Div(
    [
        html.H2("EasyBI", className="display-4"),
        html.Hr(),
        html.P("Please import your data", className="lead"),
        dbc.ButtonGroup(
            [
                dbc.Button("Import from CSV", id="csv-button"),
                dbc.Button("Import from Database", id="db-button"),
                dbc.Button("Import from URL", id="url-button"),
            ],
            vertical=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
