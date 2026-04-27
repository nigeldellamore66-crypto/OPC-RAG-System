import pandas as pd
import time
from datasets import Dataset
from rag_chain import build_rag_chain
from vectorization import build_vectorstore

#Chargement du Dataset question/réponses attendues
df = pd.read_csv("data/dataset_eval.csv", encoding="cp1252")

# Cnargement du modele RAG
vectorstore = build_vectorstore()
rag_chain = build_rag_chain(vectorstore)

questions = []
answers = []
contexts = []
ground_truths = []

for i, row in df.iterrows():
    question = row["Questions"] # Récupération de la question dans le document
    print(f"[{i+1}/{len(df)}] {question[:60]}...")
    
    try:
        result = rag_chain.invoke(question) #Génération de la réponse
        answer = result["answer"]
        ctx = [doc.page_content for doc in result["context"]] # Récupération du contexte
    except Exception as e:
        print(f"  Erreur : {e}")
        answer = "ERREUR"
        ctx = []
    
    # Assemblage du dataset enrichi avec contexte et réponses du LLM
    questions.append(question)
    answers.append(answer)
    contexts.append(ctx)
    ground_truths.append(row["Réponses références"])
    
    time.sleep(15)  # rate limit

dataset = Dataset.from_dict({
    "question": questions,
    "answer": answers,
    "contexts": contexts,
    "ground_truth": ground_truths,
})
# Sauvegarde au format arrow pour évaluation future par RAGAS
dataset.save_to_disk("data/dataset_eval_enriched")
print(f"\n{len(dataset)} exemples enrichis sauvegardés.")