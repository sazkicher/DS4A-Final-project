# Load your libraries
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd
import json

# Create the app

workspace_user = os.getenv('JUPYTERHUB_USER')  # Get DS4A Workspace user name
request_path_prefix = None
if workspace_user:
    request_path_prefix = '/user/' + workspace_user + '/proxy/8050/'

app = Dash(__name__, requests_pathname_prefix=request_path_prefix, external_stylesheets=[dbc.themes.FLATLY],
                meta_tags=[{'name':'viewport', 'content':'width=device-width, initial-scale=1.0'}])
app.title = 'Fundacion Amanecer - Correlation One'                 

#Loading the data

path = 'Data/'
filename = 'allCierreCartera.csv'
cierre_cart = pd.read_csv(path+filename, low_memory=False,
                            dtype={'edad':'float', 'estrato':'category',
                                  'cedula':'category'})
cierre_cart['fec nacimiento'] = cierre_cart['fec nacimiento'].astype('datetime64[ns]')
cierre_cart['fec solicitud'] = cierre_cart['fec solicitud'].astype('datetime64[ns]')
cierre_cart['fec aproba'] = cierre_cart['fec aproba'].astype('datetime64[ns]')
cierre_cart['fec desembolso'] = cierre_cart['fec desembolso'].astype('datetime64[ns]')
cierre_cart['fec ult.pago'] = cierre_cart['fec ult.pago'].astype('datetime64[ns]')
cierre_cart['fec proximo pago'] = cierre_cart['fec proximo pago'].astype('datetime64[ns]')
cierre_cart['vencimiento final'] = cierre_cart['vencimiento final'].astype('datetime64[ns]')
cierre_cart['reg date'] = cierre_cart['reg date'].astype('datetime64[ns]')


drop_columns = ['nro solicitud', 'pagare', 'sucursal', 'fec solicitud', 'sucursal.1',
               'region.1', 'municipio', 'sucursales']
cierre_cart.drop(labels=drop_columns, axis=1, inplace=True)

# Create the figures

## Cierre Cartera 2017-2021
cierre_cart = cierre_cart[~cierre_cart['saldo obligacion'].isin([45270281317, 44799785497])]

linea = 'crecer'
region = 'region sur'

ind_calidad_tot = cierre_cart.groupby(['reg date', 'region', 'linea'])[['saldo obligacion', 'vencida']].sum().reset_index()
idx = (ind_calidad_tot['linea'].isin([linea]))&(ind_calidad_tot['region'].isin([region]))
df1 = ind_calidad_tot[idx]

fig1 = px.line(df1, x='reg date', y='saldo obligacion',
               title='Balance mensual',
               labels={'saldo obligacion':'Balance (COP)',
                      'reg date':'Month'},
              )

dia_pago = cierre_cart.copy()
dia_pago['dia_pago'] = cierre_cart['fec ult.pago'].dt.day
dia_pago = dia_pago.groupby(['dia_pago', 'region', 'linea'])['dia_pago'].count().to_frame('count').reset_index()
df2 = dia_pago[(dia_pago['region'].isin([region]))&(dia_pago['linea'].isin([linea]))]

fig2 = px.bar(df2, x='dia_pago', y='count', title='Número de pagos por día', 
             labels={'count':'Pagos', 'dia_pago':'Día'})

region_list = cierre_cart['region'].unique()
linea_list = cierre_cart['linea'].unique()


# Layout

app.layout = dbc.Container(
    [
           dbc.Row([
                    dbc.Col(
                    html.Img(
                    src="99999.jpg",
                    alt='Logo fundación',
                    style={
                        'width': 300,
                        'height': 163,
                        'border': 'thin grey solid',
                        }
                    ),
                    md=3),
                   dbc.Col(
                   html.H1("Fundacion amanecer", className="h-100 p-5 bg-light border rounded-3"),
                   md=9)
                   ],justify="start",style={"margin-bottom": "1rem"}),
        
           dbc.Row(
               dbc.Nav([
                   dbc.NavItem(dbc.NavLink("Loan Portafolio info", active=True, href="#")),
                   dbc.NavItem(dbc.NavLink("Client segmentation", href="#")),
                   dbc.NavItem(dbc.NavLink("Predictive analitycs", href="#")),
                       ],
                   pills=True,
                      )
                  ),
        
           html.Hr(style={'border': '2px solid green'}),

           dbc.Row([
               dbc.Col([dcc.Dropdown(id='region_dropdown', options=region_list, placeholder='Region')], width=2),
                dbc.Col([dcc.Dropdown(id='linea_dropdown', options=linea_list, placeholder='Línea')], width=2)
                   ], justify='end'),
           dbc.Row([
                dbc.Col(dcc.Graph(figure=fig1, id='main-figure1')),
                dbc.Col(dcc.Graph(figure=fig2, id='main-figure2'))
                  ]),
    ])



# Callbacks

@app.callback([Output('main-figure1', 'figure'), Output('main-figure2', 'figure')],
              [Input('region_dropdown', 'value'), Input('linea_dropdown', 'value')])
def update_figs(region, linea):
    idx = (ind_calidad_tot['linea'].isin([linea]))&(ind_calidad_tot['region'].isin([region]))
    df1 = ind_calidad_tot[idx]
    fig1 = px.line(df1, x='reg date', y='saldo obligacion', title='Balance mensual',
                   labels={'saldo obligacion':'Balance (COP)', 'reg date':'Month'})
    
    df2 = dia_pago[(dia_pago['region'].isin([region]))&(dia_pago['linea'].isin([linea]))]

    fig2 = px.bar(df2, x='dia_pago', y='count', title='Número de pagos por día', 
                  labels={'count':'Pagos', 'dia_pago':'Día'})
    
    return [fig1, fig2]


# Start the server
if __name__ == '__main__':
    app.run_server(host="localhost", port="8050", debug=True)