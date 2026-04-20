from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

today = datetime.now().strftime("%d/%m/%Y")
template = os.getenv("PROMPT_SYSTEM").replace("{today}", today)

def build_rag_chain(vectorstore):
    # 1. Le retriever qui va chercher les k éléments les plus similaires dans l'index
    retriever = vectorstore.as_retriever(search_kwargs={"k": 20})
    
    # 2. Le modèle Mistral sélectionné
    llm = ChatMistralAI(
        model=os.getenv("MISTRAL_MODEL"),
        api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0 # réponse déterministes
    )
    
    # 3. Le prompt système définit dans le .env
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
     # Assemblage de la chaîne avec les 3 éléments
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain