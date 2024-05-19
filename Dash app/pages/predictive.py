# Load your libraries
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
from dash_labs.plugins.pages import register_page
import plotly.express as px
import pandas as pd
import json
import pathlib
import pickle
import numpy as np
from components.data.load_df import modelo

register_page(__name__, path='/predictive')

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../datasets').resolve()
scaler, encoder, df_modelo = modelo(DATA_PATH, 'dataset_modelo.csv')

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../components/models/').resolve()
fitted_model = pickle.load(open(DATA_PATH.joinpath('svm_clf.sav'), 'rb'))
rf_model = pickle.load(open(DATA_PATH.joinpath('Random_forest.sav'), 'rb'))
X_new = [-1.74885626, -0.13197948, -1.39706395, -1.3154443 ]
output = fitted_model.predict([X_new])

sector_list = df_modelo['sector'].unique()
region_list = df_modelo['regional'].unique()
actividad_list = df_modelo['actividad_econ'].unique()
vivienda_list = df_modelo['vivienda'].unique()
estado_civ_list = df_modelo['estado_civil'].unique()
genero_list = df_modelo['genero'].unique()
educ_list = df_modelo['educ'].unique()
mujer_cabeza_list = df_modelo['mujer_cabeza'].unique()
responsable_hog_list = df_modelo['responsable_hogar'].unique()

# Layout

layout = html.Div([
    dbc.Row('Predictive'), 
    dbc.Row(id='prediction', children=f'Prediction: {output}'),
    dbc.Row([
        dbc.Col(dbc.Input(id='edad', type='number', placeholder='Edad', className='filtro')),
        dbc.Col(dbc.Input(id='monto', type='number', placeholder='Monto', className='filtro')),
        dbc.Col(dbc.Input(id='cuotas', type='number', placeholder='Cuotas', className='filtro')),
        dbc.Col(dbc.Input(id='tasa', type='number', placeholder='Tasa'), className='filtro'),
    ]), 
    dbc.Row([
        dbc.Col(dcc.Dropdown(id='sector_dropdown', options=sector_list, placeholder='Sector', className='filtro')),
        dbc.Col(dcc.Dropdown(id='region_dropdown', options=region_list, placeholder='Región', className='filtro')),
        dbc.Col(dcc.Dropdown(id='actividad_dropdown', options=actividad_list, placeholder='Actividad', className='filtro')),
        dbc.Col(dcc.Dropdown(id='vivienda_dropdown', options=vivienda_list, placeholder='Vivienda', className='filtro')),
        dbc.Col(dcc.Dropdown(id='estado_civ_dropdown', options=estado_civ_list, placeholder='Estado civil', className='filtro')),
        dbc.Col(dcc.Dropdown(id='genero_dropdown', options=genero_list, placeholder='Género', className='filtro')),
        dbc.Col(dcc.Dropdown(id='educ_dropdown', options=educ_list, placeholder='Educación', className='filtro')),
        dbc.Col(dcc.Dropdown(id='mujer_cab_dropdown', options=mujer_cabeza_list, placeholder='Mujer cabeza de flia', className='filtro')),
        dbc.Col(dcc.Dropdown(id='responsable_hog_dropdown', options=responsable_hog_list, placeholder='Responsable hogar', className='filtro')),
    ]),
    dbc.Row(        
        dbc.Col(dbc.Button(['Clasificar'], id='prediction_button'))
    )
])

@callback(Output('prediction', 'children'),
          [State('edad', 'value'), State('monto', 'value'),
          State('cuotas', 'value'), State('tasa', 'value'),
          State('sector_dropdown', 'value'), State('region_dropdown', 'value'),
          State('actividad_dropdown', 'value'), State('vivienda_dropdown', 'value'),
          State('estado_civ_dropdown', 'value'), State('genero_dropdown', 'value'),
          State('educ_dropdown', 'value'), State('mujer_cab_dropdown', 'value'),
          State('responsable_hog_dropdown', 'value'),
          Input('prediction_button', 'n_clicks')],
          prevent_initial_call=True
        )
def classify(edad, monto, cuotas, tasa, sector, region, actividad, vivienda_prop, estado_civ, genero, educación, mujer_cab, responsable_hog, n_clicks):
    features = [edad, monto, cuotas, tasa, sector, region, actividad, vivienda_prop, estado_civ, genero, educación, mujer_cab, responsable_hog]
    if any(value is None for value in features):
        return 'Debe seleccionar un valor para todas los campos.'
    num_features = pd.DataFrame(data=[features[:4]], columns=['edad', 'monto', 'cuotas', 'tasa'])
    cat_features = pd.DataFrame(data=[features[4:]], columns=['sector', 'regional', 'actividad_econ', 'vivienda', 'estado_civil', 'genero', 'educ',
                                                            'mujer_cabeza', 'responsable_hogar'])
    num_features = scaler.transform(num_features)
    cat_features = encoder.transform(cat_features).toarray()
    features = np.concatenate((num_features, cat_features, np.array([[1]])), axis=1)
    predicted_class = rf_model.predict(features)
    output = f'Prediction: {predicted_class}'

    return output






