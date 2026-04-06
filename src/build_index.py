from data_ingestion import fetch_events
from preprocessing import preprocess_events
from vectorization import split_documents, build_vectorstore
import json
import os

# On vérifie la présence des données nettoyés dans le répertoire data
if not os.path.exists("data/events_clean.json"):

    # Ingestion des doonnées depuis l'API opendatasoft
    events = fetch_events()

    # Prétraitement des données pour nettoyage et structuration
    cleaned = preprocess_events(events)
    
else: #Si les données sont deja présentes on les charge
    with open("data/events_clean.json", "r", encoding="utf-8") as f:
        cleaned=json.load(f)


# Découpe des textes en chunks
documents = split_documents(cleaned)

# Véctorisation des chunks et création d'index
vectorstore=build_vectorstore(documents)

print("\n\nIndex construit ou déja présent.")