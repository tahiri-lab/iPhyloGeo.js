from dash import dcc, html
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
from app import app
import dash
from apps import config_manager
from apps import neoCypher_manager
# from dash.exceptions import PreventUpdate


# -----------------------------------------


# --------------------------------------
layout = html.Div([
    html.Div(html.H2("Parameters Setting"), style={"text-align": "center"}),
    html.Hr(),
    # html.Div(id='page-2-content'),
    # --------------------------------------------------------
    # Get info from page neoExplore
    # html.P(f"Content of dcc.Store: {stored_data}"),
    dbc.Row([
            dbc.Col([
                dbc.Button("Get Input Id",
                           id="get_input_name", outline=True, color="success", className="me-1"),
                html.Br(),
                dcc.Loading(
                    id='loading',
                    type='circle',
                    children=[
                        dcc.Textarea(
                            id="textarea_id",
                            value='',
                            style={"height": 50, 'color': 'blue'},
                            readOnly=True,
                        ),
                        dcc.Clipboard(
                            id="clipboard_id",
                            target_id="textarea_id",
                            title="Copy",
                            style={
                                "display": "inline-block",
                                "fontSize": 20,
                                "verticalAlign": "top",
                                "marginLeft": "10px"
                            },
                        ),
                        dcc.Store(id='seq-length-store',
                                  storage_type='session'),
                    ]),



            ], xs=12, sm=12, md=12, lg=10, xl=10),

            ], justify='around'),

    # --------------
    dbc.Row([

        dbc.Col([
            html.Div([
                html.H3("Bootstrap value threshold"),
                dcc.Slider(id='BootstrapThreshold-slider2',
                           min=0,
                           max=100,
                           step=0.1,
                           marks={
                               0: {'label': '0.0%', 'style': {'color': '#77b0b1'}},
                               25: {'label': '25.0%', 'style': {'color': '#77b0b1'}},
                               50: {'label': '50.0%', 'style': {'color': '#77b0b1'}},
                               75: {'label': '75.0%', 'style': {'color': '#77b0b1'}},
                               100: {'label': '100.0%', 'style': {'color': '#77b0b1'}}},
                           value=10),
                html.Div(id='BootstrapThreshold-slider-output-container2')
            ]),
        ],  # width={'size':5, 'offset':0, 'order':2},
            xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            html.Div([
                html.H3("Robinson and Foulds distance threshold"),
                dcc.Slider(id='RF-distanceThreshold-slider2',
                           min=0,
                           max=100,
                           step=0.1,
                           marks={
                               0: {'label': '0.0%', 'style': {'color': '#77b0b1'}},
                               25: {'label': '25.0%', 'style': {'color': '#77b0b1'}},
                               50: {'label': '50.0%', 'style': {'color': '#77b0b1'}},
                               75: {'label': '75.0%', 'style': {'color': '#77b0b1'}},
                               100: {'label': '100.0%', 'style': {'color': '#77b0b1'}}},
                           value=10),
                html.Div(id='RFThreshold-slider-output-container2'),
            ]),
        ],  # width={'size':5, 'offset':0, 'order':2},
            xs=12, sm=12, md=12, lg=5, xl=5
        ),
    ],  justify='around'),  # Horizontal:start,center,end,between,around

    dbc.Row([

        dbc.Col([
            html.Div(id='output-fasta2'),
        ],  # width={'size':3, 'offset':1, 'order':1},
            xs=12, sm=12, md=12, lg=10, xl=10
        ),
    ],  justify='around'),  # Horizontal:start,center,end,between,around

    # for sliding window siza & step size
    dbc.Row([

        dbc.Col([
            html.Div([
                html.H3("Sliding window size"),
                dcc.Input(id="input_windowSize2", type="number", min=0,
                          # max=max(ref_genes_len.values())-1,
                          placeholder="Enter Sliding Window Size", value=0,
                          style={'width': '65%', 'marginRight': '20px'}),
                html.Div(id='input_windowSize-container2'),
            ]),

        ],  # width={'size':3, 'offset':1, 'order':1},
            xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            html.Div([
                html.H3("Step size"),
                dcc.Input(id="input_stepSize2", type="number", min=0,
                          # max=max(ref_genes_len.values())-1,
                          placeholder="Enter Step Size", value=0,
                          style={'width': '65%', 'marginRight': '20px'}),
                html.Div(id='input_stepSize-container2'),
            ]),
        ],  # width={'size':3, 'offset':1, 'order':1},
            xs=12, sm=12, md=12, lg=5, xl=5
        ),
    ],  justify='around'),  # Horizontal:start,center,end,between,around


    # ----------
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div(),
            ], xs=12, sm=12, md=12, lg=5, xl=5),
            dbc.Col([
                html.Div(),
            ], xs=12, sm=12, md=12, lg=5, xl=5),

        ], justify='around'),

        html.Br(),
        html.Br(),


        # dbc.Row([
        #     dbc.Col([
        #         html.Div(card4),
        #     ], xs=12, sm=12, md=12, lg=12, xl=12),

        # ], justify='around'),

    ], fluid=True),

    # ----------
    dbc.Container([
        dbc.Row([
            dbc.Col([


            ], xs=12, sm=12, md=12, lg=10, xl=10),

        ], justify='around'),




    ]),

    # --------------------------
])

# --------------------------------------------------------------
# get seq length and input node id


@app.callback(
    Output('textarea_id', 'value'),
    Output('seq-length-store', 'data'),
    Input('get_input_name', 'n_clicks')
)
def retrieve_config_values(n):
    if n is None:
        return None, None
    else:
        config = config_manager.read_config()
        if config['params']['data_type'] == 'dna':
            nodesLabel = 'Nucleotide'
        else:
            nodesLabel = 'Protein'
        seq_list = config['seqinfo']['accession_lt']
        ref_genes_len = neoCypher_manager.get_seq_length(nodesLabel, seq_list)
        print(ref_genes_len)
        input_name = config['input']['input_name']
        # message = f"Input Id: {input_name}"
        return input_name, ref_genes_len

    # ----------------------------------

# ------------------------------------
# view the value chosen


@app.callback(
    dash.dependencies.Output(
        'BootstrapThreshold-slider-output-container2', 'children'),
    [dash.dependencies.Input('BootstrapThreshold-slider2', 'value')])
def update_output(value):
    return 'You have selected {:0.1f}%'.format(value)


@app.callback(
    dash.dependencies.Output(
        'RFThreshold-slider-output-container2', 'children'),
    [dash.dependencies.Input('RF-distanceThreshold-slider2', 'value')])
def update_output(value):
    return 'You have selected {:0.1f}%'.format(value)
# get seq length for the validation of 'sliding window size' and 'step size'
# By default, the length of 'ORF10'(117bp) was used as the ref_genes_len, since this is the minimun sequence length in our database
# Once user click the 'Get Input ID' button
# (1) sequence list in the config.yaml file calculate the minimum lengh of seq


@app.callback(
    dash.dependencies.Output('input_windowSize-container2', 'children'),
    [dash.dependencies.Input('input_stepSize2', 'value'),
     Input('seq-length-store', 'data'),
     ])
def update_output(stepSize, ref_genes_len):
    if ref_genes_len != None:
        if stepSize == None:
            value_max = int(ref_genes_len) - 1
        else:
            value_max = int(ref_genes_len) - 1 - stepSize
        return 'The input value must an integer from o to {}'.format(value_max)
    else:
        return 'The input value must an integer from o to 117'


@app.callback(
    dash.dependencies.Output('input_stepSize-container2', 'children'),
    [dash.dependencies.Input('input_windowSize2', 'value'),
     Input('seq-length-store', 'data'),
     ])
def update_output(windowSize, ref_genes_len):
    if ref_genes_len != None:
        if windowSize == None:
            value_max = int(ref_genes_len) - 1
        else:
            value_max = int(ref_genes_len) - 1 - windowSize
        return 'The input value must be an integer from 0 to {}'.format(value_max)
    else:
        return 'The input value must an integer from o to 117'


# -------------------------------------------------
