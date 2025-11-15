import dash
from dash import html, dcc, Input, Output, callback, State, ALL, MATCH, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import uuid
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Initial tab data
initial_sheets = [
    {"id": "sheet-1", "label": "sheet1"},
]

workshop = dbc.Container([
    dcc.Store(id="tabs-store", data=initial_sheets),
    
    # Store current active tab ID
    dcc.Store(id="active-tab-store", data=initial_sheets[0]["id"] if initial_sheets else "add-tab-button"),
    
    # Store chart settings for each sheet
    dcc.Store(id="chart-settings-store", data={}),
    
    html.H1("WorkSpace", className="mb-3"),
    
    # Tab container
    html.Div(id="tabs-container"),
    
    # Current active tab content display area
    dbc.Card([
        dbc.CardHeader("Tab Content"),
        dbc.CardBody(id="tab-content-area")
    ], className="mt-3")
], fluid=True, id="app-layout-container")

def create_sheet_tools(data, x_axis: str | None, y_axis: str | None, filter: dict | None, graph_type="histogram"):
    sheet_tools = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Graph Type"),
                            dbc.RadioItems(
                                id="graph-type-radio",
                                options=[
                                    {"label": "Histogram", "value": "histogram"},
                                    {"label": "Pie Chart", "value": "pie"},
                                    {"label": "Scatter Plot", "value": "scatter"},
                                    {"label": "Line Chart", "value": "line"},
                                ],
                                value=graph_type,
                                inline=False,
                            ),
                            html.Label("X-Axis"),
                            dbc.RadioItems(
                                id="x-axis-radio",
                                options={
                                    df_col: df_col for df_col in pd.DataFrame.from_dict(data).columns
                                },
                                value=x_axis,
                                inline=False,
                            ),
                            html.Label("Y-Axis"),
                            dbc.RadioItems(
                                id="y-axis-radio",
                                options={
                                    df_col: df_col for df_col in pd.DataFrame.from_dict(data).columns
                                },
                                value=y_axis,
                                inline=False,
                            ),
                            
                        ],
                        width=2,
                    ),
                    dbc.Col(
                        [
                            dbc.Form(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Label("Date Filter"),
                                            dcc.DatePickerRange(
                                                id='date-picker-range',
                                                start_date_placeholder_text='Start Date',
                                                end_date_placeholder_text='End Date',
                                                display_format='YYYY-MM-DD',
                                                minimum_nights=0,
                                                show_outside_days=True,
                                                start_date=filter.get('start_date') if filter else None,
                                                end_date=filter.get('end_date') if filter else None
                                            )
                                        ]
                                    )
                                ]
                            )
                        ],
                        width=2,
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(figure={}, id='controls-and-graph')
                        ],
                        width=8,
                    )
                ]
            )
        ]
    )
    return sheet_tools

@callback(
    Output("chart-settings-store", "data"),
    Input("x-axis-radio", "value"),
    Input("y-axis-radio", "value"),
    State("chart-settings-store", "data"),
    State("active-tab-store", "data"),
)
def update_axis_options(x_axis, y_axis, chart_settings, active_tab):
    if not chart_settings:
        chart_settings = {}
    
    try:
        # Update chart settings for the current active tab
        if active_tab not in chart_settings:
            chart_settings[active_tab] = {}
        
        chart_settings[active_tab]["x_axis"] = x_axis
        chart_settings[active_tab]["y_axis"] = y_axis
        
        print(f"Updated settings for tab {active_tab}: {chart_settings[active_tab]}")
        return chart_settings
        
    except Exception as e:
        print(f"Error updating axis options: {e}")
        return chart_settings
        
@callback(
    Output("chart-settings-store", "data", allow_duplicate=True),
    Output("controls-and-graph", "figure"),
    Input("graph-type-radio", "value"),
    Input("x-axis-radio", "value"),
    Input("y-axis-radio", "value"),
    Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
    State("uploaded-data-store", "data"),
    State("chart-settings-store", "data"),
    State("dynamic-tabs", "active_tab"),
    prevent_initial_call=True
)
def update_graph(graph_type, x_axis, y_axis, start_date, end_date, data, chart_settings, active_tab):
    if not data:
        return dash.no_update
    
    # Update chart settings for the current sheet
    updated_settings = chart_settings.copy()
    updated_settings[active_tab] = {
        "graph_type": graph_type,
        "x_axis": x_axis,
        "y_axis": y_axis,
        "filter": {"start_date": start_date, "end_date": end_date}
    }
    
    df = pd.DataFrame.from_dict(data)
    
    # Filter data if date filter is applied
    if start_date and end_date:
        # Assuming there is a column named 'date' in the data
        # If the actual date column name is different, it needs to be replaced
        if 'date' in df.columns:
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        else:
            print("Warning: 'date' column not found in data. Date filtering will not be applied.")
    
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
    
    return updated_settings, fig

@callback(
    Output("tabs-container", "children"),
    Input("tabs-store", "data"),
    Input("active-tab-store", "data")
)
def initialize_workshop(sheets_data, active_tab_id):
    
    # Create regular tabs
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


    # Handle tab content display
@callback(
    Output("tab-content-area", "children"),
    Input("dynamic-tabs", "active_tab"),
    State("tabs-store", "data"),
    State("uploaded-data-store", "data"),
    State("chart-settings-store", "data")
)
def update_tab_content(active_tab, sheets_data, uploaded_data, chart_settings):
    """Update content area based on the current active tab"""
    # If it's the Data Source tab, display data source content
    if active_tab == "data-source-tab":
        return create_data_source(uploaded_data)
    
    # Find the content of the current active tab
    for tab in sheets_data:
        if tab["id"] == active_tab:
            # If it's a sheet tab, display chart tools and graph
            # Read current sheet's chart settings from chart-settings-store
            current_tab_settings = chart_settings.get(active_tab, {})
            
            # Check if there is uploaded data
            if not uploaded_data:
                return html.Div("Please upload data first to use this tab.")
            
            df = pd.DataFrame.from_dict(uploaded_data)
            columns = df.columns.tolist()
            
            # Get current settings, or use defaults if not available
            x_axis = current_tab_settings.get("x_axis", columns[0] if columns else None)
            y_axis = current_tab_settings.get("y_axis", columns[1] if len(columns) > 1 else None)
            filter = current_tab_settings.get("filter")
            filter_value = current_tab_settings.get("filter_value")
            graph_type = current_tab_settings.get("graph_type", "histogram")
            
            # Ensure x_axis and y_axis are valid column names
            if x_axis not in columns:
                x_axis = columns[0] if columns else None
            if y_axis not in columns and len(columns) > 1:
                y_axis = columns[1]
            elif y_axis not in columns and len(columns) == 1:
                y_axis = None
            
            return create_sheet_tools(uploaded_data, x_axis, y_axis, filter, graph_type)
    

@callback(
    Output("data-source-tab", "children"),  # This callback is actually not needed as data is displayed in tab-content-area
    Input("dynamic-tabs", "active_tab"),
    State("uploaded-data-store", "data") 
)
def create_data_source(data):
    """Create data source table display component"""
    if not data:
        print("No data available for display.")
        return html.Div("No Uploaded Data")
    
    try:
        # Directly use the uploaded data, ensuring type correctness
        formatted_data = []
        for row in data:
            formatted_row = {}
            for key, value in row.items():
                # Ensure key is a string
                str_key = str(key)
                # Ensure value is a basic type
                if isinstance(value, (int, float, str, bool)):
                    formatted_row[str_key] = value
                else:
                    formatted_row[str_key] = str(value)
            formatted_data.append(formatted_row)
        
        # Get all column names
        columns = list(formatted_data[0].keys()) if formatted_data else []
        
        return html.Div([
            html.H4("Uploaded Data Preview"),
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
            html.H4("Data Error"),
            html.P(f"Failed to display data: {str(e)}")
        ])
    
# Handle adding new tabs
@callback(
    Output("tabs-store", "data"),
    Output("active-tab-store", "data"),
    Input("dynamic-tabs", "active_tab"),
    State("tabs-store", "data"),
    prevent_initial_call=True
)
def handle_add_tab(active_tab, sheets_data):
    # Only add a new tab when the + button is clicked
    if active_tab == "add-tab-button":
        # Calculate the number of existing sheet tabs
        sheet_count = 0
        for tab in sheets_data:
            if tab["label"].startswith("sheet"):
                sheet_count += 1
        
        # Generate new tab name
        new_sheet_name = f"sheet{sheet_count + 1}"
        
        # Generate new tab ID
        new_tab_id = f"tab-{str(uuid.uuid4())[:8]}"
        
        # Create new tab data
        new_tab = {
            "id": new_tab_id,
            "label": new_sheet_name,
        }
        
        # Insert the new tab before the + tab
        updated_tabs = sheets_data + [new_tab]
        
        # Activate the newly added tab
        return updated_tabs, new_tab_id
    
    return dash.no_update, dash.no_update

# Handle closing tabs
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
    
    # Get the ID of the tab whose close button was clicked
    triggered_id = ctx.triggered[0]["prop_id"]
    if "tab_id" in triggered_id:
        import json
        tab_id_to_close = json.loads(triggered_id.split(".")[0])["tab_id"]
        
        # Check if the tab to be closed is a fixed tab (Data Source or sheet1)
        if tab_id_to_close in ["tab-1", "tab-2"]:
            return dash.no_update, dash.no_update
        
        # Filter out the tab to be closed
        updated_tabs = [tab for tab in sheets_data if tab["id"] != tab_id_to_close]
        
        # If the closed tab was the active one, activate the first tab or the + tab
        new_active_tab = active_tab
        if active_tab == tab_id_to_close:
            if updated_tabs:
                new_active_tab = updated_tabs[0]["id"]
            else:
                new_active_tab = "add-tab-button"
        
        return updated_tabs, new_active_tab
    
    return dash.no_update, dash.no_update

# Example callback: Embed the entire app layout as a child of another container
@callback(
    Output("outer-container", "children"),
    Input("trigger-button", "n_clicks")
)
def embed_app_in_outer_container(n_clicks):
    if n_clicks:
        # Return the app layout container
        return app.layout
    else:
        # In initial state or when not clicked, show a prompt message
        return html.Div([
            dbc.Button("Load App", id="trigger-button", color="primary"),
            html.Div(id="app-container")
        ])

if __name__ == '__main__':
    app.run(debug=True)