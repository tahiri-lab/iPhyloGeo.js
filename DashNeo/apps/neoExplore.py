from neo4j import GraphDatabase
import os
import pandas as pd
import dash
import dash_cytoscape as cyto
from dash import dcc, html, ctx
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
from dash import dash_table
from datetime import datetime
from dotenv import load_dotenv
from app import app
import secrets
import string
import yaml

# ------------------------
# For Neo4j Connection
load_dotenv("my.env")
password = os.getenv("NEO_PASS")
# print(password)
# --------------------------
# get location list


def get_databaseProperties_list():
    q_lineage = "MATCH (n:Lineage) RETURN DISTINCT n.lineage"
    q_protein = "MATCH (n:Protein) RETURN DISTINCT n.protein"
    q_location = "MATCH (n:Location) RETURN DISTINCT n.location"
    driver = GraphDatabase.driver("neo4j+ssc://2bb60b41.databases.neo4j.io:7687",
                                  auth=("neo4j", password))
    with driver.session() as session:
        results_location = session.run(q_location)
        location_list = [record['n.location'] for record in results_location]
        results_protein = session.run(q_protein)
        protein_list = [record['n.protein'] for record in results_protein]
        results_lineage = session.run(q_lineage)
        record_lineage_lt = [record['n.lineage'].split(
            '.')[0] for record in results_lineage]
        lineage_list = list(set(record_lineage_lt))

    location_lt = [item for item in location_list if item is not None]
    protein_lt = [item for item in protein_list if item is not None]
    lineage_lt = [item for item in lineage_list if item is not None]
    return location_lt, protein_lt, lineage_lt


location_list, protein_list, lineage_list = get_databaseProperties_list()
print(location_list)
print(protein_list)
print(lineage_list)
# ------------------------------------------------------
# for lineage data search: creat a empty table at the begining (place holder)
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


def queryToDataframe(query, col_name_lt):
    # Execute the Cypher query
    driver = GraphDatabase.driver("neo4j+ssc://2bb60b41.databases.neo4j.io:7687",
                                  auth=("neo4j", password))
    with driver.session() as session:
        # session = driver.session()
        results = session.run(query)
    # Transform the results to a DataFrame
        df = pd.DataFrame(results, columns=col_name_lt)
    return df


def getNucleoIdFromLineageFilter(df):
    accession_lt = []
    driver = GraphDatabase.driver("neo4j+ssc://2bb60b41.databases.neo4j.io:7687",
                                  auth=("neo4j", password))
    rows_as_dicts = df.to_dict(orient='records')
    for row in rows_as_dicts:
        lineage = row['lineage']
        theDate = row['earliest_date']
        location = row['most_common_country']
        query = """
            MATCH (n:Nucleotide)-[:COLLECTED_IN]->(l:Location)<-[:IN_MOST_COMMON_COUNTRY]-(m:Lineage)
            WHERE l.location = $location AND m.lineage = $lineage AND n.collection_date >= datetime($theDate)
            RETURN n.accession
            ORDER BY n.collection_date
            LIMIT 1
        """
        params = {"location": location, "lineage": lineage, "theDate": theDate}
        with driver.session() as session:
            # session = driver.session()
            results = session.run(query, params)
            record = results.single()
            # print(record)
            if record:
                accession = record["n.accession"]
                accession_lt.append(accession)
    return accession_lt


def getProteinIdFromLineageFilter(df, protein_name):
    accession_lt = []
    driver = GraphDatabase.driver("neo4j+ssc://2bb60b41.databases.neo4j.io:7687",
                                  auth=("neo4j", password))
    rows_as_dicts = df.to_dict(orient='records')
    for row in rows_as_dicts:
        lineage = row['lineage']
        theDate = row['earliest_date']
        location = row['most_common_country']
        query = """
            MATCH (n:Protein)-[:COLLECTED_IN]->(l:Location)<-[:IN_MOST_COMMON_COUNTRY]-(m:Lineage)
            WHERE l.location = $location AND m.lineage = $lineage AND n.protein = $protein_name AND n.collection_date >= datetime($theDate)
            RETURN n.accession
            ORDER BY n.collection_date
            LIMIT 1
        """
        params = {"location": location, "lineage": lineage,
                  "protein_name": protein_name, "theDate": theDate}
        with driver.session() as session:
            # session = driver.session()
            results = session.run(query, params)
            record = results.single()
            # print(record)
            if record:
                accession = record["n.accession"]
                accession_lt.append(accession)
    return accession_lt


# ---------Create Input Node and relations based on users setting------------------------------------------
# Function to generate a unique random name


def generate_short_id(length=8):
    characters = string.ascii_letters + string.digits
    short_id = ''.join(secrets.choice(characters) for _ in range(length))
    return short_id


def generate_unique_name():
    driver = GraphDatabase.driver("neo4j+ssc://2bb60b41.databases.neo4j.io:7687",
                                  auth=("neo4j", password))
    with driver.session() as session:
        random_name = generate_short_id()

        result = session.run(
            "MATCH (u:User {name: $name}) RETURN COUNT(u)", name=random_name)
        count = result.single()[0]

        while count > 0:
            random_name = generate_short_id()
            result = session.run(
                "MATCH (u:User {name: $name}) RETURN COUNT(u)", name=random_name)
            count = result.single()[0]

        return random_name


def addInputNeo(nodesLabel, inputNode_name, id_list):
    # Execute the Cypher query
    driver = GraphDatabase.driver("neo4j+ssc://2bb60b41.databases.neo4j.io:7687",
                                  auth=("neo4j", password))

    # Create a new node for the user
    with driver.session() as session:
        session.run(
            "CREATE (userInput:Input {name: $name})", name=inputNode_name)

    # Perform MATCH query to retrieve nodes
    with driver.session() as session:
        result = session.run(
            "MATCH (n:" + nodesLabel + ") WHERE n.accession IN $id_lt RETURN n",
            nodesLabel=nodesLabel,
            id_lt=id_list)

        # Create relationship with properties for each matched node
        with driver.session() as session:
            for record in result:
                other_node = record["n"]
                session.run("MATCH (u:Input {name: $name}), (n:" + nodesLabel + " {accession: $id}) "
                            "CREATE (n)-[r:IN_INPUT]->(u)",
                            name=inputNode_name, nodesLabel=nodesLabel, id=other_node["accession"])
    print("An Input Node is Added in Neo4j Database!")

# ----------------------------------------------------


def update_inputYaml(feature_name, value):
    # Load the YAML file
    with open('config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    # Update the values
    config['input'][feature_name] = value

    # Write the updated dictionary back to the YAML file
    with open('config/config.yaml', 'w') as file:
        yaml.dump(config, file)


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
                        "Select the group(s) of lineage to be studied:"),
                    dcc.Checklist(id='choice-lineage',
                                  options=[{'label': x, 'value': x}
                                           for x in lineage_list],
                                  labelStyle={'display': 'inline-block', 'marginRight': '20px'}),
                    # First dropdown for selecting DNA or Protein
                    html.H5(
                        "Selecte the type sequences data to be studied:"),
                    dcc.Dropdown(
                        id='type-dropdown',
                        options=[
                            {'label': 'Nucleotide', 'value': 'dna'},
                            {'label': 'Protein', 'value': 'protein'}
                        ],
                        value=None
                    ),
                    # Placeholder for the protein name radio items (initially hidden)
                    html.Div(id='protein-name-container', style={'display': 'none'}, children=[
                        dcc.RadioItems(
                            id='protein-name-radio',
                            options=[
                                {'label': i, 'value': i}
                                for i in protein_list
                            ],
                            value=None
                        )
                    ]),

                    dbc.Button("Confirm",
                               id="button-confir-lineage", outline=True, color="success", className="me-1"),
                    # Output for displaying the selected values
                    html.Div(id='output-container',
                             style={'margin-top': '20px'}),
                    # Valid message
                    html.Div(id='valid-message'),

                    # ------------------------------------
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

                    # -----------------------------------------------------------------------------------------------------
                ],
                    id='exploreLineage', is_open=False,   # the Id of Collapse
                ),
                # ------------

            ], xs=12, sm=12, md=12, lg=12, xl=12),

        ], justify='around'),
        # ----Row 1: Collapse -- end ---
        html.Br(),
        html.Hr(),
        html.Br(),
        # ----Row 2 begin -------
        dbc.Row([
            dbc.Col([
                dbc.CardHeader(
                    dbc.Button(
                        "Exploration: Start with the location",
                        color="primary",
                        id="button-ExploreLocation",
                    )
                ),
                dbc.Collapse([
                    html.H5("Date Range Selection"),
                    dcc.DatePickerRange(
                        id='date-range-lineage',
                        start_date_placeholder_text="Start Date",
                        end_date_placeholder_text="End Date",
                        display_format='YYYY-MM-DD',
                        min_date_allowed=datetime(2020, 1, 1),
                        max_date_allowed=datetime(2022, 12, 31),
                        initial_visible_month=datetime(2020, 1, 1),
                    ),
                    html.H5(
                        "Select the locations to be studied:"),
                    dcc.Checklist(id='choice-location',
                                  options=[{'label': x, 'value': x}
                                           for x in lineage_list],
                                  labelStyle={'display': 'inline-block', 'marginRight': '20px'}),
                    # First dropdown for selecting DNA or Protein
                    html.H5(
                        "Selecte the type sequences data to be studied:"),
                    dcc.Dropdown(
                        id='type-dropdown2',
                        options=[
                            {'label': 'Nucleotide', 'value': 'dna'},
                            {'label': 'Protein', 'value': 'protein'}
                        ],
                        value=None
                    ),
                    # Placeholder for the protein name radio items (initially hidden)
                    html.Div(id='protein-name-container2', style={'display': 'none'}, children=[
                        dcc.RadioItems(
                            id='protein-name-radio2',
                            options=[
                                {'label': i, 'value': i}
                                for i in protein_list
                            ],
                            value=None
                        )
                    ]),

                    dbc.Button("Confirm",
                               id="button-confir-lineage2", outline=True, color="success", className="me-1"),
                    # Output for displaying the selected values
                    html.Div(id='output-container2',
                             style={'margin-top': '20px'}),
                    # Valid message
                    html.Div(id='valid-message2'),

                    # ------------------------------------
                    html.Hr(),

                    # ----Row 2-2: Dash Table (begin) -------
                ],
                    id='exploreLocation', is_open=False,   # the Id of Collapse
                ),




                # ----------we are in dbc.Row (2)------------------------------------------------------------------
            ], xs=12, sm=12, md=12, lg=12, xl=12),

        ], justify='around'),


        # ----Row 2 end ---




        # ---------------------





    ]),
])

# ----------------------------


@app.callback(
    Output("exploreLocation", "is_open"),
    [Input("button-ExploreLocation", "n_clicks")],
    [State("exploreLocation", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("exploreLineage", "is_open"),
    [Input("button-ExploreLineage", "n_clicks")],
    [State("exploreLineage", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
# ------------------------------------------
# select protein name


@app.callback(
    Output('protein-name-container', 'style'),
    Output('protein-name-radio', 'value'),
    Input('type-dropdown', 'value')
)
def display_protein_name_dropdown(value):
    if value == 'protein':
        return {'display': 'block'}, None
    else:
        return {'display': 'none'}, None
# -----------------------------------------------
# Check seque type selected


@app.callback(
    Output('output-container', 'children'),
    # Input('button-confir-lineage', 'n_clicks'),
    Input('type-dropdown', 'value'),
    Input('protein-name-radio', 'value'),
    prevent_initial_call=True
)
def display_selected_values(type_value, protein_name):
    if type_value == 'protein':
        return f'Selected type: {type_value}, Protein name: {protein_name}'
    else:
        return f'Selected type: {type_value}'


# --------------------------------------------


@app.callback(
    Output('lineage-table', 'data'),
    Output('valid-message', 'children'),
    [Input('button-confir-lineage', 'n_clicks'),
     State('choice-lineage', 'value'),
     State('type-dropdown', 'value'),
     # State('protein-name-radio', 'value'),
     ],
)
def update_table(n, checklist_value, seqType_value):

    if n is None:
        return None, None
    else:
        if checklist_value and seqType_value:
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
            return table_data, None
        # elif not start_date or not end_date:
        #     return html.Div("Please select a date range.")
        elif not checklist_value:
            message = html.Div(
                "Please select at least one option from the checklist.")
            return None, message
        elif not seqType_value:
            message = html.Div(
                "Please select sequence type.")
            return None, message


# ---------- Visual Cyto----------------------


@app.callback(
    Output('row-count', 'children'),
    Output('cyto-container', 'children'),
    [
        # Input('button-confir-filter', 'n_clicks'),
        Input(component_id='lineage-table',
              component_property="derived_virtual_data")]
)
def check_update(all_rows_data):
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
                    'selector': 'node',
                    'style': {
                        'content': 'data(label)'
                    }
                },
                {
                    'selector': 'edge',
                    'style': {
                        'label': 'data(weight)'
                    }
                },
                {
                    'selector': '[weight > 30]',
                    'style': {
                        'line-color': 'blue',
                    }
                }
            ]
        )

    return row_count, mycyto
    # ---------------------------------------------
# change the page URL


@app.callback(
    Output('url', 'pathname'),
    Input('button-confir-filter', 'n_clicks'),
    Input('type-dropdown', 'value'),
    Input('protein-name-radio', 'value'),
    State(component_id='lineage-table',
          component_property="derived_virtual_data"),
    # prevent_initial_call=True
)
def update_page2_url(n_clicks, seq_type, protein_name, all_rows_data):
    if n_clicks is None:
        return dash.no_update
    else:
        dff = pd.DataFrame(all_rows_data)
        if dff.empty != True:
            # global_df = dff
            print(
                f'---------------submitted df--------------Size {dff.shape}')
            # print(dff)
            inputNode_name = generate_unique_name()
            if seq_type == 'dna':
                seq_accession_lt = getNucleoIdFromLineageFilter(dff)
                print(seq_accession_lt)
                addInputNeo('Nucleotide', inputNode_name, seq_accession_lt)
            elif seq_type == 'protein':
                seq_accession_lt = getProteinIdFromLineageFilter(
                    dff, protein_name)
                print(seq_accession_lt)
                addInputNeo('Protein', inputNode_name, seq_accession_lt)

            update_inputYaml('input_name', inputNode_name)

            url = 'apps/parameters'
            return url
