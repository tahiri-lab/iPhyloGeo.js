from dash import dcc, html
# import dash_core_components as dcc
# import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import homePage, neoExplore, parametersSetting


# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "26rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "25rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Tahiri Lab", className="display-4"),
        html.Hr(),
        html.H3(
            "Phylogeography", className='text-center text-primary mb-3'
        ),
        dbc.Nav(
            [dbc.NavLink("Home", href='/apps/homePage', active="exact"),
             dbc.NavLink("Cov-Lineages Exploreration",
                         href='/apps/neoExplore', active="exact"),
             # dbc.NavLink("Perameters", href='/apps/parameters', active="exact"),
             # dbc.NavLink("Using Our Meteorological Data (SARS-CoV-2)", href='/apps/usingOurDataset', active="exact"),
             # dbc.NavLink("Phylogeography Analysis With Our Data (SARS-CoV-2, whole sequences)", href='/apps/pipelineWithOurData', active="exact"),
             # dbc.NavLink("Phylogeography Analysis With Our Data (SARS-CoV-2, specific genes)", href='/apps/pipelineCoVGenes', active="exact"),
             # dbc.NavLink("Check Results", href='/apps/checkResults', active="exact"),
             ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/homePage':
        return homePage.layout
    if pathname == '/apps/neoExplore':
        return neoExplore.layout
    if pathname == '/apps/parameters':
        return parametersSetting.layout
    # if pathname.startswith('/apps/parameters'):
    #     return parametersSetting.layout
    # if pathname == '/apps/usingOurDataset':
    #     return usingOurDataset.layout
    # if pathname == '/apps/pipelineWithOurData':
    #     return pipelineWithOurData.layout
    else:
        return homePage.layout


if __name__ == '__main__':
    app.run_server(debug=True)
