import json
from datetime import datetime
import re
from bs4 import BeautifulSoup

def preprocess_events(events):

    # Appel de la fonction de nettoyage pour chaque événement et filtrage des événements invalides
    cleaned_events = []
    for result in events.get("results", []):
        cleaned_event = clean_event(result)
        if cleaned_event:
            cleaned_events.append(cleaned_event)

    # Sauvegarde des fichier nettoyés en json
    with open("data/events_clean.json", "w", encoding="utf-8") as f:
        json.dump(cleaned_events, f, ensure_ascii=False, indent=2)

    return cleaned_events

def clean_event(event):
    # Nettoyage des champs de l'événement
    if not event.get("longdescription_fr") or not event.get("title_fr"):
        return None  # Ignorer les événements sans description ou titre
  
    cleaned_event = {
        "text": f"L'évenement {event.get('title_fr')}. aura lieu dans la ville de {event.get('location_city')}. , durant les dates suivantes: {format_timings(event.get('timings'))}. Voici sa description: {clean_html(event.get('longdescription_fr', ''))}",
        "metadata": {
            "title": event.get("title_fr", ""),     
            "city": event.get("location_city", ""),   
            "timings": format_timings(event.get("timings", "[]")),  
            "region": event.get("location_region", ""), 
            "firstdate": event.get("firstdate_begin", ""),
            "location": event.get("location_name", ""),
    }
    }
    return cleaned_event

def clean_html(text):
    # Implémentation d'une fonction de nettoyage HTML avec BeautifulSoup
    soup = BeautifulSoup(text, "html.parser")
    clean = soup.get_text(separator=" ")
    clean = re.sub(r'\s+', ' ', clean)  # remplace tous les espaces/\n multiples par un seul espace
    return clean.strip()

def format_timings(timings_str):
    # Convertit les timings ISO en français lisible.
    timings = json.loads(timings_str)
    
    formatted = []
    for t in timings:
        begin = datetime.fromisoformat(t["begin"])
        end = datetime.fromisoformat(t["end"])
        formatted.append(
            f"le {begin.strftime('%d/%m/%Y')} de {begin.strftime('%Hh%M')} à {end.strftime('%Hh%M')}"
        )
    
    return " ; ".join(formatted)