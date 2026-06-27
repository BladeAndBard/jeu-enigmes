import streamlit as st
import anthropic
import os

# --- Connexion à Claude ---
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def appeler_claude(historique, system):
    reponse = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=system,
        messages=historique
    )
    return reponse.content[0].text

# --- Initialisation ---
system = "Tu es le maître du jeu d'un jeu d'énigmes. Tu poses des énigmes en français, tu évalues les réponses avec bienveillance et tu donnes des indices si le joueur est bloqué."

if "historique" not in st.session_state:
    st.session_state.historique = []
    st.session_state.historique.append({"role": "user", "content": "Pose-moi une énigme."})
    premiere_enigme = appeler_claude(st.session_state.historique, system)
    st.session_state.historique.append({"role": "assistant", "content": premiere_enigme})

# --- Interface ---
st.title("🎮 Jeu d'énigmes avec IA")

# Protection par mot de passe
password = st.text_input("Mot de passe :", type="password")
if password != st.secrets["PASSWORD"]:
    st.stop()
    
# Afficher la conversation
for message in st.session_state.historique:
    if message["role"] == "assistant":
        st.write("🤖 " + message["content"])
    elif message["role"] == "user" and message["content"] != "Pose-moi une énigme.":
        st.write("👤 " + message["content"])

# Zone de réponse uniquement si une énigme a été posée
if len(st.session_state.historique) > 0:
    reponse = st.text_input("Ta réponse :")
    if st.button("Valider") and reponse:
        st.session_state.historique.append({"role": "user", "content": reponse})
        texte = appeler_claude(st.session_state.historique, system)
        st.session_state.historique.append({"role": "assistant", "content": texte})
        st.rerun()
