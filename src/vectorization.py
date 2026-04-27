from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv

load_dotenv()

# On appelle le recursive text splitter de langchain pour créer des chunks à partir de nos documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50
)

# On appelle le modèle Embeddings de MistralAI qui permettra de vectoriser nos chunks
embeddings = MistralAIEmbeddings(
    model="mistral-embed",
    api_key=os.getenv("MISTRAL_API_KEY")
)

def split_documents(events):
# Fonction permettant de découper les documents json issus des requêtes sur l'API en chunks en y ajoutant les metadatas correspondantes
    documents = []
    for event in events:
        text = event["text"]
        metadata = {
            "title": event["metadata"]["title"],
            "city": event["metadata"]["city"],
            "region": event["metadata"]["region"],
            "location": event["metadata"]["location"],
            "firstdate": event["metadata"]["firstdate"],
            "date_debut": event["metadata"]["date_debut"],
            "date_fin": event["metadata"]["date_fin"],
            "nb_occurrences": event["metadata"]["nb_occurrences"],
        }
        chunks = text_splitter.create_documents([text], metadatas=[metadata])
        documents.extend(chunks)

    return documents

def build_vectorstore(documents=None):
# Fonction permettant de créer l'index de vectorisation avec la liste de documents splités en entrée
    if not os.path.exists("data/faiss_index"): # si l'index n'existe pas on le créer puis on le sauvegarde
        if documents is None:
            raise ValueError("Aucun index existant et aucun document fourni !")
        vectorstore = FAISS.from_documents(documents, embeddings)
        vectorstore.save_local("data/faiss_index")
    else:  # si l'index existe on le charge
        vectorstore = FAISS.load_local("data/faiss_index", embeddings, allow_dangerous_deserialization=True)

    return vectorstore