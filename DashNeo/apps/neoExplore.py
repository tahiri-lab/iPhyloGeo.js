from neo4j import GraphDatabase
import os
import pandas as pd
import dash
import dash_cytoscape as cyto
from dash import dcc, html
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
from dash import dash_table
from datetime import datetime
from dotenv import load_dotenv
from app import app

# --------------------------

lineage_list = ['A', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AP', 'AQ', 'AS', 'AT', 'AU', 'AV', 'AW', 'AY', 'AZ', 'B', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BY', 'BZ', 'C', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CJ', 'CK', 'CL', 'CM', 'CN', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CY', 'CZ', 'D', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'DG', 'DH', 'DJ', 'DK', 'DL', 'DM', 'DN', 'DP', 'DQ', 'DR', 'DS',
                'DT', 'DU', 'DV', 'DW', 'DY', 'DZ', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF', 'G', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'U', 'V', 'W', 'XA', 'XAA', 'XAB', 'XAC', 'XAD', 'XAE', 'XAF', 'XAG', 'XAH', 'XAJ', 'XAK', 'XAL', 'XAM', 'XAN', 'XAP', 'XAQ', 'XAR', 'XAS', 'XAT', 'XAU', 'XAV', 'XAW', 'XAY', 'XAZ', 'XB', 'XBA', 'XBB', 'XBC', 'XBD', 'XBE', 'XBF', 'XBG', 'XBH', 'XBJ', 'XBK', 'XBL', 'XBM', 'XBN', 'XBP', 'XC', 'XD', 'XE', 'XF', 'XG', 'XH', 'XJ', 'XK', 'XL', 'XM', 'XN', 'XP', 'XQ', 'XR', 'XS', 'XT', 'XU', 'XV', 'XW', 'XY', 'XZ', 'Y', 'Z']
# ------------------------------------------------------
# for lineage data search
['lineage', 'earliest_date', 'latest_date', 'iso_code',
 'most_common_country', 'rate']
data_lineage = {
    'lineage': [],
    'earliest_date': [],
    'latest_date': [],
    'iso_code': [],
    'most_common_country': [],
    'rate': [],
}
df_lineage = pd.DataFrame(data_lineage)
# -----------Neo4j query function------------------------------
load_dotenv("my.env")
password = os.getenv("NEO_PASS")
# print(password)


def queryToDataframe(query, col_name_lt):
    # Execute the Cypher query
    driver = GraphDatabase.driver("neo4j+ssc://2bb60b41.databases.neo4j.io:7687",
                                  auth=("neo4j", password))

    session = driver.session()
    results = session.run(query)
    # Transform the results to a DataFrame
    df = pd.DataFrame(results, columns=col_name_lt)
    return df


# -----------------------------------------
layout = html.Div([
    html.Div(html.H2("Phylogeography"), style={"text-align": "center"}),
    html.Hr(),
    # ----------
    dbc.Container([

        # ----Row 1 begin -------
        dbc.Row([
            dbc.Col([

                # ------
                dbc.CardHeader(
                    dbc.Button(
                        "Exploration: Start with the lineage",
                        color="primary",
                        id="button-ExploreLineage",
                    )
                ),
                dbc.Collapse([
                    html.H5(
                        "Selecte the group(s) of lineage to be studied:"),
                    dcc.Checklist(id='choice-lineage',
                                  options=[{'label': x, 'value': x}
                                           for x in lineage_list],
                                  labelStyle={'display': 'inline-block', 'marginRight': '20px'}),
                    dbc.Button("Confirm Lineage Selection",
                               id="button-confir-lineage", outline=True, color="success", className="me-1"),
                    # html.Button("Confirm Table Filter",
                    #             id="button-table", style={"display": "none"}),


                ],
                    id='exploreLineage', is_open=False,   # the Id of Collapse
                ),
                # ------------

            ], xs=12, sm=12, md=12, lg=12, xl=12),

        ], justify='around'),
        # ----Row 1 end ---
        html.Hr(),

        # ----Row 1-2: Dash Table (begin) -------
        dbc.Row([
            dbc.Col([
                dcc.Loading(
                    id='loading',
                    type='circle',
                    children=[
                        dash_table.DataTable(
                            id='lineage-table',
                            columns=[
                                {"name": i, "id": i, "deletable": False,
                                 "selectable": False, "hideable": False}
                                for i in df_lineage.columns
                            ],
                            # the contents of the table
                            data=df_lineage.to_dict('records'),
                            editable=False,              # allow editing of data inside all cells
                            # allow filtering of data by user ('native') or not ('none')
                            filter_action="native",
                            # enables data to be sorted per-column by user or not ('none')
                            sort_action="native",
                            sort_mode="multi",         # sort across 'multi' or 'single' columns
                            # column_selectable="multi",  # allow users to select 'multi' or 'single' columns
                            # row_selectable="single",     # allow users to select 'multi' or 'single' rows
                            # choose if user can delete a row (True) or not (False)
                            row_deletable=True,
                            # selected_columns=[],        # ids of columns that user selects
                            selected_rows=[],           # indices of rows that user selects
                            # all data is passed to the table up-front or not ('none')
                            page_action="native",
                            page_current=0,             # page number that user is on
                            page_size=20,                # number of rows visible per page
                            style_cell={                # ensure adequate header width when text is shorter than cell's text
                                'minWidth': 95, 'maxWidth': 95, 'width': 95
                            },
                            style_data={                # overflow cells' content into multiple lines
                                'whiteSpace': 'normal',
                                'height': 'auto'
                            },
                            style_header={
                                'whiteSpace': 'normal',
                                'height': 'auto'
                            }
                        ),
                        html.Br(),
                        dbc.Button("Confirm samples Selection",
                                   id="button-confir-filter", outline=True, color="success", className="me-1"),
                        html.Br(),
                        # Total rows count
                        html.Div(id='row-count'),
                    ]
                ),


            ], xs=12, sm=12, md=12, lg=12, xl=12),

        ], justify='around'),
        # ----Row 1-2 end ---
        html.Hr(),

        # ----Row 1-3: Cyto (begin) -------
        dbc.Row([
            dbc.Col([

                html.Div(id='cyto-container')

            ], xs=12, sm=12, md=12, lg=12, xl=12),

        ], justify='around'),

        # ------ Row 1-3 End ---------
        html.Br(),
        html.Hr(),
        html.Br(),
        # ----Row 2 begin -------
        dbc.Row([
            dbc.Col([



            ], xs=12, sm=12, md=12, lg=12, xl=12),

        ], justify='around'),


        # ----Row 2 end ---


    ]),
])

# ----------------------------


@app.callback(
    Output("exploreLineage", "is_open"),
    [Input("button-ExploreLineage", "n_clicks")],
    [State("exploreLineage", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('lineage-table', 'data'),
    [Input('button-confir-lineage', 'n_clicks'),
     State('choice-lineage', 'value'),
     ],
)
def update_table(n, checklist_value):

    if n is None:
        return None
    else:
        if checklist_value:
            # -----------------Query data in Neo4j database(input: parameters; output: pandas Data Frame)---------------------------------
            starts_with_conditions = " OR ".join(
                [f'n.lineage STARTS WITH "{char}"' for char in checklist_value])

            query = f"""
                MATCH (n:Lineage) - [r: IN_MOST_COMMON_COUNTRY] -> (l: Location)
                WHERE {starts_with_conditions}
                RETURN n.lineage as lineage, n.earliest_date as earliest_date, n.latest_date as latest_date, l.iso_code as iso_code, n.most_common_country as most_common_country,  r.rate as rate
                """
            cols = ['lineage', 'earliest_date', 'latest_date', 'iso_code',
                    'most_common_country', 'rate']
            df = queryToDataframe(query, cols)
            # Convert the 'Date' column to pandas datetime format
            df['earliest_date'] = pd.to_datetime(
                df['earliest_date'].apply(lambda x: x.to_native()))
            df['latest_date'] = pd.to_datetime(
                df['latest_date'].apply(lambda x: x.to_native()))

            # Format the 'Date' column as '%Y-%m-%d'
            df['earliest_date'] = df['earliest_date'].dt.strftime('%Y-%m-%d')
            df['latest_date'] = df['latest_date'].dt.strftime('%Y-%m-%d')

            # print(df)

            # print(q)
            # -----------------------Present the results in Dash Table --------------------------------------
            # Update DataTable
            table_data = df.to_dict('records')
            # global global_table
            # global_table = table
            return table_data
        # elif not start_date or not end_date:
        #     return html.Div("Please select a date range.")
        elif not checklist_value:
            return html.Div("Please select at least one option from the checklist.")

# ---------- Visual Cyto ----------------------


# @app.callback(Output('cyto-container', 'children'),
#               Input('button-confir-filter', 'n_clicks'),
#               State('table-container', "derived_virtual_data"),)
# def make_graphs(n, all_rows_data):
#     print(all_rows_data)
#     dff = pd.DataFrame(all_rows_data)
#     if n is None:
#         return dash.no_update
#     else:
#         return html.Div("Data Size: {}".format(dff.shape))

# ---------- Check Global variable + Cyto----------------------


@app.callback(
    Output('row-count', 'children'),
    Output('cyto-container', 'children'),
    [Input('button-confir-filter', 'n_clicks'),
     State(component_id='lineage-table',
           component_property="derived_virtual_data")]
)
def check_update(n, all_rows_data):
    dff = pd.DataFrame(all_rows_data)
    if n is None:
        return dash.no_update
    else:
        dff = pd.DataFrame(all_rows_data)

        print("shape", dff.shape)

        row_count = html.H5("Selected Data Size: {}".format(len(dff))),
        mycyto = html.Div()
        if dff.empty != True:
            nodes_list = dff.lineage.unique().tolist(
            ) + dff.most_common_country.unique().tolist()
            elements = [{'data': {'id': id, 'label': id}} for id in nodes_list]
            dff = dff[['lineage', 'most_common_country', 'rate']]
            dff.rename(columns={"most_common_country": "source",
                                "lineage": "target", "rate": "weight"}, inplace=True)
            data_list = dff.to_dict('records')
            relations = [{'data': item} for item in data_list]
            elements.extend(relations)

            mycyto = cyto.Cytoscape(
                id='cytoscape-styling-2',
                # circle "random","preset","circle","concentric","grid","breadthfirst","cose","close-bilkent","cola","euler","spread","dagre","klay"
                layout={'name': 'circle'},
                style={'width': '100%', 'height': '400px'},
                elements=elements,
                stylesheet=[
                    {
                        'selector': 'edge',
                        'style': {
                                    'label': 'data(weight)'
                        }
                    },
                    {
                        'selector': '[weight > 30]',
                        'style': {
                                    'line-color': 'blue'
                        }
                    }
                ]
            )
    return row_count, mycyto
    # ---------------------------------------------


# -----------------------------------------

# Make the button visible
#     style = {"display": "inline"} if table is not None else {
#         "display": "none"}
#     app.layout.children[2].style = style


# -------------Visualization: dash_cytoscape-----------------------
