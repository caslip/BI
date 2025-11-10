from dash import callback, Input, Output, State, dash_table, no_update, dcc, html, Dash
import pandas as pd
import base64
import io
import dash_bootstrap_components as dbc
import plotly.express as px

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def create_sheet_tools():
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
                                options=[
                                    {"label": "列A", "value": "column_a"},
                                    {"label": "列B", "value": "column_b"},
                                    {"label": "列C", "value": "column_c"},
                                ],
                                value="column_a",
                                inline=False,
                            ),
                            html.Label("Y轴"),
                            dbc.RadioItems(
                                id="y-axis-radio",
                                options=[
                                    {"label": "列X", "value": "column_x"},
                                    {"label": "列Y", "value": "column_y"},
                                    {"label": "列Z", "value": "column_z"},
                                ],
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

app.layout = create_sheet_tools()

@callback(
    [Output('uploaded-data-store', 'data'),
     Output('column-names-store', 'data')],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def parse_contents(contents, filename):
    if contents is None:
        return None, None
    
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return None, None
    except Exception as e:
        print(e)
        return None, None
    
    return df.to_json(date_format='iso', orient='split'), df.columns.tolist()

@callback(
    [Output('x-axis-radio', 'options'),
     Output('x-axis-radio', 'value'),
     Output('y-axis-radio', 'options'),
     Output('y-axis-radio', 'value')],
    Input('column-names-store', 'data')
)
def update_axis_options(column_names):
    if column_names is None:
        return [], None, [], None
    
    options = [{'label': col, 'value': col} for col in column_names]
    return options, column_names[0], options, column_names[0]

@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='graph-type-radio', component_property='value'),
    Input(component_id='x-axis-radio', component_property='value'),
    Input(component_id='y-axis-radio', component_property='value'),
    State(component_id='uploaded-data-store', component_property='data')
)
def update_graph(graph_type, x_axis, y_axis, df_data):
    if df_data is None:
        return px.histogram()  # Return an empty histogram if no data is available
    
    # Convert df_data from JSON to DataFrame if necessary
    if isinstance(df_data, str):
        df_data = pd.read_json(df_data)
    
    if graph_type == 'histogram':
        fig = px.histogram(df_data, x=x_axis, y=y_axis, histfunc='avg')
    elif graph_type == 'pie':
        fig = px.pie(df_data, names=x_axis, values=y_axis)
    elif graph_type == 'scatter':
        fig = px.scatter(df_data, x=x_axis, y=y_axis)
    elif graph_type == 'line':
        fig = px.line(df_data, x=x_axis, y=y_axis)
    else:
        fig = px.histogram(df_data, x=x_axis, y=y_axis, histfunc='avg')
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)
