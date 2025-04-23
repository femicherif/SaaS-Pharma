import streamlit as st
import requests
from bs4 import BeautifulSoup

def chercher_rcp(medicament):
    base_url = "https://base-donnees-publique.medicaments.gouv.fr"
    search_url = f"{base_url}/index.php?search={medicament}&page=1"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    lien_rcp = soup.find('a', text='RCP')
    if lien_rcp:
        rcp_url = base_url + lien_rcp.get('href')
        rcp_page = requests.get(rcp_url)
        return rcp_page.text
    else:
        return None

def extraire_infos(rcp_text):
    if not rcp_text:
        return None, None, None, None
    soup = BeautifulSoup(rcp_text, 'html.parser')
    sections = soup.find_all('div', class_='section')
    indications = ""
    posologie = ""
    duree = ""
    generiques = "À rechercher manuellement (fonction à intégrer plus tard)"
    for section in sections:
        titre = section.find('h2')
        if titre:
            titre_text = titre.get_text().strip().lower()
            contenu = section.get_text().strip()
            if 'indications thérapeutiques' in titre_text:
                indications = contenu
            elif 'posologie et mode d’administration' in titre_text:
                posologie = contenu
            elif 'durée du traitement' in titre_text:
                duree = contenu
    return generiques, indications, posologie, duree

st.title("Assistant Médicament 📋")
medicament = st.text_input("Nom du médicament :")
if medicament:
    with st.spinner("Recherche en cours..."):
        rcp = chercher_rcp(medicament)
        generiques, indications, posologie, duree = extraire_infos(rcp)
        if rcp:
            st.subheader("Indications principales :")
            st.write(indications or "Non trouvé")
            st.subheader("Posologie recommandée :")
            st.write(posologie or "Non trouvée")
            st.subheader("Durée du traitement :")
            st.write(duree or "Non précisée")
            st.subheader("Génériques suggérés :")
            st.write(generiques)
        else:
            st.error("Aucune RCP trouvée pour ce médicament.")
