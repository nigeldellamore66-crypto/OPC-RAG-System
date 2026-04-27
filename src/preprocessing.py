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
    if not event.get("longdescription_fr") or not event.get("title_fr"):
        return None

    # Parse les timings une seule fois
    timings_info = parse_timings(event.get("timings", "[]"))
    
    # Génère un résumé temporel adapté au nombre d'occurrences
    timings_summary = summarize_timings(timings_info)

    cleaned_event = {
        "text": (
            f"L'événement {event.get('title_fr')} "
            f"a lieu au {event.get('location_name')} "
            f"dans la ville de {event.get('location_city')}. "
            f"{timings_summary}. "
            f"Description : {clean_html(event.get('longdescription_fr', ''))}"
        ),
        "metadata": {
            "title": event.get("title_fr", ""),
            "city": event.get("location_city", ""),
            "region": event.get("location_region", ""),
            "location": event.get("location_name", ""),
            # Métadonnées temporelles compactes et exploitables
            "date_debut": timings_info["date_debut"],
            "date_fin": timings_info["date_fin"],
            "nb_occurrences": timings_info["nb_occurrences"],
            "firstdate": event.get("firstdate_begin", ""),
        }
    }
    return cleaned_event


def parse_timings(timings_str):
    #Extrait les infos temporelles structurées des timings.
    if not timings_str or timings_str == "[]":
        return {
            "date_debut": "",
            "date_fin": "",
            "nb_occurrences": 0,
            "occurrences": [],
        }
    
    timings = json.loads(timings_str)
    if not timings:
        return {
            "date_debut": "",
            "date_fin": "",
            "nb_occurrences": 0,
            "occurrences": [],
        }
    
    occurrences = []
    for t in timings:
        begin = datetime.fromisoformat(t["begin"])
        end = datetime.fromisoformat(t["end"])
        occurrences.append({"begin": begin, "end": end})
    
    return {
        "date_debut": min(o["begin"] for o in occurrences).strftime("%Y-%m-%d"),
        "date_fin": max(o["end"] for o in occurrences).strftime("%Y-%m-%d"),
        "nb_occurrences": len(occurrences),
        "occurrences": occurrences,
    }


def summarize_timings(timings_info):
    #Génère un texte naturel décrivant les dates, adapté au nombre d'occurrences.
    nb = timings_info["nb_occurrences"]
    
    if nb == 0:
        return "Dates non précisées"
    
    if nb == 1:
        # Événement unique : on donne la date complète avec horaires
        o = timings_info["occurrences"][0]
        return (
            f"Date : le {o['begin'].strftime('%d/%m/%Y')} "
            f"de {o['begin'].strftime('%Hh%M')} à {o['end'].strftime('%Hh%M')}"
        )
    
    if nb <= 10:
        # Peu d'occurrences : on les liste toutes
        formatted = [
            f"le {o['begin'].strftime('%d/%m/%Y')} "
            f"de {o['begin'].strftime('%Hh%M')} à {o['end'].strftime('%Hh%M')}"
            for o in timings_info["occurrences"]
        ]
        return f"Dates : {' ; '.join(formatted)}"
    
    # Beaucoup d'occurrences : on résume sur la période
    date_debut = datetime.strptime(timings_info["date_debut"], "%Y-%m-%d")
    date_fin = datetime.strptime(timings_info["date_fin"], "%Y-%m-%d")
    return (
        f"Événement récurrent : {nb} occurrences "
        f"du {date_debut.strftime('%d/%m/%Y')} "
        f"au {date_fin.strftime('%d/%m/%Y')}"
    )


def clean_html(text):
    # Implémentation d'une fonction de nettoyage HTML avec BeautifulSoup
    soup = BeautifulSoup(text, "html.parser")
    clean = soup.get_text(separator=" ")
    clean = re.sub(r'\s+', ' ', clean)  # remplace tous les espaces/\n multiples par un seul espace
    return clean.strip()