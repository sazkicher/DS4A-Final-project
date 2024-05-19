# Load your libraries
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
from dash_labs.plugins.pages import register_page
import plotly.express as px
import pandas as pd
import json
import pathlib

register_page(__name__, path='/client_seg')


# Layout

layout = html.H1('Client Segmentation')






