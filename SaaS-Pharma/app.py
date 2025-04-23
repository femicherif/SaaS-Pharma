
import streamlit as st
import pandas as pd

# Titre
st.title("Assistant Médicament 💊 - Version locale")

# Charger la base de données locale
@st.cache_data
def charger_donnees():
    return pd.read_csv("medicaments.csv")

df = charger_donnees()

# Entrée utilisateur
medicament = st.text_input("Nom du médicament à rechercher :").strip().lower()

if medicament:
    resultats = df[df['nom'].str.lower() == medicament]

    if not resultats.empty:
        ligne = resultats.iloc[0]
        st.subheader("Indications principales :")
        st.write(ligne['indications'])

        st.subheader("Posologie par jour :")
        st.write(ligne['posologie'])

        st.subheader("Durée du traitement :")
        st.write(ligne['duree'])

        st.subheader("Génériques proposés :")
        st.write(ligne['generiques'])
    else:
        st.error("Ce médicament n'existe pas encore dans la base. 🚫")
