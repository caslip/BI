from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import callback, Input, Output, State, dash_table, no_update
import pandas as pd
import base64
import io
import threading
from sqlalchemy import create_engine

lock = threading.Lock()


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

sidebar = html.Div(
    [
        html.H2("EasyBI", className="display-4"),
        html.Hr(),
        html.P("Please import your data", className="lead"),
        dbc.ButtonGroup(
            [
                # Button of CSV to trigger modals
                dbc.Button( "Import from CSV",
                            id='csv-button',
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },),
                dbc.Modal(
                [
                    dbc.ModalHeader("Upload File"),
                    dbc.ModalBody(
                        dcc.Upload(
                            id='upload-in-modal',
                            children=html.Div(['Drag and Drop or Click to Upload File'], id='upload-text'),
                            style={
                                'width': '100%',
                                'height': '100px',
                                'lineHeight': '100px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                            },
                            multiple=False
                            )
                        ),
                    dbc.ModalFooter(
                        dbc.Button("Done", id="submit-csv", n_clicks=0)
                    )
                    ],
                    id="csv-modal",
                    is_open=False,
                ),
                
                # Button of Database to trigger modals
                dbc.Button( "Import from Database", 
                            id="db-button",
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },),
                dbc.Modal(
                [
                    dbc.ModalHeader("Please config the MySQL connection"),
                    dbc.ModalBody(
                        dbc.Form([
                            dbc.Row([
                                dbc.Label("Host:", width=3),
                                dbc.Col(dcc.Input(type="text", id="host-input", value="localhost"), width=9)
                            ], className="mb-3"),
                            
                            dbc.Row([
                                dbc.Label("Port:", width=3),
                                dbc.Col(dcc.Input(type="number", id="port-input", value="3306"), width=9)
                            ], className="mb-3"),

                            dbc.Row([
                                dbc.Label("Username:", width=3),
                                dbc.Col(dcc.Input(type="text", id="username-input", value="root"), width=9)
                            ], className="mb-3"),

                            dbc.Row([
                                dbc.Label("Password:", width=3),
                                dbc.Col(dcc.Input(type="password", id="password-input"), width=9)
                            ], className="mb-3"),

                            dbc.Row([
                                dbc.Label("DataBase Name:", width=3),
                                dbc.Col(dcc.Input(type="text", id="db-name-input"), width=9)
                            ], className="mb-3", style={"align-items": "center"}),

                            dbc.Row([
                                dbc.Label("Search Table:", width=3),
                                dbc.Col(dcc.Input(type="text", id="search-input"), width=9)
                            ], className="mb-3", style={"align-items": "center"}),


                        ]),
                    ),
                    dbc.ModalFooter(
                        dbc.Button("Submit", id="submit-db", className="ms-auto", n_clicks=0)
                    ),
                ],
                id="db-modal",
                is_open=False,
                ),
                dbc.Button( "Import from URL", 
                            id="url-button",
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },),
                dbc.Modal(
                [
                    dbc.ModalHeader("Please input URL"),
                    dbc.ModalBody(
                        dbc.Input(id="url-input", placeholder="Input URL...", type="url",
                                  style={
                                        'width': '100%',
                                        'height': '100px',
                                        'lineHeight': '100px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                    },)
                    ),
                    dbc.ModalFooter(
                        dbc.Button("Submit", id="submit-url", className="ms-auto", n_clicks=0)
                    ),
                ],
                id="url-modal",
                is_open=False,
                ),
            ],
            vertical=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

@callback(
    Output("csv-modal", "is_open"),
    Input("csv-button", "n_clicks"),
    Input("close-modal", "n_clicks"),
    State("csv-modal", "is_open")
)
def toggle_csv_modal(open_clicks, close_clicks, is_open):
    if open_clicks or close_clicks:
        return not is_open
    return is_open
# Get csv file content
@callback(Output('uploaded-data-store', 'data', allow_duplicate=True),
          Output('upload-text', 'children'),
              Input('upload-in-modal', 'contents'),
              State('upload-in-modal', 'filename'),
              State('upload-in-modal', 'last_modified'),
              prevent_initial_call=True)
def update_csv_output(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return no_update, html.Div([
            'There was an error processing this file.'
        ])

    return df.to_dict('records'), f'File "{filename}" uploaded successfully!'

@callback(
    Output("db-modal", "is_open"),
    Input("db-button", "n_clicks"),
    Input("submit-db", "n_clicks"),
    State("db-modal", "is_open"),
)
def toggle_database_modal(open_clicks, submit_clicks, is_open):
    if open_clicks or submit_clicks:
        return not is_open
    return is_open

# Get data from database
@callback(
    Output("uploaded-data-store", "data", allow_duplicate=True),
    Input("submit-db", "n_clicks"),
    State("host-input", "value"),
    State("port-input", "value"),
    State("username-input", "value"),
    State("password-input", "value"),
    State("db-name-input", "value"),
    State("search-input", "value"),
    prevent_initial_call=True
)
def update_database_output(n_clicks, host, port, username, password, db_name, table):
    with lock:
        try:
            if n_clicks:
                connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}'
                engine = create_engine(connection_string)
                df = pd.read_sql(f"SELECT * FROM {table};", con=engine)
                return df.to_dict('records')
        except Exception as e:
            print(e)
            return no_update

@callback(
    Output("url-modal", "is_open"),
    Input("url-button", "n_clicks"),
    Input("submit-url", "n_clicks"),
    State("url-modal", "is_open"),
)
def toggle_url_modal(open_clicks, submit_clicks, is_open):
    if open_clicks or submit_clicks:
        return not is_open
    return is_open

# Get url file content
@callback(
    Output("uploaded-data-store", "data", allow_duplicate=True),
    Input("submit-url", "n_clicks"),
    State("url-input", "value"),
    prevent_initial_call=True
)
def update_url_output(n_clicks, url):
    with lock:
        try:
            if n_clicks:
                df = pd.read_csv(url)
                print(df.columns)
                return df.to_dict('records')
        except Exception as e:
            print(e)
            return no_update