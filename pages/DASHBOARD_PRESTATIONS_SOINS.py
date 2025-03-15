##_____________________________________________________________________________________________
##___________importation des bibliotheques_____________________________________________________

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import geopandas as gdp
import folium
import contextily as ctx
import matplotlib.pyplot as plt

#@st.cache

##_____________________________________________________________________________________________
##___________IMPORTATION DES DONNEES  ET DU NETOYYAGE DES DATASETS_____________________________

########################### Données sur les ressources en santé du BURKINA FASO################
ressource=pd.read_csv("Gouvernance_data.csv",sep=';', decimal=',',encoding='ISO-8859-1')
ressource=ressource.rename(columns={'Rayon daction moyen théorique en km': "Rayon d'action moyen théorique en km" })
#st.write("Donnée brute par district sanitaire")
#st.dataframe(ressource.head(5))
########################### Données district et calcul des indicateurs par région ################
ds=pd.read_csv("Dataset_DS.csv",sep=';', decimal=',',encoding='ISO-8859-1')

#Regroupement des données par région
data_reg=ds.groupby(["region","Annee"]).sum()
data_reg=data_reg.reset_index()
data2=data_reg.drop(["pays", "province","District"], axis=1)

#Calcul des indicateurs
# Soins curatif et hospitalisation
data2["Nouveaux contacts par habitant"] = (data2["CE-Nouveaux consultants"] / data2["GEN - Population total"]).round(2)
data2["Nouveau contact chez les moins de 5 ans"] = (data2["CE-Nouveaux consultants moins de cinq ans"] /
                                                    data2["GEN - Population de moins de 5 ans"]).round(2)
data2["Proportion (%) d’enfants pris en charge selon l'approche PCIME"] = (100*data2["Nombre de enfants pris en charge selon approche PCIME"] /
                                                                           data2["CE-Nouveaux consultants moins de cinq ans"]).round(2)
# Santé maternelle
data2["Taux (%) d'accouchement dans les FS"] = (100* data2["SMI-Accouchement total"] / data2["Accouchements attendus"]).round(1)
data2["Taux (%) de couverture en CPN1"] = (100* data2["Nombre de CPN1"] / data2["Grossesses attendues"]).round(1)
data2["Taux (%) de couverture en CPN4"] = (100* data2["Nombre de CPN4"] / data2["Grossesses attendues"]).round(1)
data2["Pourcentage des femmes enceintes vues au 1er trimestre"] = (100* data2["Nombre de CPN1 vues au 1er trimestre de la grossesse"] /
                                                                   data2["Nombre de CPN1"]).round(1)
data2["Pourcentage des femmes enceintes ayant bénéficié du TPI3"] = (100* data2["Nombre de femmes enceintes ayant recu le TPI3"] /
                                                                     data2["Nombre de CPN1"]).round(1)
data2["Proportion (%) de faible poids de naissance"] = (100* data2["Nouveau-nes a terme de moins de 2500 g  a la naissance"] /
                                                        data2["SMI-total naissance vivante"]).round(1)
data2["Couverture (%) en consultation postnatale 6e semaine"] = (100* data2["Consultations postnatales  6eme-8eme semaine"] /
                                                                 data2["SMI-Nombre de femmes ayant accouche"]).round(1)
data2["Couverture (%) en consultation postnatale 6e heure"] = (100* data2["Consultations postnatales  6eme-8eme heure"] /
                                                               data2["SMI-Nombre de femmes ayant accouche"]).round(1)
data2["Taux (%) de confirmation du paludisme"] = (100* data2["Palu-TDR et GE realises"] /data2["Palu-Cas de paludisme suspect cas"]).round(1)

###création du dataset des indicateurs par région
# Variable a supprimer dans la base region afin d'alleger le dataset
data_brute=['Accouchements attendus', 'CE-Nouveaux consultants',
       'CE-Nouveaux consultants moins de cinq ans',
       'Consultations postnatales  6eme-8eme heure',
       'Consultations postnatales  6eme-8eme semaine',
       'Enfants de 0 -11 mois ayant recu le DTC-HepB-Hib1',
       'Enfants de 0 -11 mois ayant recu le DTC-HepB-Hib3',
       'Femmes vues en CPN au cours du mois et ayant beneficie dun test VIH',
       'GEN - Population de moins de 5 ans', 'GEN - Population total',
       'Grossesses attendues', 'Naissances vivantes attendues',
       'Nombre de CPN1',
       'Nombre de CPN1 vues au 1er trimestre de la grossesse',
       'Nombre de CPN4',
       'Nombre de enfants pris en charge selon approche PCIME',
       'Nombre de femmes enceintes ayant recu le TPI3',
       'Nouveau-nes a terme de moins de 2500 g  a la naissance',
       'Nouveau-nes mis aux seins dans lheure qui suit la naissance',
       'Palu-Cas de paludisme suspect cas', 'Palu-TDR et GE realises',
       'Population < 1 an', 'SMI-Accouchement total',
       'SMI-Nombre de femmes ayant accouche', 'SMI-total naissance vivante']


indic_region=data2.drop(data_brute, axis=1)

########################### Données district et calcul des indicateurs au niveau national ################
data_nat=ds.groupby(["pays","Annee"]).sum()
data_nat=data_nat.reset_index()
data3=data_nat.drop(["region", "province","District"], axis=1)

# Soins curatif et hospitalisation NATIONAL
data3["Nouveaux contacts par habitant"] = (data3["CE-Nouveaux consultants"] / data3["GEN - Population total"]).round(2)
data3["Nouveau contact chez les moins de 5 ans"] = (data3["CE-Nouveaux consultants moins de cinq ans"] /
                                                    data3["GEN - Population de moins de 5 ans"]).round(2)
data3["Proportion (%) d’enfants pris en charge selon l'approche PCIME"] = (100*data3["Nombre de enfants pris en charge selon approche PCIME"] /
                                                                           data3["CE-Nouveaux consultants moins de cinq ans"]).round(2)
# Santé maternelle
data3["Taux (%) d'accouchement dans les FS"] = (100* data3["SMI-Accouchement total"] / data3["Accouchements attendus"]).round(1)
data3["Taux (%) de couverture en CPN1"] = (100* data3["Nombre de CPN1"] / data3["Grossesses attendues"]).round(1)
data3["Taux (%) de couverture en CPN4"] = (100* data3["Nombre de CPN4"] / data3["Grossesses attendues"]).round(1)
data3["Pourcentage des femmes enceintes vues au 1er trimestre"] = (100* data3["Nombre de CPN1 vues au 1er trimestre de la grossesse"] /
                                                                   data3["Nombre de CPN1"]).round(1)
data3["Pourcentage des femmes enceintes ayant bénéficié du TPI3"] = (100* data3["Nombre de femmes enceintes ayant recu le TPI3"] /
                                                                     data3["Nombre de CPN1"]).round(1)
data3["Proportion (%) de faible poids de naissance"] = (100* data3["Nouveau-nes a terme de moins de 2500 g  a la naissance"] /
                                                        data3["SMI-total naissance vivante"]).round(1)
data3["Couverture (%) en consultation postnatale 6e semaine"] = (100* data3["Consultations postnatales  6eme-8eme semaine"] /
                                                                 data3["SMI-Nombre de femmes ayant accouche"]).round(1)
data3["Couverture (%) en consultation postnatale 6e heure"] = (100* data3["Consultations postnatales  6eme-8eme heure"] /
                                                               data3["SMI-Nombre de femmes ayant accouche"]).round(1)
data3["Taux (%) de confirmation du paludisme"] = (100* data3["Palu-TDR et GE realises"] /data3["Palu-Cas de paludisme suspect cas"]).round(1)

indic_nat=data3.drop(data_brute, axis=1)


###_______________________________fusion de dataframe region et national_______________
df_nat=indic_nat
df_nat = df_nat.rename(columns={'pays': 'region'}) ## pour avoir les memes nom de colonnes
df_concat = pd.concat([df_nat, indic_region], ignore_index=True)
df_concat = df_concat.rename(columns={'region': 'organisation_unit'})


##_____________________________________________________________________________________________
##_____________________________DECLARATION DES VARIABLES ______________________________________

# liste des structures du dataframe fuisionner (region et national)
org_unit=['Burkina Faso', 'Boucle du Mouhoun', 'Cascades', 'Centre',
       'Centre Est', 'Centre Nord', 'Centre Ouest', 'Centre Sud', 'Est',
       'Hauts Bassins', 'Nord', 'Plateau Central', 'Sahel', 'Sud Ouest']

# liste des indicateurs du dataframe fuisionner (region et national)

numeric_col=["Nouveaux contacts par habitant",
       "Nouveau contact chez les moins de 5 ans",
       "Proportion (%) d’enfants pris en charge selon l'approche PCIME",
       "Taux (%) d'accouchement dans les FS", "Taux (%) de couverture en CPN1",
       "Taux (%) de couverture en CPN4",
       "Pourcentage des femmes enceintes vues au 1er trimestre",
       "Pourcentage des femmes enceintes ayant bénéficié du TPI3",
       "Proportion (%) de faible poids de naissance",
       "Couverture (%) en consultation postnatale 6e semaine",
       "Couverture (%) en consultation postnatale 6e heure",
       "Taux (%) de confirmation du paludisme"]

###liste des années du daset fusion
#annee=[2024,2023,2022,2021,2020]
annee=ds["Annee"].unique().tolist()




##_____________________________________________________________________________________________
##___________Titre du dashboard et du context dans streamlit___________________________________
with st.sidebar:
    col7, col8,col9 = st.columns(3)
    
    with col7:
        st.image("armoiries_bfa.png", use_container_width=True)
    
    with col8:
        st.image("armoiries_bfa.png", use_container_width=True)
    with col9:
        st.image("armoiries_bfa.png", use_container_width=True)


##_____________________________________________________________________________________________
##_____________________________CREATION DE LA BARRE LATERALE POUR LE CHOIX DES PARAMETRES _____
st.sidebar.title("choix des parametres")

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            background-color: #f0f2f6;  /* Couleur de fond */
        }
        section[data-testid="stSidebar"] h1 {
            color: darkblue; /* Couleur du texte */
        }
    </style>
""", unsafe_allow_html=True)

#st.markdown("<h3 style='color:blue; font-weight:bold;'>Choisis l'indicateur à visualiser:</h3>", unsafe_allow_html=True)
var_y=st.sidebar.selectbox("Choisis l'indicateur à visualise",numeric_col)
structure=st.sidebar.selectbox("Choisis l'unité d'organisation",org_unit)
var_an=st.sidebar.selectbox("Choisis l'année pour la visualisation",annee)

##_____________________________________________________________________________________________
##___________# Créer les onglets dans streamlit___________________________________


titres_onglets = ["TABLEAU DE BORD", "DONNEES DE BASE"]
onglet1, onglet2 = st.tabs(titres_onglets)
 
# Ajouter du contenu à chaque onglet
with onglet1:
##_____________________________________________________________________________________________
##_____________________________DEFINITION DES OBJECTIFS ET DE CERTAINS PARAMETRES______________

    ### objectif par indicateurs par région et national
    objectif=""
    if var_y=="Nouveaux contacts par habitant":
        objectif=1
    elif var_y=="Nouveau contact chez les moins de 5 ans":
        objectif=2
    elif var_y=="Proportion (%) d’enfants pris en charge selon l'approche PCIME":
        objectif=80
    elif var_y=="Taux (%) d'accouchement dans les FS":
        objectif=85
    elif var_y=="Taux (%) de couverture en CPN1":
        objectif=80
    elif var_y=="Taux (%) de couverture en CPN4":
        objectif=50
    elif var_y=="Pourcentage des femmes enceintes vues au 1er trimestre":
        objectif=50
    elif var_y=="Pourcentage des femmes enceintes ayant bénéficié du TPI3":
        objectif=90
    elif var_y=="Proportion (%) de faible poids de naissance":
        objectif=10
    elif var_y=="Couverture (%) en consultation postnatale 6e semaine":
        objectif=50
    elif var_y=="Couverture (%) en consultation postnatale 6e heure":
        objectif=90
    elif var_y=="Taux (%) de confirmation du paludisme":
        objectif=95

########################################################################################
## Barre laterale de separation entre les sections
    st.markdown(
    """
    <style>
    .custom-hr {
        border: none;
        height: 3px;
        background: linear-gradient(to right, #2E86C1, #AED6F1);
        margin: 20px 0;
    }
    </style>
    <hr class="custom-hr">
    """,
    unsafe_allow_html=True
    )

   # _____________________________________________________________________________________________
    ##_____________________________VISUALISATION DES INDICATEURS DE REGION ET NATIONAL_____________

    # parametre de l'axe des ordonnées
    if var_y=="Nouveaux contacts par habitant" or var_y=="Nouveau contact chez les moins de 5 ans":
        ordonnee="Nombre"
    else :
        ordonnee="Pourcentage"

    # parametre de l'axe des ordonnées
    if var_y=="Nouveaux contacts par habitant" or var_y=="Nouveau contact chez les moins de 5 ans":
        expression="contacts au moins"
    else :
        expression="%"


    # filtre de l'unité d'organisation
    df_fusion = df_concat.query("organisation_unit == @structure")

    ### EVOLUTION DES INDICATEURS PAR STRUCTURE
   
####################################
   # _____________________________________________________________________________________________
    ##_____________________________VISUALISATION DES INDICATEURS DE REGION ET NATIONAL_____________

    # parametre de l'axe des ordonnées
    if var_y=="Nouveaux contacts par habitant" or var_y=="Nouveau contact chez les moins de 5 ans":
        ordonnee="Nombre"
    else :
        ordonnee="Pourcentage"

    if structure=="Burkina Faso":
        itemstructure="du"
    else :
        itemstructure="de la région de"

    # parametre de l'axe des ordonnées
    if var_y=="Nouveaux contacts par habitant" or var_y=="Nouveau contact chez les moins de 5 ans":
        expression="contacts au moins"
    else :
        expression="%"

            # parametre de l'axe des ordonnées
    if var_y=="Nouveaux contacts par habitant" or var_y=="Nouveau contact chez les moins de 5 ans":
        maxy=3
    else :
        maxy=100
    y_max = df_fusion[var_y].max() * 1.4  # Ajoute 10% de marge

    # filtre de l'unité d'organisation
    df_fusion = df_concat.query("organisation_unit == @structure")

    ### EVOLUTION DES INDICATEURS PAR STRUCTURE
    st.markdown(f"##### 🎯 L'objectif **PNDS** de **{var_y}** est de **{objectif} {expression}** ✅")
    
    fig3=px.line(df_fusion, x="Annee",y=var_y,text=var_y,title=f"Graphique3:Evolution du {var_y} {itemstructure} {structure} ")
    fig3.update_traces(line=dict(width=2))
    fig3.update_layout(
    plot_bgcolor="lightgray",
    paper_bgcolor="white",
    yaxis=dict(range=[0,  y_max]))
    fig3.update_traces(
        textposition="top center",
        texttemplate="<b>%{text:.1f}</b>",
        marker=dict(size=10, color="red"), 
    )
    fig3.update_layout(
        xaxis=dict(
            tickfont=dict(color="purple")))  # Changer la couleur des labels de l'axe X
        
    fig3.add_hline(y=objectif, line_dash="dash", line_color="red", annotation_text="Objectif", annotation_position="top left")
    fig3.update_traces(textposition="top center")
    st.plotly_chart(fig3)
    
            ## Barre laterale de separation entre les sections
    st.markdown(
    """
    <style>
    .custom-hr {
        border: none;
        height: 3px;
        background: linear-gradient(to right, #2E86C1, #AED6F1);
        margin: 20px 0;
    }
    </style>
    <hr class="custom-hr">
    """,
    unsafe_allow_html=True
    )
    st.markdown(f"##### 🎯 L'objectif **PNDS** de **{var_y}** est de **{objectif} {expression}** ✅")
  #####presentation par région
    data_an=indic_region.query("Annee== @var_an").sort_values(by=var_y)
    #st.write(data_an)

    #################Présentation par région
    fig4=px.bar(data_an, x="region",y=var_y, text=var_y,title=f"Graphique4: {var_y} par région en {var_an}",color_continuous_scale=px.colors.sequential.Viridis)
    fig4.add_hline(y=objectif, line_dash="dash", line_color="red", annotation_text="Objectif", annotation_position="top left")
    fig4.update_layout(
        xaxis=dict(
            tickfont=dict(color="purple")))  # Changer la couleur des labels de l'axe X
    st.plotly_chart(fig4)
    st.markdown(
    """
    <style>
    .custom-hr {
        border: none;
        height: 3px;
        background: linear-gradient(to right, #2E86C1, #AED6F1);
        margin: 20px 0;
    }
    </style>
    <hr class="custom-hr">
    """,
    unsafe_allow_html=True
    )
#################SYSTEME D'INFORMATION GEOGRAPHIQUE#########################
#### SYSTEME D'INFORMATION GEOGRAPHIQUE
    # importation du shapefile
    district=gdp.read_file("district_sanitaire.shp")
    fosa=gdp.read_file("centre_sante.shp")

    # Affichage de la table district
    #district.head()
    ########### carte thematique
    region_sig="BOUCLE DU MOUHOUN"
    if structure=="Boucle du Mouhoun":
        region_sig="BOUCLE DU MOUHOUN"
    elif structure=="Cascades":
        region_sig="CASCADES"
    elif structure=="Centre":
        region_sig="CENTRE"
    elif structure=="Centre Est":
        region_sig="CENTRE-EST"
    elif structure=="Centre Nord":
        region_sig="CENTRE-NORD"
    elif structure=="Centre Ouest":
        region_sig="CENTRE-OUEST"
    elif structure=="Centre Sud":
        region_sig="CENTRE-SUD"
    elif structure=="Est":
        region_sig="EST"
    elif structure=="Hauts Bassins":
        region_sig="HAUTS-BASSINS"
    elif structure=="Nord":
        region_sig="NORD"
    elif structure=="Plateau Central":
        region_sig="PLATEAU-CENTRAL"
    elif structure=="Sahel":
        region_sig="SAHEL"
    elif structure=="Sud Ouest":
        region_sig="SUD-OUEST"

    region=district[district["Region"]==region_sig]
    zoom_level = 12

    if structure=="Burkina Faso":
            #district.plot(figsize=(20,20))
            fig33, ax33=plt.subplots(figsize=(30,30))
            district.plot(column="Completude",cmap="RdYlBu",legend=True, vmin=0, vmax=100,edgecolor="black", linewidth=2,ax=ax33)
            for idx, row in district.iterrows():
                ax33.text(row.geometry.centroid.x,row.geometry.centroid.y,row["Nom_DS"], fontsize=12)
                ax33.set_title(f"Carte: Complétude des RMA du {structure} en 2024 par district", fontsize=40,color="navy",	loc="left",pad=20)
            # Ajouter un fond de carte OpenStreetMap
            ctx.add_basemap(ax33, source=ctx.providers.OpenStreetMap.Mapnik,zoom=zoom_level)
            st.pyplot(fig33)
    else:
            
            ## region selectionner
        #district.plot(figsize=(20,20))
        fig55, ax55=plt.subplots(figsize=(30,30))
        region.plot(column="Completude",cmap="RdYlBu",legend=True, vmin=0, vmax=100, edgecolor="black", linewidth=2,ax=ax55)
        for idx, row in region.iterrows():
            ax55.text(row.geometry.centroid.x,row.geometry.centroid.y,row["Nom_DS"], fontsize=12)
            ax55.set_title(f"Carte: Complétude des RMA de la région du {structure} en 2024 par district", fontsize=40,color="navy",	loc="left",pad=20)
        # Ajouter un fond de carte OpenStreetMap
        ctx.add_basemap(ax55, source=ctx.providers.OpenStreetMap.Mapnik,zoom=zoom_level)
        #st.pyplot(fig3)
        st.pyplot(fig55)







###################PRESENTATION DES TABLEAUX DE DONNEES#####################
with onglet2:
    st.header("Données sur les ressources en santé")
    st.write(ressource.head())
    st.header('Données brute des districts sanitaire')
    st.write(ds.head())
    st.header('Indicateurs par région')
    st.write(data2.head()) 
