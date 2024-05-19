from re import template
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def line_plot_range(df, title=None, xtitle=None, ytitle=None):
    fig = go.Figure([
        go.Scatter(
            name='Tasa promedio',
            x=df['mes_desembolso'],
            y=df['tasa promedio'],
            mode='lines',
            line=dict(color='#34A527'),
        ),
        go.Scatter(
            name='Tasa al Q3/75%',
            x=df['mes_desembolso'],
            y=df['Q3/75%'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Tasa al Q1/25%',
            x=df['mes_desembolso'],
            y=df['Q1/25%'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False
        ),
        go.Scatter(
            name='Tasa máxima',
            x=df['mes_desembolso'],
            y=df['tasa máxima'],
            mode='lines',
            line=dict(color='red')
        ),
        go.Scatter(
            name='Tasa mínima',
            x=df['mes_desembolso'],
            y=df['tasa mínima'],
            mode='lines',
            line=dict(color='#FFA600')
    )
    ],)
    fig.update_layout(
        yaxis_title=ytitle,
        xaxis_title=xtitle,
        hovermode="x",
        template='ggplot2'
    )

    return fig

def line_plot_two_axis(df, title=None, xtitle=None, y1_title=None, y2_title=None):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Add traces
    fig.add_trace(
        go.Scatter(
            name='Promedio($)',
            x=df['mes_desembolso'],
            y=df['promedio (miles_$)'],
            mode='lines',
            line=dict(color='#3CBF2D'),
        ), secondary_y=False)
        
    fig.add_trace(
        go.Scatter(
            name='Q3/75%($)',
            x=df['mes_desembolso'],
            y=df['Q3/75%'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False,
        ), secondary_y=False)

    fig.add_trace(
        go.Scatter(
            name='Q1/25%($)',
            x=df['mes_desembolso'],
            y=df['Q1/25%'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False,
        ), secondary_y=False)
        
        
    fig.add_trace(    
        go.Scatter(
            name='Máximo($)',
            x=df['mes_desembolso'],
            y=df['máximo'],
            mode='lines',
            line=dict(color='red'),

        ), secondary_y=True)

    fig.add_trace(
        go.Scatter(
            name='Mínimo($)',
            x=df['mes_desembolso'],
            y=df['mínimo'],
            mode='lines',
            line=dict(color='#FFA600'),

        ), secondary_y=False)

    fig.update_layout(
        title=title,
        xaxis_title=xtitle,
        hovermode="x",
        template='ggplot2'
    )

    fig.update_yaxes(title_text=y1_title, secondary_y=False)
    fig.update_yaxes(title_text=y2_title, secondary_y=True)
    
    return fig

def line_plot_two_axis_cart(df, x_data, y1_data, y2_data):
    fig9 = make_subplots(specs=[[{"secondary_y": True}]])


    fig9.add_trace(
        go.Scatter(
            name='Total pagado',
            x=df[x_data],
            y=df[y1_data]/1000000,
            mode='lines',
            line=dict(color='#34A527'),
        ), secondary_y=False)
        


    fig9.add_trace(    
        go.Scatter(
            name='Numero de pagos',
            x=df[x_data],
            y=df[y2_data],
            mode='lines',
            line=dict(color='#FFA600'),

        ), secondary_y=True)


    fig9.update_layout(
        hovermode="x",
        template='ggplot2'
    )



    fig9.update_yaxes(title_text="Total pagado (millones de pesos)", secondary_y=False)
    fig9.update_yaxes(title_text="Numero de pagos", secondary_y=True)

    return fig9