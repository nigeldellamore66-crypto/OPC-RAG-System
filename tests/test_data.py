import json
import pytest
from datetime import datetime, timedelta

# Chargement des données
with open("data/events_clean.json", "r", encoding="utf-8") as f:
    events = json.load(f)

# Création dynamique de la date de filtrage pour les événements de l'année passée
today = datetime.now()
one_year_ago = today - timedelta(days=365)
date_str = one_year_ago.strftime("%Y-%m-%d")

def test_geographic_filter():
    # Vérifie que tous les événements sont en Île-de-France
    for event in events:
        assert event["metadata"]["region"] == "Île-de-France"

def test_date_filter():
    # Vérifie que toutes les dates sont >= aujourd'hui - 365 jours
    for event in events:
        date_event=event["metadata"]["firstdate"][:10]
        assert date_event >= date_str

def test_text_not_empty():
    # Vérifie que tous les événements ont un texte non vide
    for event in events:
        assert event["text"] != ""
        assert len(event["text"]) > 10

def test_required_metadata_fields():
    # Vérifie que tous les champs obligatoires sont présents
    for event in events:
        assert "title" in event["metadata"]
        assert "city" in event["metadata"]
        assert "firstdate" in event["metadata"]

def test_no_html_in_text():
    # Vérifie qu'il n'y a plus de balises HTML dans le texte
    for event in events:
        assert "<p>" not in event["text"]
        assert "<br>" not in event["text"]