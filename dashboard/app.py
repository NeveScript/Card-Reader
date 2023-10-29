from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db

# ============================= #
# ======== FUNCTIONS ========== #
# ============================= #

def create_table(data):

    table_rows = []

    for key, values in data.items():

        situacao_class = 'em_aberto' if values["situacao"] == 'Em Aberto' else 'concluido'
    
        table_row = html.Tr([
            html.Td(key),
            html.Td(values["situacao"], className=situacao_class),
            html.Td(values["timestamp"]),
            html.Td(values["tipo"]),
            html.Td(html.Button('Detalhes', className='btn-primary'))
        ])
        table_rows.append(table_row)
    
    table = html.Table([
        # Cabeçalho da tabela
        html.Thead(html.Tr([
            html.Th("ID"),
            html.Th("Situação"),
            html.Th("Data"),
            html.Th("Tipo"),
            html.Th("Ação")
        ])),
        # Corpo da tabela
        html.Tbody(table_rows)
    ], className="table table-responsive-md table-striped")
    
    return table

cred = credentials.Certificate("./dashboard/key.json")
firebase_admin.initialize_app(cred, {    'databaseURL': 'https://observarioviolenciamulher-default-rtdb.firebaseio.com'})

ref = db.reference('dados')
data = ref.get()

create_table(data)

# Criar a aplicação Dash
app = Dash(__name__)

# Layout da aplicação
app.layout = html.Div([
    html.H1("Registro de Denúncias", className="text-primary text-center"),
    html.Link(
        rel='stylesheet',
        href='https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css'
    ),
    html.Link(
        rel='stylesheet',
        href='./dashboard/assets/css'
    ),
    create_table(data)
])

if __name__ == '__main__':
    app.run_server(debug=True)