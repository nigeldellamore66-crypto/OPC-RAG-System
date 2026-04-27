import streamlit as st
import os
from rag_chain import build_rag_chain
from vectorization import build_vectorstore


# Fonction permettant de générer les réponses en appellant la chaîne définie dans rag_chain.py avec le prompt utilisateur en entrée

def generer_reponse(prompt):
    try:
        
        result = st.session_state.chain.invoke(prompt)
        reponse = result["answer"]

        return reponse
    except Exception as e:
        st.error(f"Erreur lors de la génération de la réponse: {e}")
        return "Je suis désolé, j'ai rencontré un problème. Veuillez réessayer."

# Chargement de la base de vectorisation et initialisation de la chaîne 
if "chain" not in st.session_state:
    vectorstore = build_vectorstore()
    st.session_state.chain = build_rag_chain(vectorstore)

# Initialisation du chat avec un message de bienvenue
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour, je suis l'assistant virtuel de Puls-Events. Comment puis-je vous aider aujourd'hui?"}]

st.title("Assistant Virtuel de Puls-Events")
# Affichage des messages précédents
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Construction du dialogue avec un champ d'écriture pour l'utilisateur dont l'entrée est envoyée comme prompt pour générer des réponses
if prompt := st.chat_input("Comment puis-je vous aider?"):
    # Ajout du message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Ajout de la réponse
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.text("En train de réfléchir...")
        response = generer_reponse(prompt)
        message_placeholder.write(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})