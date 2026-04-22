import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

# URL de l'API OPENDATASOFT
API_URL = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/evenements-publics-openagenda/records/"

# Récupération de la région à filtrer depuis les variables d'environnement
FILTER_REGION = os.getenv("FILTER_REGION", "Occitanie")

# Création dynamique de la date de filtrage pour les événements de l'année passée
today = datetime.now()
one_year_ago = today - timedelta(days=365)
date_str = one_year_ago.strftime("%Y-%m-%d")


"""
Fonction permettant de requêter l'API avec une logique de pagination
"""
def fetch_events():
    all_results = []
    offset = 0
    limit = 100
    max_events = 15000  # Limite maximale pour éviter de récupérer trop d'événements

    while True:

        params = { # paramètres donnés à la requête sur l'API
        "lang": "fr",
        "limit": limit,
        "offset": offset,
        "where": f"location_region='{FILTER_REGION}' AND firstdate_begin > '{date_str}'"
    }
        
        
        response = requests.get(API_URL, params=params) # on envoie la requête avec les paramètres de pagination et de filtrage
        data = response.json() # on parse la réponse JSON pour extraire les résultats
        results = data.get("results", []) # on récupère les résultats de la page courante, ou une liste vide si la clé "results" n'existe pas
        
        if not results:  # plus rien dans results → on arrête
            print(f"{len(all_results)} résultats récupérés, arrêt de la récupération.")
            break
        
        all_results.extend(results) # on ajoute les résultats à la liste globale

        if len(all_results) >= max_events: # on a atteint la limite → on arrête
            print(f"Limite de {max_events} événements atteinte, arrêt de la récupération.")
            break   

        offset += limit  # on passe à la page suivante

    return {"results": all_results}

