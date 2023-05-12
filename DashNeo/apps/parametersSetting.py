from dash import dcc, html
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
from app import app

# -----------------------------------------
layout = html.Div([
    html.Div(html.H2("Parameters Setting"), style={"text-align": "center"}),
    html.Hr(),
    # --------------
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
                html.Div([

                    # ---------------------------------
                    # --------------------------------
                ]),

            ], xs=12, sm=12, md=12, lg=10, xl=10),

        ], justify='around'),




    ]),

    # --------------------------
])
