"""
Évaluation du RAG avec Ragas.
Charge le dataset enrichi (questions + answers + contexts + ground_truth)
et calcule les métriques d'évaluation.
"""
import os
import time
from pathlib import Path
from datasets import load_from_disk
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    answer_correctness,
)
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.run_config import RunConfig
from dotenv import load_dotenv

load_dotenv()

# Chemin des fichiers
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATASET_PATH = DATA_DIR / "dataset_eval_enriched"
RESULTS_PATH = DATA_DIR / "ragas_results.csv"


def main():
    # Chargement du dataset enrichi au format arrow
    print(f"Chargement du dataset depuis {DATASET_PATH}...")
    dataset = load_from_disk(str(DATASET_PATH))
    print(f"  → {len(dataset)} exemples chargés")
    print(f"  → Colonnes : {dataset.column_names}")

    # Chargement de Mistral comme LLM juge
    print("\nConfiguration du LLM juge...")
    judge_llm = LangchainLLMWrapper(
        ChatMistralAI(
            model="mistral-large-latest",
            api_key=os.getenv("MISTRAL_API_KEY"),
            temperature=0,
        )
    )

    # Chargement du modele embeddings Mistral
    judge_embeddings = LangchainEmbeddingsWrapper(
        MistralAIEmbeddings(
            model="mistral-embed",
            api_key=os.getenv("MISTRAL_API_KEY"),
        )
    )

    # Choisir les métriques ragas
    metrics = [
        faithfulness,           # La réponse est-elle fidèle aux contextes ?
        answer_relevancy,       # La réponse répond-elle bien à la question ?
        context_precision,      # Les contextes récupérés sont-ils pertinents ?
        context_recall,         # Les contextes contiennent-ils l'info attendue ?
        answer_correctness,     # La réponse correspond-elle au ground_truth ?
    ]
    print(f"\nMétriques activées : {[m.name for m in metrics]}")

    # Rate limiting de Mistral
    # max_workers=1 : pas d'appels parallèles
    # max_retries=10 : retry automatique en cas d'erreurs
    run_config = RunConfig(
        max_workers=1,
        max_retries=10,
        max_wait=60,
        timeout=200,
    )

    # Evaluation du Dataset avec RAGAS
    print("\nLancement de l'évaluation Ragas...")
    start = time.time()

    # Evaluation RAGAS avec les données et paramètres choisis
    result = evaluate(
        dataset=dataset,
        metrics=metrics,
        llm=judge_llm,
        embeddings=judge_embeddings,
        run_config=run_config,
        raise_exceptions=False,  # ne pas crasher si une métrique plante sur un exemple
    )

    duration = time.time() - start
    print(f"\nÉvaluation terminée en {duration:.0f} secondes.")

    # Affiche le résultat global
    print("\n=== Scores moyens ===")
    print(result)

    # Sauvegarde des resultats détaillés
    df_results = result.to_pandas()
    df_results.to_csv(RESULTS_PATH, index=False, encoding="utf-8")
    print(f"\nRésultats détaillés sauvegardés dans {RESULTS_PATH}")

if __name__ == "__main__":
    main()