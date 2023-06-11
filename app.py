import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Chargement des données

def load_data1(nrows):
    delay_data = pd.read_excel('https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx')
    return delay_data

def load_data2(nrows):
    pricing_data = pd.read_csv('https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv')
    return pricing_data

delay_data = load_data1(50)

pricing_data = load_data2(50)



st.title("Tableau de bord de gestion du produit")

# Part des revenus potentiellement affectée par la fonctionnalité
st.header("Part des revenus potentiellement affectée par la fonctionnalité")

# Calcul de la part des revenus affectée
total_revenue = pricing_data['rental_price_per_day'].sum()
revenue_affected = pricing_data[pricing_data['has_getaround_connect']]['rental_price_per_day'].sum()
revenue_percentage = (revenue_affected / total_revenue) * 100

# Affichage du résultat
 st.write("La part des revenus potentiellement affectée par la fonctionnalité est de", round(revenue_percentage, 2), "%")

# Nombre de locations affectées en fonction du seuil et de la portée
st.header("Nombre de locations affectées en fonction du seuil et de la portée")

# Sélection du seuil et de la portée
threshold = st.slider("Seuil", min_value=0, max_value=100, value=50)
scope = st.slider("Portée", min_value=0, max_value=100, value=50)

# Calcul du nombre de locations affectées
affected_locations = pricing_data[(pricing_data['mileage'] > threshold) & (pricing_data['engine_power'] > scope)].shape[0]

st.write("Le nombre de locations affectées est de", affected_locations)

st.header("Fréquence des retards des chauffeurs pour le prochain enregistrement")

# Calcul de la fréquence des retards
delay_frequency = delay_data[delay_data['delay_at_checkout_in_minutes'] < 0].shape[0] / delay_data.shape[0]

st.write("La fréquence des retards des chauffeurs pour le prochain enregistrement est de", round(delay_frequency, 2))

st.header("Impact des retards sur le prochain conducteur")

# Calcul de l'impact sur le prochain conducteur
average_delay = delay_data[delay_data['delay_at_checkout_in_minutes'] < 0]['delay_at_checkout_in_minutes'].mean()

st.write("L'impact des retards sur le prochain conducteur est en moyenne de", round(average_delay, 2), "minutes")

st.header("Résolution des cas problématiques en fonction du seuil et de la portée")

# Calcul des cas problématiques résolus
problematic_cases = pricing_data[(pricing_data['mileage'] > threshold) & (pricing_data['engine_power'] > scope)]['model_key'].nunique()

st.write("Le nombre de cas problématiques résolus est de", problematic_cases)

st.header("Évolution du nombre de locations affectées en fonction du seuil")

# Sélection des seuils
thresholds = np.linspace(0, 100, 11)

# Calcul du nombre de locations affectées pour chaque seuil
affected_counts = []
for threshold in thresholds:
    affected_locations = pricing_data[pricing_data['mileage'] > threshold].shape[0]
    affected_counts.append(affected_locations)

# Création du graphique
fig = go.Figure()
fig.add_trace(go.Scatter(x=thresholds, y=affected_counts, mode='lines', name='Nombre de locations affectées'))
fig.update_layout(title='Évolution du nombre de locations affectées en fonction du seuil',
                  xaxis_title='Seuil',
                  yaxis_title='Nombre de locations affectées')

# Affichage du graphique
st.plotly_chart(fig)

 
## Création d'un endpoint/predict

!pip install Flask mlflow

from flask import Flask, request, jsonify
import mlflow.pyfunc

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Récupérer les données d'entrée JSON
    data = request.get_json()
    inputs = data['input']
    
    # Charger le modèle MLflow
    model = mlflow.pyfunc.load_model('path/to/your/model')
    
    # Effectuer les prédictions à l'aide du modèle d'apprentissage automatique
    predictions = model.predict(inputs)
    
    # Construire la réponse JSON avec les prédictions
    response = {'prediction': predictions}
    
    # Renvoyer la réponse au client
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)




response = requests.post("https://my_app.herokuapp.com/predict", json={
    "input": [[7.0, 0.27, 0.36, 20.7, 0.045, 45.0, 170.0, 1.001, 3.0, 0.45, 8.8]]
})
print(response.json())

