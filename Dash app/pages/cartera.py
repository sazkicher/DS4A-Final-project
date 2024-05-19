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
from components.data.load_df import cartera, colocacion
from components.data.create_df import create_df, filter_df, filter_idx
from components.plots.line_plots import line_plot_range, line_plot_two_axis

register_page(__name__, path='/cartera')

# Loading the data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../datasets').resolve()
cierre_cart = cartera(DATA_PATH, 'allCierreCartera.csv')

# Creating figures
## fig 1
df = filter_df(df=cierre_cart, x=['dia_pago'], y='dia_pago', filters=[], agg_function='count', to_frame='count')

fig1 = px.bar(df, x='dia_pago', y='count', labels={'count':'Pagos', 'dia_pago':'Día del mes'}, color_discrete_sequence=['#34A527'])

## fig 2
df = filter_df(df=cierre_cart, x=['dia_semana'], y='dia_semana', filters=[], agg_function='count', to_frame='count')
df = df.reindex()

fig2 = px.bar(df, x='dia_semana', y='count', labels={'count':'Pagos', 'dia_semana':'Día de la semana'}, color_discrete_sequence=['#34A527'],
              category_orders={'dia_semana':['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']})

## fig 3
df = filter_df(df=cierre_cart, x=['dia_pago'], y=['valor cuota'], filters=[], agg_function='sum')

fig3 = px.bar(df, x='dia_pago', y='valor cuota', labels={'valor cuota':'Total pagado', 'dia_pago':'Día del mes'}, color_discrete_sequence=['#34A527'])

## fig 4
df = filter_df(df=cierre_cart, x=['region'], y=['valor cuota'], filters=[], agg_function='sum')

fig4 = px.bar(df, x='region', y='valor cuota', labels={'valor cuota':'Total pagado', 'region':'Región'}, color_discrete_sequence=['#34A527'])

## fig 5
df = filter_df(df=cierre_cart, x=['sucursal real'], y=['valor cuota'], filters=[], agg_function='sum')

fig5 = px.bar(df, x='sucursal real', y='valor cuota', labels={'valor cuota':'Total pagado', 'sucursal real':'Sucursal'}, color_discrete_sequence=['#34A527'])

## fig 6
df = filter_df(df=cierre_cart, x=['municipio cliente'], y=['valor cuota'], filters=[], agg_function='sum')

fig6 = px.bar(df, x='municipio cliente', y='valor cuota', color_discrete_sequence=['#34A527'], labels={'municipio cliente':'Municipio', 'valor cuota':'Total pagado'})

## fig 7
df = filter_df(df=cierre_cart, x=['periodicidad'], y=['valor cuota'], filters=[], agg_function='sum')

fig7 = px.bar(df, x='valor cuota', y='periodicidad', orientation='h', color_discrete_sequence=['#34A527'], labels={'peridiocidad':'Periodicidad', 'valor cuota':'Total pagado'})

## fig 8
df = filter_df(df=cierre_cart, x=['periodicidad'], y='valor cuota', filters=[], agg_function='count', to_frame='count')

fig8 = px.bar(df, x='count', y='periodicidad', orientation='h', color_discrete_sequence=['#34A527'], labels={'count':'Cantidad de pagos', 'periodicidad':'Periodicidad'})

# fig 9
df = cierre_cart[~cierre_cart['dia_pago'].isnull()]
df = filter_df(df=df, x=['fec ult.pago'], y='fec ult.pago', filters=[], agg_function='count', to_frame='count')

fig9 = px.bar(df, x="fec ult.pago", y="count",text_auto='.2s', labels={'count':'Número de pagos', 'dia_pago':'Día de pago' }, color_discrete_sequence=['#34A527'])
fig9.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
fig9.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across")
fig9.update_yaxes(showspikes=True, spikecolor="orange", spikethickness=2)

# Filter values
region_list = cierre_cart['region'].unique()
linea_list = cierre_cart['linea'].unique()
estrato_list = cierre_cart['estrato'].unique()
municipio_list = cierre_cart['municipio cliente'].unique()
profesion_list = cierre_cart['profesion'].unique()
sucursal_list = cierre_cart['sucursal real'].unique()
year_list = cierre_cart['reg año'].unique()
mes_list = cierre_cart['reg mes'].sort_values().unique()

# Layout

offcanvas = html.Div(
    [
        dbc.Button("Filtros", id="open-offcanvas-cart", className="bfiltros", n_clicks=0),
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
            ],
            id="offcanvas-cart",
            title="Filtros",
            is_open=False,
            ),
    ]
)

layout = html.Div([
    # html.Div([
    #     dbc.Col([dcc.Dropdown(id='año_dropdown', options=year_list, placeholder='Año', className='filtro')], width=1),
    #     dbc.Col([dcc.Dropdown(id='mes_dropdown', options=mes_list, placeholder='Mes', className='filtro')], width=1),
    #     dbc.Col([dcc.Dropdown(id='region_dropdown', options=region_list, placeholder='Region', className='filtro')], width=1),
    #     dbc.Col([dcc.Dropdown(id='sucursal_dropdown', options=sucursal_list, placeholder='Sucursal', className='filtro')], width=1),
    #     dbc.Col([dcc.Dropdown(id='municipio_dropdown', options=municipio_list, placeholder='Municipio', className='filtro')], width=1),
    #     dbc.Col([dcc.Dropdown(id='linea_dropdown', options=linea_list, placeholder='Línea', className='filtro')], width=1),
    #     dbc.Col([dcc.Dropdown(id='estrato_dropdown', options=estrato_list, placeholder='Estrato', className='filtro')], width=1),
    #     dbc.Col([dcc.Dropdown(id='profesion_dropdown', options=profesion_list, placeholder='Profesión', className='filtro')], width=1),
    #     dbc.Col([dbc.Button(['Filtrar'], id='button_filter', className='filtro')], width=1),
    #     ], className='barrafiltros d-flex flex-row-reverse'),
    offcanvas,
    dbc.Row([
        dbc.Col([
            html.Div('Número de pagos por día del mes', className="titulosvis"),
            dcc.Graph(figure=fig1, id='main-figure1_cart'),
        ], md=6),
        dbc.Col([
            html.Div('Número de pagos por día de la semana', className='titulosvis'),
            dcc.Graph(figure=fig2, id='main-figure2_cart')
        ], md=6),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div('Total de pagos por día del mes', className='titulosvis'),
            dcc.Graph(figure=fig3, id='main-figure3_cart')
        ]),
        dbc.Col([
            html.Div('Total de pagos por region', className='titulosvis'),
            dcc.Graph(figure=fig4, id='main-figure4_cart')
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div('Total de pago por Sucursal real', className='titulosvis'),
            dcc.Graph(figure=fig5, id='main-figure5_cart')
        ]),
        dbc.Col([
            html.Div('Total de pago por municipio', className='titulosvis'),
            dcc.Graph(figure=fig6, id='main-figure6_cart')
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div('Pago por periodicidad', className='titulosvis'),
            dcc.Graph(figure=fig7, id='main-figure7_cart')
        ]),
        dbc.Col([
            html.Div('Número de cuotas por periodicidad', className='titulosvis'),
            dcc.Graph(figure=fig8, id='main-figure8_cart')
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div('Cantidad de clientes por dia de pago-anual', className='titulosvis'),
            dcc.Graph(figure=fig9, id='main-figure9_cart')
        ])
    ])
])

input_list = [State('año_dropdown', 'value'), State('mes_dropdown', 'value'),
              State('region_dropdown', 'value'), State('sucursal_dropdown', 'value'),
              State('municipio_dropdown', 'value'), State('linea_dropdown', 'value'),
              State('estrato_dropdown', 'value'), State('profesion_dropdown', 'value'),
              Input('button_filter', 'n_clicks'),
              Input("open-offcanvas-cart", "n_clicks"),
              State("offcanvas-cart", "is_open")]

@callback([Output('main-figure1_cart', 'figure'), Output('main-figure2_cart', 'figure'),
          Output('main-figure3_cart', 'figure'), Output('main-figure4_cart', 'figure'),
          Output('main-figure5_cart', 'figure'), Output('main-figure6_cart', 'figure'),
          Output('main-figure7_cart', 'figure'), Output('main-figure8_cart', 'figure'),
          Output('main-figure9_cart', 'figure')],
          [State('año_dropdown', 'value'), State('mes_dropdown', 'value'), State('region_dropdown', 'value'),
          State('sucursal_dropdown', 'value'), State('municipio_dropdown', 'value'),
          State('linea_dropdown', 'value'), State('estrato_dropdown', 'value'),
          State('profesion_dropdown', 'value'),
          Input('button_filter', 'n_clicks')],
          prevent_initial_call=True)
def update_figs(año, mes, region, sucursal, municipio, linea, estrato, profesion, nclicks):
    filters = ['reg año', 'reg mes', 'region', 'sucursal real', 'municipio cliente', 'linea', 'estrato', 'profesion']
    filter_values = [año, mes, region, sucursal, municipio, linea, estrato, profesion]

    ## fig 1
    df = filter_df(df=cierre_cart, x=['dia_pago'], y='dia_pago', filters=filters, agg_function='count', to_frame='count', filter_values=filter_values)

    fig1 = px.bar(df, x='dia_pago', y='count', labels={'count':'Pagos', 'dia_pago':'Día del mes'}, color_discrete_sequence=['#34A527'], template='ggplot2')

    ## fig 2
    df = filter_df(df=cierre_cart, x=['dia_semana'], y='dia_semana', filters=filters, agg_function='count', to_frame='count', filter_values=filter_values)

    fig2 = px.bar(df, x='dia_semana', y='count', labels={'count':'Pagos', 'dia_semana':'Día de la semana'}, color_discrete_sequence=['#34A527'],
              category_orders={'dia_semana':['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}, template='ggplot2')
    
    ## fig 3
    df = filter_df(df=cierre_cart, x=['dia_pago'], y=['valor cuota'], filters=filters, agg_function='sum', filter_values=filter_values)

    fig3 = px.bar(df, x='dia_pago', y='valor cuota', labels={'valor cuota':'Total pagado', 'dia_pago':'Día del mes'}, color_discrete_sequence=['#34A527'], template='ggplot2')

    ## fig 4
    df = filter_df(df=cierre_cart, x=['region'], y=['valor cuota'], filters=filters, agg_function='sum', filter_values=filter_values)

    fig4 = px.bar(df, x='region', y='valor cuota', labels={'valor cuota':'Total pagado', 'region':'Región'}, color_discrete_sequence=['#34A527'], template='ggplot2')

    ## fig 5
    df = filter_df(df=cierre_cart, x=['sucursal real'], y=['valor cuota'], filters=filters, agg_function='sum', filter_values=filter_values)

    fig5 = px.bar(df, x='sucursal real', y='valor cuota', labels={'valor cuota':'Total pagado', 'sucursal real':'Sucursal'}, color_discrete_sequence=['#34A527'], template='ggplot2')
    
    ## fig 6
    df = filter_df(df=cierre_cart, x=['municipio cliente'], y=['valor cuota'], filters=filters, agg_function='sum', filter_values=filter_values)

    fig6 = px.bar(df, x='municipio cliente', y='valor cuota', color_discrete_sequence=['#34A527'], labels={'municipio cliente':'Municipio', 'valor cuota':'Total pagado'}, template='ggplot2')

    ## fig 7
    df = filter_df(df=cierre_cart, x=['periodicidad'], y=['valor cuota'], filters=filters, agg_function='sum', filter_values=filter_values)

    fig7 = px.bar(df, x='valor cuota', y='periodicidad', orientation='h', color_discrete_sequence=['#34A527'], labels={'peridiocidad':'Periodicidad', 'valor cuota':'Total pagado'}, template='ggplot2')

    ## fig 8
    df = filter_df(df=cierre_cart, x=['periodicidad'], y='valor cuota', filters=filters, agg_function='count', to_frame='count', filter_values=filter_values)

    fig8 = px.bar(df, x='count', y='periodicidad', orientation='h', color_discrete_sequence=['#34A527'], labels={'count':'Cantidad de pagos', 'periodicidad':'Periodicidad'}, template='ggplot2')

    ## fig 9
    df = cierre_cart[~cierre_cart['dia_pago'].isnull()]
    df = df[filter_idx(df, ['año_pago', 'mes_pago'], [año, mes])]
    df = filter_df(df=df, x=['fec ult.pago'], y='fec ult.pago', filters=filters[2:], agg_function='count', to_frame='count', filter_values=filter_values[2:])

    fig9 = px.bar(df, x="fec ult.pago", y="count",text_auto='.2s', labels={'count':'Número de pagos', 'dia_pago':'Día de pago' }, color_discrete_sequence=['#34A527'], template='ggplot2')
    fig9.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig9.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across")
    fig9.update_yaxes(showspikes=True, spikecolor="orange", spikethickness=2)
    
    return [fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9]

@callback(Output('offcanvas-cart', 'is_open'), input_list)
def toggle_offcanvas(año, mes, region, sucursal, municipio, linea, estrato, profesion, n2, n1, is_open):
    print('--------------')
    print(n1, n2, is_open)
    if n1:
        print(n1, n2, is_open)
        is_open = not is_open
    #filters = ['año_desembolso', 'nombre_mes', 'region', 'sucursal', 'municipio', 'linea', 'estrato', 'profesion']
    #filter_values = [año, mes, region, sucursal, municipio, linea, estrato, profesion]
    #if not any(filter_idx(colocacion, filters, filter_values)):
    #    is_open = True
    
    print(n1, n2, is_open)
    return is_open