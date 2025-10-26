"""
Service for web visualisation of gathered data
Ideas for further improvments are present in README file
"""

import pandas as pd
from dash import Dash, Input, Output, callback, dash_table, dcc, html

from core.db import engine
from core.settings import settings

df = pd.read_sql(settings.COUNTRIES_SOURCE_NAME, engine)

app = Dash()

main_columns = settings.DEFAULT_COLUMNS
all_columns = df.columns.tolist()
column_options = [{"label": col, "value": col} for col in all_columns]

# HTML and CSS is not my strongiest experties, so next part have been generated and corrected after inspection
app.layout = html.Div(
    [
        html.H1(children="AI digital test task", style={"textAlign": "center"}),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label("Select additional columns to display:"),
                                dcc.Dropdown(
                                    id="column-selector",
                                    options=column_options,
                                    value=[],
                                    multi=True,
                                    placeholder="Select additional columns...",
                                ),
                            ],
                            style={"margin-bottom": "10px", "width": "100%"},
                        ),
                        dash_table.DataTable(
                            id="data-table",
                            data=df.to_dict("records"),
                            columns=[{"name": col.replace("_", " ").title(), "id": col} for col in main_columns],
                            fixed_rows={'headers': True},
                            style_cell={"textAlign": "left", "padding": "10px"},
                            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
                            style_data={"whiteSpace": "normal", "height": "auto"},
                            style_table={"height": "calc(100vh - 200px)", "overflowY": "auto"},
                            sort_action="native",
                            page_action="none",
                            row_selectable="single",
                            selected_rows=[],
                            style_data_conditional=[
                                {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
                            ],
                            style_cell_conditional=[
                                {"if": {"column_id": "name_official"}, "textAlign": "left", "fontWeight": "bold"}
                            ],
                        ),
                    ],
                    style={
                        "width": "70%",
                        "display": "inline-block",
                        "vertical-align": "top",
                        "padding": "10px",
                        "border": "1px solid #ccc",
                        "border-radius": "5px",
                        "margin": "10px",
                        "float": "left",
                    },
                ),
                html.Div(
                    [html.H3("Selected Country Flags"), html.Div(id="selected-info")],
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "vertical-align": "top",
                        "padding": "10px",
                        "border": "1px solid #ccc",
                        "border-radius": "5px",
                        "margin": "10px",
                        "float": "right",
                    },
                ),
            ],
            style={"display": "flex", "flex-direction": "row"},
        ),
    ]
)


@callback([Output("data-table", "columns"), Output("data-table", "data")], Input("column-selector", "value"))
def update_table_columns(selected_columns):
    columns = [{"name": col.replace("_", " ").title(), "id": col} for col in main_columns]

    for col in selected_columns:
        if col not in main_columns:
            columns.append({"name": col.replace("_", " ").title(), "id": col})

    data = df.to_dict("records")

    return columns, data


@callback(Output("selected-info", "children"), Input("data-table", "selected_rows"))
def update_selected_info(selected_rows):
    if not selected_rows:
        return html.P("No row selected")

    selected_row = df.iloc[selected_rows[0]]
    country_name = selected_row["name_common"]
    flag_url = selected_row["flags_png"]

    return html.Div(
        [
            html.H4(f"Flag of {country_name}"),
            html.Img(
                src=flag_url,
                style={"width": "200px", "height": "150px", "border": "1px solid #ccc", "object-fit": "contain"},
                alt=f"Flag of {country_name}",
            ),
        ]
    )


if __name__ == "__main__":
    app.run(debug=settings.DEBUG_MODE)
