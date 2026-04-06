import streamlit as st
import os
from rag_chain import build_rag_chain
from vectorization import build_vectorstore

def generer_reponse(prompt):
    try:
        # Récupère les 3 derniers messages
        historique = st.session_state.messages[-3:]
        
        # Formate l'historique en texte
        historique_str = ""
        for msg in historique:
            role = "Utilisateur" if msg["role"] == "user" else "Assistant"
            historique_str += f"{role}: {msg['content']}\n"
        
        # Construit la question enrichie avec l'historique
        prompt_with_history = f"Historique:\n{historique_str}\nQuestion: {prompt}"
        
        response = st.session_state.chain.invoke(prompt_with_history)
        return response
    except Exception as e:
        st.error(f"Erreur lors de la génération de la réponse: {e}")
        return "Je suis désolé, j'ai rencontré un problème. Veuillez réessayer."


if "chain" not in st.session_state:
    vectorstore = build_vectorstore()
    st.session_state.chain = build_rag_chain(vectorstore)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour, je suis l'assistant virtuel de Puls-Events. Comment puis-je vous aider aujourd'hui?"}]

st.title("Assistant Virtuel de Puls-Events")
# Affichage des messages précédents
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

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