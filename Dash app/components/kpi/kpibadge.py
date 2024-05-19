from dash import html 


import dash_bootstrap_components as dbc

class kpibadge:
    def __init__(self,kpi,label):
        self.kpi = kpi
        self.label = label

    def display(self):
        layout = html.Div(
            [
             html.Div(self.label,className='h6 d-flex justify-content-center'),
             html.H2(self.kpi,className='d-flex justify-content-center'),
            ], className='m-2'
        )
        return layout