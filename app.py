from dash import Dash, html, dcc, Input, Output, State, callback
import datetime
import logging
import os
import plotly.graph_objects as go

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USERS_DB = {
    'user1':  {'password': 'pass1',    'balance': 5000,  'transactions': []},
    'user2':  {'password': 'pass2',    'balance': 3000,  'transactions': []},
    'admin':  {'password': 'admin123', 'balance': 10000, 'transactions': []},
}

TEAL = '#00A6A6'
HIDDEN = {'display': 'none'}
NAVBAR = {
    'backgroundColor': TEAL, 'padding': '14px 24px', 'color': 'white',
    'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center',
}
CONTAINER = {'maxWidth': '960px', 'margin': '0 auto', 'padding': '20px', 'fontFamily': 'Segoe UI, Arial, sans-serif'}
LOGIN_BOX = {
    'maxWidth': '400px', 'margin': '60px auto', 'padding': '40px',
    'border': '1px solid #e0e0e0', 'borderRadius': '12px',
    'boxShadow': '0 4px 16px rgba(0,0,0,.08)', 'textAlign': 'center', 'backgroundColor': '#fff',
}
INPUT_S = {
    'width': '100%', 'padding': '10px 12px', 'margin': '8px 0',
    'border': '1px solid #ccc', 'borderRadius': '6px',
    'boxSizing': 'border-box', 'fontSize': '14px',
}
BTN = {
    'width': '100%', 'padding': '10px', 'margin': '10px 0 4px',
    'backgroundColor': TEAL, 'color': 'white', 'border': 'none',
    'borderRadius': '6px', 'cursor': 'pointer', 'fontSize': '14px', 'fontWeight': '600',
}
CARD = {
    'backgroundColor': '#f9f9f9', 'padding': '20px',
    'borderRadius': '10px', 'marginBottom': '16px', 'border': '1px solid #eee',
}

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    dcc.Store(id='user-store', storage_type='session'),

    html.Div(id='navbar', style=HIDDEN, children=[
        html.H1("💳 NED'S Wallet", style={'margin': 0, 'fontSize': '22px'}),
        html.Button('Logout', id='logout-btn', style={
            'backgroundColor': '#FF6B6B', 'padding': '7px 18px',
            'border': 'none', 'color': 'white', 'borderRadius': '6px', 'cursor': 'pointer',
        }),
    ]),

    html.Div(style=CONTAINER, children=[
        html.Div(id='login-section', children=[
            html.Div(style=LOGIN_BOX, children=[
                html.Div('💳', style={'fontSize': '40px', 'marginBottom': '8px'}),
                html.H2("NED'S Wallet", style={'color'
