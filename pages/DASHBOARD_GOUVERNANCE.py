##___________importation des bibliotheques_____________________________________________________

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

##_____________________________________________________________________________________________
##___________IMPORTATION DES DONNEES  ET DU NETOYYAGE DES DATASETS_____________________________

########################### Données sur les ressources en santé du BURKINA FASO################
ressource=pd.read_csv("Gouvernance_data.csv",sep=';', decimal=',',encoding='ISO-8859-1')
ressource=ressource.rename(columns={'Rayon daction moyen théorique en km': "Rayon d'action moyen théorique en km" })
#st.write("Donnée brute par district sanitaire")
#st.dataframe(ressource.head(5))

##_____________________________________________________________________________________________
### indicateurs de ressources(personnels et infrastructures)
val_gouv=["Rayon d'action moyen théorique en km",
       "Ratio population/médecin ", "Ratio habitants/infirmier",
       "Ratio population/SFE-ME"]

    ##_____________________________VISUALISATION DES INDICATEURS DE RESSOURCES_____________________
message2="Choisis l'indicateurs de ressources à visualiser"
st.markdown(f"<h3 style='font-size:18px; color:navy; text-align:left;'>{message2}</h3>", unsafe_allow_html=True)
valeur_indic=st.selectbox("",val_gouv)
norme_PNDS=""
if valeur_indic=="Rayon d'action moyen théorique en km":
    norme_PNDS=5
elif valeur_indic=="Ratio population/médecin ":
    norme_PNDS=5000
elif valeur_indic=="Ratio habitants/infirmier":
    norme_PNDS=2000
elif valeur_indic=="Ratio population/SFE-ME":
    norme_PNDS=3000


####Message en fonction de l'indicateur
if valeur_indic=="Rayon d'action moyen théorique en km":
    message=f"La vision du Ministère de la santé est de rapprocher de moins de {norme_PNDS} km les centres de santé aux populations "
elif valeur_indic=="Ratio population/médecin ":
    message=f"La vision du Ministère de la santé est que chaque médecin doit prendre en charge moins de {norme_PNDS} personnes"
elif valeur_indic=="Ratio habitants/infirmier":
    message=f"La vision du Ministère de la santé est que chaque infirmier doit prendre en charge moins de {norme_PNDS} personnes"
elif valeur_indic=="Ratio population/SFE-ME":
    message=f"La vision du Ministère de la santé est que chaque sage femme/maieuticien doit prendre en charge moins de {norme_PNDS} personnes"

st.markdown(f"<h3 style='font-size:16px; color:navy; text-align:left;'>{message}</h3>", unsafe_allow_html=True)

    ##filtre les données
##filtre les données
    
df_res = ressource[ressource["Annee"].isin([2021,2022,2023])]
#st.markdown(f"<h3 style='font-size:14px; color:red; text-align:left;'>Graphique1: Evolution du {valeur_indic} de 2021 à 2023 </h3>", unsafe_allow_html=True)
        ##### norme pnds pour les indicateurs globaux

## choix des indicateurs liés
var_connex="Centre de sante publique" #par defaut
if valeur_indic=="Rayon d’action moyen théorique en km":
    var_connex="Centre de sante publique"
elif valeur_indic=="Ratio population/médecin ":
    var_connex="Effectif Médecins"
elif valeur_indic=="Ratio habitants/infirmier":
    var_connex="Effectif Infirmiers"
elif valeur_indic=="Ratio population/SFE-ME":
    var_connex="Effectif de Sage femme"

###graph
fig1 = px.bar(df_res, x="Annee", y=valeur_indic,
text=valeur_indic, color_discrete_sequence=["#4AA3A2", "#A7001E"],title=f"Graphique1: Evolution du {valeur_indic} de 2021 à 2023"
)
fig1.add_hline(y=norme_PNDS, line_dash="dash", line_color="red", annotation_text="Objectif", annotation_position="top left")
fig1.update_layout(
        xaxis=dict(
            tickfont=dict(color="purple")))  # Changer la couleur des labels de l'axe X
st.plotly_chart(fig1)


#####
fig2=px.bar(df_res, x="Annee",y=var_connex, color="Disponibilite", text=var_connex,color_discrete_sequence=["#4AA3A2", "#A7001E"],title=f"la situation de la disponibilité et du gap de l' {var_connex} pour atteindre les objectifs")
fig2.update_layout(
        xaxis=dict(
            tickfont=dict(color="purple")))  # Changer la couleur des labels de l'axe X
st.plotly_chart(fig2)


