# Puls-Events RAG POC

Proof of Concept d'un chatbot intelligent basé sur un système **RAG (Retrieval-Augmented Generation)** pour la société **Puls-Events**. Le chatbot répond à des questions sur les événements culturels en **Île-de-France** en s'appuyant sur des données issues d'**Open Agenda** via OpenDataSoft.

---

## Objectifs

- Démontrer la faisabilité technique d'un chatbot événementiel basé sur RAG
- Permettre aux utilisateurs d'interroger le catalogue d'événements en langage naturel
- Fournir des réponses ancrées dans les données réelles, sans hallucinations
- Servir de base pour évaluer un déploiement à plus grande échelle

---

## Prérequis

- Python 3.13+
- Poetry
- Une clé API Mistral AI → [console.mistral.ai](https://console.mistral.ai/)

---

## Installation

**1. Cloner le repository**

```bash
git clone https://github.com/nigeldellamore66-crypto/OPC-RAG-System
cd puls_events_rag
```

**2. Installer les dépendances**

```bash
# Avec Poetry (recommandé)
poetry install

# Avec pip
pip install -r requirements.txt
```

**3. Configurer les variables d'environnement**

```bash
cp .env.example .env
# Éditer .env avec vos clés API
```

---

## Configuration `.env`

```env
MISTRAL_API_KEY=votre_clé_mistral
MISTRAL_MODEL=mistral-small-latest
FILTER_REGION=Île-de-France
PROMPT_SYSTEM="..."
```

---

## Utilisation

**1. Construire l'index vectoriel** *(à faire une seule fois)*

```bash
poetry run python src/build_index.py
```

**2. Lancer l'interface chat**

```bash
poetry run streamlit run src/app.py
```

---

## Structure du projet

```
puls_events_rag/
├── src/
│   ├── data_ingestion.py     # Récupération des données OpenDataSoft
│   ├── preprocessing.py      # Nettoyage et filtrage des événements
│   ├── vectorization.py      # Création de l'index FAISS
│   ├── rag_chain.py          # Chaîne RAG LangChain + Mistral
│   ├── build_index.py        # Script de construction de l'index
│   ├── app.py                # Interface Streamlit
│   ├── create_dataset_rag.py # Script qui enrichit le dataset d'évaluation avec le contexte et la réponse du LLM
│   ├── evaluate_ragas.py     # Script d'évaluation du dataset qui utilise RAGAS
│   └── .env.example          # Template des variables d'environnement
│
├── data/
│   ├── events_clean.json    # Données nettoyées (généré automatiquement)
│   └── faiss_index/         # Index vectoriel (généré automatiquement)
├── tests/
│   └── test_data.py         # Tests unitaires
├── .gitignore               # Fichiers exclus du repo
├── requirements.txt         # Dépendances Python
└── README.md
```

---

## Tests

```bash
poetry run pytest tests/ -v
```

---

## Limitations connues

- L'API OpenDataSoft limite les résultats à **10 000 événements**
- Des **hallucinations occasionnelles** ont été observées malgré `temperature=0`
- La recherche sémantique **ne filtre pas nativement par date** (filtrage Python en amont implémenté)

---

## Stack technique

| Outil | Rôle |
|-------|------|
| LangChain | Orchestration du pipeline RAG |
| Mistral AI | Embeddings + génération de réponses |
| FAISS | Base vectorielle |
| OpenDataSoft | Source de données événementielles |
| Streamlit | Interface utilisateur |
| BeautifulSoup | Nettoyage du HTML |
| pytest | Tests unitaires |
| RAGAS | Evaluation du modèle RAG |
