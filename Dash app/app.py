# Import libraries
import dash
import dash_labs as dl
import dash_bootstrap_components as dbc
import os
from dash import html

# Import our modules
from callbacks import register_callbacks

# Create the app
workspace_user = os.getenv('JUPYTERHUB_USER')
request_path_prefix = None
if workspace_user:
    request_path_prefix = '/user/' + workspace_user + '/proxy/8050/'
app = dash.Dash(__name__, requests_pathname_prefix=request_path_prefix,
                plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.ZEPHYR],
                meta_tags=[{'name':'viewport', 'content':'width=device-width, initial-scale=1.0'}])
app.config.suppress_callback_exceptions = True
app.title = 'Fundacion Amanecer - Correlation One'

# Page layout

logo = html.Img(src='assets/logo.jpg', alt='Logo fundación', className='logo')

navbar = dbc.Navbar([
    dbc.NavItem(dbc.NavLink("Colocación", href="/colocacion",style={'color':"#ffffff"})),
    dbc.NavItem(dbc.NavLink("Cartera", href="/cartera",style={'color':"#ffffff"})),
    dbc.NavItem(dbc.NavLink("Clientes", href="/client_seg",style={'color':"#ffffff"})),
    dbc.NavItem(dbc.NavLink("Predecir", href="/predictive",style={'color':"#ffffff"})),
    ],
    color="#0bac27",
    dark=True,
)

app.layout = dbc.Container([
    logo,
    navbar,
    dl.plugins.page_container
    ],
    className='dbc',
    fluid=True,
)

# Callbacks
register_callbacks(app)

# Start the server
server = app.server
if __name__ == '__main__':
    app.run_server(host="localhost", port="8050", debug=True)