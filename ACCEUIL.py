##_____________________________________________________________________________________________
##___________importation des bibliotheques_____________________________________________________

import streamlit as st
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import plotly.express as px
#import seaborn as sns
#import geopandas as gdp
#import folium
#import contextily as ctx


###################################################################################
#def main():

logo_url = "data:image/png;base64,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"

st.markdown(
    f"""
    <style>
    .title-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #2E86C1, #AED6F1);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
    }}

    .logo {{
        width: 60px;
        height: 60px;
        margin-right: 15px;
    }}

    .title-text {{
        font-size: 36px;
        font-weight: bold;
        color: white;
        font-family: 'Arial', sans-serif;
        margin: 0;
    }}

    .subtitle-text {{
        font-size: 20px;
        color: white;
        font-style: italic;
        font-family: 'Arial', sans-serif;
        margin-top: 5px;
    }}
    </style>

    <div class="title-container">
        <img src="{logo_url}" class="logo">
        <div>
            <p class="title-text">📊 Tableau de Bord 2019-2024</p>
            <p class="subtitle-text">Analyse des indicateurs clés</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")
message1="🏡L'objectif du tableau de bord est de mettre en exergue les performances et les contre-performances de la mise en œuvre du Plan national de développement sanitaire du Burkina Faso.<br>📊 Il presente la tendance des indicateurs pour le niveau national et par région en fonction des objectifs du PNDS.<br>🏥 Il offre la possibilité de predire la performance d'une formation sanitaire en fonction du niveau d'attente de quelques indicateurs clés sur la continuité des soins"

# Utilisation de la variable dans du HTML et CSS
st.markdown(
    f"""
    <style>
    .custom-text {{
        font-size: 18px;
        font-weight: bold;
        color: #000080;
        text-align: justify
        background-color: #f4f4f4;
        padding: 10px;
        border-radius: 10px;
    }}
    </style>
    <div class="custom-text">{message1}</div>
    """,    unsafe_allow_html=True
    )



##___________Titre du dashboard et du context dans streamlit___________________________________
with st.sidebar:
    col7, col8,col9 = st.columns(3)
    
    with col7:
        st.image("armoiries_bfa.png", use_container_width=True)
    
    with col8:
        st.image("armoiries_bfa.png", use_container_width=True)
    with col9:
        st.image("armoiries_bfa.png", use_container_width=True)

st.sidebar.subheader("Etudiant: KABORE ADAMA")

from datetime import datetime
st.write("")
st.markdown(f"🕒 **Dernière mise à jour :** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")


#if __name__ == "__main__":
#   main()

