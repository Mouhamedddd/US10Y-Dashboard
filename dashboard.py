import dash
from dash import dcc, html, dash_table
import pandas as pd
import plotly.express as px
import datetime
from datetime import timedelta
from flask import Flask, render_template
from dash.dependencies import Input, Output

def load_data():
    # Charger les données du fichier CSV
    csv_file = "yield.csv" 
    df = pd.read_csv(csv_file, names=["Timestamp", "Yield"])

    # Convertir le champ Timestamp en datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])+timedelta(hours=1)

    # Supprimer le signe '%' et convertir la colonne Yield en numérique, remplacer 'null' et autres non numériques par NaN
    df['Yield'] = df['Yield'].str.replace('%', '', regex=False)  # Enlever le '%' sans erreurs
    df['Yield'] = pd.to_numeric(df['Yield'], errors='coerce')     # Convertir en numérique, remplacer les erreurs par NaN



    return df

# Fonction pour obtenir la valeur de Yield à 20h aujourd'hui
def get_yield_at_20h(df):
    df_20h = df[df['Timestamp'].dt.hour == 20]
    return df_20h.iloc[-1]['Yield'] if not df_20h.empty else None

# Fonction pour obtenir la valeur de Yield à 20h du jour précédent
def get_yield_at_20h_previous_day(df):
    df_20h = df[df['Timestamp'].dt.hour == 20]
    return df_20h.iloc[-2]['Yield'] if len(df_20h) >= 2 else None

# Fonction pour calculer la volatilité, la moyenne, le max et le min sur 24h
def calculate_stats(df):
    df_24h = df[df['Timestamp'] > (df['Timestamp'].max() - pd.Timedelta(hours=24))]
    return df_24h['Yield'].std(), df_24h['Yield'].mean(), df_24h['Yield'].max(), df_24h['Yield'].min()


# Fonction pour récupérer la dernière valeur de Yield
def get_latest_yield():
     # Charger les données du fichier CSV
    csv_file = "yield.csv"
    dfbis = pd.read_csv(csv_file, names=["Timestamp", "Yield"])

    latest_yield = dfbis.iloc[-1]['Yield']  # Dernière valeur de Yield
    return latest_yield

# Initialiser l'application Flask
server = Flask(__name__)

#Initialisation dash  et attache a Dash
app=dash.Dash(__name__,server=server, routes_pathname_prefix="/dash/")

#Mise en page du Dashboard
app.layout= html.Div([

	#Last Yield

	html.Div(
        	children=[
            		html.H3(id="latest-yield", style={'color': 'red','fontSize':'75px'})
        	],
        	style={'textAlign': 'center'}
    	),

	#Graphique
	dcc.Graph(id="yield-graph"),

	#Intervalle de mise a jour toutes les 5 minutes
	dcc.Interval(id="interval-component",interval=1000*60*5, n_intervals=0),

	# Indicateurs ligne par ligne
    html.Div(children=[
	html.Br(), html.Br(),
        html.H4("8pm yield : ", style={"display": "inline"}), html.Span(id="price-20h-value"),
        html.Br(),
        html.H4("Yesterday 8pm yield : ", style={"display": "inline"}), html.Span(id="price-20h-prev-day"),
        html.Br(), html.Br(),
        
        html.H4("Mean : ", style={"display": "inline"}), html.Span(id="avg-between-values"),
        html.Br(),
        html.H4("Volatility : ", style={"display": "inline"}), html.Span(id="volatility-value"),
        html.Br(), html.Br(),
        
        html.H4("Max : ", style={"display": "inline"}), html.Span(id="max-value"),
        html.Br(),
        html.H4("Min : ", style={"display": "inline"}), html.Span(id="min-value"),
    ], style={'textAlign': 'center', 'fontSize': '20px','color':'WHITE'}),
])


#Callback de mise a jour

@app.callback(
    dash.Output("latest-yield", "children"),
    [dash.Input("interval-component", "n_intervals")]
)
def update_latest_yield(n):
    latest_yield = get_latest_yield()
    print(f"Latest Yield: {latest_yield}")  # Debugging in console
    return f"{latest_yield}" if latest_yield is not None else "N/A"



@app.callback(
    dash.Output("yield-graph","figure"),
    dash.Input("interval-component","n_intervals")
)
def update_graph(n):
    df=load_data()
    return px.line(df, x="Timestamp",y="Yield")


@app.callback(
    [
        dash.Output("price-20h-value", "children"),
        dash.Output("price-20h-prev-day", "children"),
        dash.Output("avg-between-values", "children"),
        dash.Output("volatility-value", "children"),
        dash.Output("max-value", "children"),
        dash.Output("min-value", "children")
    ],
    [dash.Input("interval-component", "n_intervals")]
)
def update_indicators(n):
    df = load_data()

    print("\n--- Mise à jour des indicateurs ---")
    print(df.tail(10))  # Vérifier les dernières valeurs du CSV

    # Récupération des indicateurs
    price_20h = get_yield_at_20h(df)
    price_20h_previous_day = get_yield_at_20h_previous_day(df)
    volatility, mean_value, max_value, min_value = calculate_stats(df)

    # Vérification pour éviter les erreurs d'affichage
    price_20h_str = f"{price_20h} %" if price_20h is not None else "N/A"
    price_20h_prev_str = f"{price_20h_previous_day} %" if price_20h_previous_day is not None else "N/A"

    # Moyenne entre les valeurs de 20h
    avg_between_values = (
        f"{(price_20h + price_20h_previous_day) / 2:.2f} %" 
        if price_20h is not None and price_20h_previous_day is not None 
        else "N/A"
    )

    return (
        price_20h_str,
        price_20h_prev_str,
        avg_between_values,
        f"{volatility:.4f} %" if volatility is not None else "N/A",
        f"{max_value} %" if max_value is not None else "N/A",
        f"{min_value} %" if min_value is not None else "N/A"
    )


#Route pour la page html
@server.route('/')
def home():
	return render_template('index.html')


# Lancer l'application
if __name__ == "__main__":
    server.run(debug=True, host="0.0.0.0", port=8050)
