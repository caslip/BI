@callback(
    Output("tab-content-area", "children"),
    Input("uploaded-data-store", "data"),
    Input("dynamic-tabs", "active_tab"),
    State("tabs-store", "data")
)
def update_tab_content(data, active_tab, tabs_data):
    