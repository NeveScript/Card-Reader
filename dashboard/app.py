import requests
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash import Input, Output
import firebase_admin
from firebase_admin import credentials, db
from collections import defaultdict
import plotly.express as px
import dash_leaflet as dl
from dash_leaflet import Marker
import time

print("Booting...")
# Inicializando o aplicativo Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Carregando os dados da Firebasegit
cred = credentials.Certificate("./dashboard/key.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://observarioviolenciamulher-default-rtdb.firebaseio.com'})
ref = db.reference('dados')
data = ref.get()
# print(data)

markers = []

# ============================================================== #
# ==================== [ FUNÇÕES ]  ================================= #
# ============================================================== #

# Função para obter o endereço com base nas coordenadas
def get_location(x, y):
    api_key = "58bf9451648c478fbbc60a2f9d7c3f21"  
    url = f"https://api.opencagedata.com/geocode/v1/json?q={x}+{y}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if "results" in data:
        address = data["results"][0]["formatted"]
        return address
    else:
        return "Não foi possível obter informações de geolocalização para essas coordenadas"
    
def count_cases_by_location(data):
    location_counts = defaultdict(int)
    for key, value in data.items():

        try:
#            print(value["location"][0])
 #           print("location"[0] in value)

            x = value["location"][0]
            y = value["location"][1]
            location = get_location(x, y)
            #print("Edereço: " + location)
            #marker = Marker(position=(x, y), children=location)
            popup_text = f"Endereço: {location} | Data: {value['timestamp']} | Situação: {value['situacao']}"
            marker = Marker(position=(x, y), children=[
                location,  
                dl.Popup(children=popup_text)  
            ])
            markers.append(marker)
            location_counts[location] += 1

        except:
            print("Something is wrong")

    return location_counts

def count_cases_em_aberto(data):
    cases_em_aberto = 0

    for key, value in data.items():
        if(value['situacao'] == 'Em Aberto'):
            cases_em_aberto += 1
    
    return cases_em_aberto

# variáveis globais 
location_counts = count_cases_by_location(data)
locations = list(location_counts.keys())
case_counts = list(location_counts.values())
cases_em_aberto_counts = count_cases_em_aberto(data)


@app.callback(Output('map', 'children'), Input('interval-component', 'n_intervals'))
def update_map_markers(n_intervals):
    
    global markers
    markers = []
    new_data = ref.get()
    location_counts = count_cases_by_location(new_data)
    locations = list(location_counts.keys())
    case_counts = list(location_counts.values())
    cases_em_aberto_counts = count_cases_em_aberto(new_data)
    
    return markers


fig = px.pie(names=locations, values=case_counts, title='Total de Casos por Endereço')
map = dl.Map(
    children=[
        dl.TileLayer(),  
    ] + markers,  
    center=[56, 10],
    zoom=6,
    style={'height': '75vh'}
)
# ============================================================== #
# ===================== [ LAYOUT ]============================== #
# ============================================================== #
app.layout = dbc.Container([
        dbc.Row([
            dbc.Navbar(
            children=[
                dbc.NavbarBrand("OVM Dashboard", href="#", className="text-white"),
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("Home", href="#", className="text-white")),
                        dbc.NavItem(dbc.NavLink("Sobre", href="#", className="text-white")),
                    ],
                    navbar=True,
                ),
            ],
            color="primary", className="mb-2 p-2"
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H4("Denúncias em Aberto", className="card-title"),
                    html.P("Número de denúncias em aberto:", className="card-text"),
                    html.P(cases_em_aberto_counts, className="card-text"),
                ]),
                color="primary", inverse=True
            ),
            width=4
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H4("Denúncias Concluídas", className="card-title"),
                    html.P("Número de denúncias concluídas:", className="card-text"),
                    html.P("--", className="card-text"),
                ]),
                color="success", inverse=True
            ),
            width=4
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H4("Total de Denúncias", className="card-title"),
                    html.P("Número total de denúncias:", className="card-text"),
                    html.P(len(data), className="card-text"),
                ]),
                color="info", inverse=True
            ),
            width=4
        ),
    ]),
    html.Div([
        map
    ]),
    html.Div([
        dcc.Graph(
            figure=fig,  
            style={'height': '50vh'}  
        )

    ]),
], fluid=True, className="m-3")

if __name__ == '__main__':
    print("Running!")
    app.run_server(debug=True)
