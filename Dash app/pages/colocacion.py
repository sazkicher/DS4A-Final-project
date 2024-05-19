# Import libraries
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
from dash_labs.plugins.pages import register_page
from matplotlib.pyplot import figimage
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import pathlib
from components.data.load_df import colocacion
from components.data.create_df import create_df, filter_df, filter_idx
from components.plots.line_plots import line_plot_range, line_plot_two_axis
from components.kpi.kpibadge import kpibadge

register_page(__name__, path='/colocacion')

# Loading the data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../datasets').resolve()
colocacion = colocacion(DATA_PATH, 'colocacion.xlsx')

## Create dataframes for figures


# Create the figures
## Colocacion
### fig 1
df = filter_df(df=colocacion, x=['mes_desembolso'], y='mes_desembolso', filters=[], agg_function='count', to_frame='cantidad')
total_col = df['cantidad'].sum()

fig1 = px.line(df, x="mes_desembolso", y="cantidad", markers=True, labels={'mes_desembolso':'Mes', 'cantidad':'Cantidad'}, template='ggplot2')
fig1.update_traces(line_color='#34A527')
fig1.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across")
fig1.update_yaxes(showspikes=True, spikecolor="orange", spikethickness=2)
fig1.update_layout(spikedistance=1000, hoverdistance=100)

### fig 3
tasa_promedio = colocacion['tasa'].mean()
df = filter_df(df=colocacion, x=['mes_desembolso'], y=['tasa'], filters=[], agg_function='descr')
df.columns = df.columns.droplevel(0)
df = df.rename(columns={'':'mes_desembolso', 'count':'cantidad', 'mean':'tasa promedio', 'std':'desv.est', 'min':'tasa mínima', '25%':'Q1/25%', '50%':'mediana', '75%': 'Q3/75%', 'max': 'tasa máxima' })

fig3 = line_plot_range(df, xtitle='Mes', ytitle='Tasa de colocación')

### fig 5
df = filter_df(df=colocacion, x=['mes_desembolso'], y=['valor_desembolsado'], filters=[], agg_function='sum')

fig5 = px.histogram(df, x="valor_desembolsado", marginal="box", nbins=20, text_auto=True, color_discrete_sequence=['#34A527'], labels={'valor_desembolsado':'Valor desembolsado'}, template='ggplot2')
### fig 6
df = filter_df(df=colocacion, x=['mes_desembolso'], y='valor_desembolsado', filters=[], agg_function='count', to_frame='Cantidad')

fig6 = px.histogram(df, x="Cantidad", marginal="box", nbins=20, text_auto=True, color_discrete_sequence=['#34A527'], labels={'Cantidad':'Nro. de desembolsos'}, template='ggplot2')

### fig 2
df = filter_df(df=colocacion, x=['cedula'], y='cedula', filters=[], agg_function='count', to_frame='Nro. obligaciones')
df = df['Nro. obligaciones'].value_counts().to_frame('Cantidad').reset_index()
df = df.rename(columns={'index':'Nro. obligaciones'})

fig2 = px.bar(df, x="Nro. obligaciones", y="Cantidad", color="Cantidad", text_auto=True, color_continuous_scale='temps', template='ggplot2')

### fig 7 and 8
df = colocacion.copy()
# green, orrd,  oranges, oryel
fig8 = px.density_heatmap(data_frame=df, x="mes_desembolso", y="tasa", color_continuous_scale="greens", labels={'mes_desembolso':'Mes', 'tasa':'Tasa'}, template='ggplot2')
fig7 = px.box(df, x="mes_desembolso", y="tasa", color_discrete_sequence=['#34A527'], labels={'mes_desembolso':'Mes', 'tasa':'Tasa'}, template='ggplot2')

### fig 4
desembolso_prom = colocacion['valor_desembolsado'].mean()
df = filter_df(df=colocacion, x=['mes_desembolso'], y=['valor_desembolsado'], filters=[], agg_function='descr')
df.columns = df.columns.droplevel(0)
df = df.rename(columns={'':'mes_desembolso', 'count':'cantidad', 'mean':'promedio (miles_$)', 'std':'desv.est', 'min':'mínimo', '25%':'Q1/25%', '50%':'mediana', '75%': 'Q3/75%', 'max': 'máximo'})

fig4 = line_plot_two_axis(df, xtitle='Mes', y1_title="<b>Promedio de desembolsos</b>, Q1,Q3 y mínimo",
                          y2_title="<b>Máximo de desembolsos</b>")


# Filter values
region_list = colocacion['region'].unique()
linea_list = colocacion['linea'].unique()
estrato_list = colocacion['estrato'].sort_values().unique()
municipio_list = colocacion['municipio'].unique()
profesion_list = colocacion['profesion'].unique()
sucursal_list = colocacion['sucursal'].unique()
year_list = colocacion['año_desembolso'].unique()
mes_list = colocacion['nombre_mes'].sort_values().unique()

# Layout

# número total de colocaciones, promedio del valor de desembolsos, promedio de la tasa.
# Colores de gráficas
# Títulos 
# Ejes

kpi1 = kpibadge(round(total_col, 2), 'Total colocaciones')
kpi2 = kpibadge('$'+str(round(desembolso_prom, 2)), 'Valor promedio de desembolsos')
kpi3 = kpibadge(str(round(tasa_promedio, 2))+'%', 'Tasa promedio')

offcanvas = html.Div(
    [
        dbc.Button("Filtros", id="open-offcanvas", className="bfiltros", n_clicks=0),
        dbc.Offcanvas(
            [
                html.P("Seleccione:"),
                dcc.Dropdown(id='año_dropdown', options=year_list, placeholder='Año', className='filtro'),
                dcc.Dropdown(id='mes_dropdown', options=mes_list, placeholder='Mes', className='filtro'),
                dcc.Dropdown(id='region_dropdown', options=region_list, placeholder='Región', className='filtro'),
                dcc.Dropdown(id='sucursal_dropdown', options=sucursal_list, placeholder='Sucursal', className='filtro'),
                dcc.Dropdown(id='municipio_dropdown', options=municipio_list, placeholder='Municipio', className='filtro'),
                dcc.Dropdown(id='linea_dropdown', options=linea_list, placeholder='Línea', className='filtro'),
                dcc.Dropdown(id='estrato_dropdown', options=estrato_list, placeholder='Estrato', className='filtro'),
                dcc.Dropdown(id='profesion_dropdown', options=profesion_list, placeholder='Profesión', className='filtro'),
                dbc.Button(['Filtrar'], id='button_filter', className='bfiltrar'),
                html.Div(id='filter-message', children='', className='errorfiltros')
            ],
            id="offcanvas",
            title="Filtros",
            is_open=False,
            ),
    ]
)

layout = html.Div([
    offcanvas,
    dbc.Row([
        dbc.Col(children=[
            kpi1.display()
        ], className='kpi', id='total-colocaciones'),
        dbc.Col(children=[
            kpi2.display()
        ], className='kpi', id='desembolso-promedio'),
        dbc.Col(children=[
            kpi3.display()
        ], className='kpi', id='tasa-promedio'),
    ], justify='center'),
    dbc.Row([
        dbc.Col([
            html.Div("Cantidad de desembolsos mensuales 2017 - 2021", className="titulosvis"),
            dcc.Graph(figure=fig1, id='main-figure1'),
        ], md=6),
        dbc.Col([
            html.Div('Cantidad de obligaciones por cliente/cédula 2017 - 2021', className='titulosvis'),
            dcc.Graph(figure=fig2, id='main-figure2')
        ], md=6),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div('Tasa de colocación promedio y quartiles Q1/Q3 2017 - 2021', className='titulosvis'),
            dcc.Graph(figure=fig3, id='main-figure3')
        ]),
        dbc.Col([
            html.Div('Desembolsos promedios mensuales y quartiles Q1/Q3 2017 - 2021', className='titulosvis'),
            dcc.Graph(figure=fig4, id='main-figure4')
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div('Valor de desembolsos mensuales 2017 - 2021', className='titulosvis'),
            dcc.Graph(figure=fig5, id='main-figure5')
        ]),
        dbc.Col([
            html.Div('Cantidad de desembolsos mensuales 2017 - 2021', className='titulosvis'),
            dcc.Graph(figure=fig6, id='main-figure6')
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div('Tasa de Colocación mensual 2017 - 2021', className='titulosvis'),
            dcc.Graph(figure=fig7, id='main-figure7')
        ]),
        dbc.Col([
            html.Div('Tasa de Colocación mensual 2017 - 2021', className='titulosvis'),
            dcc.Graph(figure=fig8, id='main-figure8')
        ]),
    ]),
])

# Callbacks
input_list = [State('año_dropdown', 'value'), State('mes_dropdown', 'value'),
              State('region_dropdown', 'value'), State('sucursal_dropdown', 'value'),
              State('municipio_dropdown', 'value'), State('linea_dropdown', 'value'),
              State('estrato_dropdown', 'value'), State('profesion_dropdown', 'value'),
              Input('button_filter', 'n_clicks'),
              Input("open-offcanvas", "n_clicks"),
              State("offcanvas", "is_open")]

output_list = [Output('main-figure1', 'figure'), Output('main-figure2', 'figure'),
	           Output('main-figure3', 'figure'), Output('main-figure4', 'figure'),
               Output('main-figure5', 'figure'), Output('main-figure6', 'figure'),
	           Output('main-figure7', 'figure'), Output('main-figure8', 'figure'),
               Output('total-colocaciones', 'children'), Output('desembolso-promedio', 'children'),
               Output('tasa-promedio', 'children'),
               Output('filter-message', 'children')]

@callback(output_list, input_list[:-2], prevent_initial_call=True)
def update_figs(año, mes, region, sucursal, municipio, linea, estrato, profesion, n_clicks):
    filters = ['año_desembolso', 'nombre_mes', 'region', 'sucursal', 'municipio', 'linea', 'estrato', 'profesion']
    filter_values = [año, mes, region, sucursal, municipio, linea, estrato, profesion]
    message = ''
    print(any(filter_idx(colocacion, filters, filter_values)))
    if not any(filter_idx(colocacion, filters, filter_values)):
        filters = []
        filter_values = [None]
        message = 'No existen registros con esta combinación de filtros.'

    ## fig 1
    df = filter_df(df=colocacion, x=['mes_desembolso'], y='mes_desembolso', filters=filters, agg_function='count', to_frame='cantidad',
                    filter_values=filter_values)
    total_col = df['cantidad'].sum()

    fig1 = px.line(df, x="mes_desembolso", y="cantidad", markers=True, labels={'mes_desembolso':'Mes', 'cantidad':'Cantidad'}, template='ggplot2')
    fig1.update_traces(line_color='#34A527')
    fig1.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across")
    fig1.update_yaxes(showspikes=True, spikecolor="orange", spikethickness=2)
    fig1.update_layout(spikedistance=1000, hoverdistance=100)

    ## fig 3
    df = colocacion[filter_idx(colocacion, filters, filter_values)]
    tasa_promedio = df['tasa'].mean()
    df = create_df(df=df, x=['mes_desembolso'], y=['tasa'], filters=[], agg_function='descr')
    df.columns = df.columns.droplevel(0)
    df = df.rename(columns={'':'mes_desembolso', 'count':'cantidad', 'mean':'tasa promedio', 'std':'desv.est', 'min':'tasa mínima', '25%':'Q1/25%', '50%':'mediana', '75%': 'Q3/75%', 'max': 'tasa máxima' })

    fig3 = line_plot_range(df, xtitle='Mes', ytitle='Tasa de colocación')

    ## fig 5
    df = filter_df(df=colocacion, x=['mes_desembolso'], y=['valor_desembolsado'], filters=filters, agg_function='sum', filter_values=filter_values)

    fig5 = px.histogram(df, x="valor_desembolsado", marginal="box", nbins=20, text_auto=True, color_discrete_sequence=['#34A527'], labels={'valor_desembolsado':'Valor desembolsado'}, template='ggplot2')

    ## fig 6 
    df = filter_df(df=colocacion, x=['mes_desembolso'], y='valor_desembolsado', filters=filters, agg_function='count', to_frame='Cantidad', filter_values=filter_values)

    fig6 = px.histogram(df, x="Cantidad", marginal="box", nbins=20, text_auto=True, color_discrete_sequence=['#34A527'], labels={'Cantidad':'Nro. de desembolsos'}, template='ggplot2')

    ## fig 2
    df = filter_df(df=colocacion, x=['cedula'], y='cedula', filters=filters, agg_function='count', to_frame='Nro. obligaciones', filter_values=filter_values)
    df = df['Nro. obligaciones'].value_counts().to_frame('Cantidad').reset_index()
    df = df.rename(columns={'index':'Nro. obligaciones'})

    fig2 = px.bar(df, x="Nro. obligaciones", y="Cantidad", color="Cantidad", text_auto=True, color_continuous_scale='temps', template='ggplot2')

    ## fig 7 and 8
    df = colocacion[filter_idx(colocacion, filters, filter_values)]

    fig8 = px.density_heatmap(data_frame=df, x="mes_desembolso", y="tasa", color_continuous_scale="greens", labels={'mes_desembolso':'Mes', 'tasa':'Tasa'}, template='ggplot2')
    fig7 = px.box(df, x="mes_desembolso", y="tasa", color_discrete_sequence=['#34A527'], labels={'mes_desembolso':'Mes', 'tasa':'Tasa'}, template='ggplot2')

    ## fig 4
    df = colocacion[filter_idx(colocacion, filters, filter_values)]
    desembolso_prom = df['valor_desembolsado'].mean()
    df = filter_df(df=df, x=['mes_desembolso'], y=['valor_desembolsado'], filters=[], agg_function='descr')
    df.columns = df.columns.droplevel(0)
    df = df.rename(columns={'':'mes_desembolso', 'count':'cantidad', 'mean':'promedio (miles_$)', 'std':'desv.est', 'min':'mínimo', '25%':'Q1/25%', '50%':'mediana', '75%': 'Q3/75%', 'max': 'máximo'})

    fig4 = line_plot_two_axis(df, xtitle='Mes', y1_title="<b>Promedio de desembolsos</b>, Q1,Q3 y mínimo",
                          y2_title="<b>Máximo de desembolsos</b>")

    ## kpis
    kpi1 = kpibadge(round(total_col, 2), 'Total colocaciones')
    kpi2 = kpibadge('$'+str(round(desembolso_prom, 2)), 'Valor promedio de desembolsos')
    kpi3 = kpibadge(str(round(tasa_promedio, 2))+'%', 'Tasa promedio')

    return [fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, kpi1.display(),
            kpi2.display(), kpi3.display(), message]

@callback(Output('offcanvas', 'is_open'), input_list)
def toggle_offcanvas(año, mes, region, sucursal, municipio, linea, estrato, profesion, n2, n1, is_open):
    print('--------------')
    print(n1, n2, is_open)
    if n1 or n2:
        print(n1, n2, is_open)
        is_open = not is_open
    filters = ['año_desembolso', 'nombre_mes', 'region', 'sucursal', 'municipio', 'linea', 'estrato', 'profesion']
    filter_values = [año, mes, region, sucursal, municipio, linea, estrato, profesion]
    if not any(filter_idx(colocacion, filters, filter_values)):
        is_open = True
    
    print(n1, n2, is_open)
    return is_open
# @callback(
#     Output("offcanvas", "is_open"),
#     Input("open-offcanvas", "n_clicks"), Input('button_filter', 'n_clicks'),
#     [State("offcanvas", "is_open")],
# )
# def toggle_offcanvas(n1, n2, is_open):
#     print('--------------')
#     print(n1, n2, is_open)
    
#     if n1:
#         print(n1, n2, is_open)
#         return not is_open
#     return is_open