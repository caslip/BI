from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import callback, Input, Output, State, dash_table, no_update
import pandas as pd
import base64
import io
import threading

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
                        dbc.Button("Done", id="close-modal", n_clicks=0)
                    )
                    ],
                    id="csv-modal",
                    is_open=False,
                ),
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


# 获取 csv 并显示
@callback(Output('uploaded-data-store', 'data', allow_duplicate=True),
          Output('upload-text', 'children'),
              Input('upload-in-modal', 'contents'),
              State('upload-in-modal', 'filename'),
              State('upload-in-modal', 'last_modified'),
              prevent_initial_call=True)
def update_output(contents, filename, date):
    with lock:
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
            return html.Div([
                'There was an error processing this file.'
            ])
        
        print(df.head())

        return df.to_dict('records'), f'File "{filename}" uploaded successfully!'

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

# 获取 URL 并显示
@callback(
    Output("uploaded-data-store", "data", allow_duplicate=True),
    Input("submit-url", "n_clicks"),
    State("url-input", "value"),
    prevent_initial_call=True
)
def check_url(n_clicks, url):
    with lock:
        try:
            if n_clicks:
                df = pd.read_csv(url)
                print(df.head())
                return df.to_dict('records')
        except Exception as e:
            print(e)
            return no_update