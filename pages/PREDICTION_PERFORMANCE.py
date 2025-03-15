# Importer les packages
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
###############################################
with st.sidebar:
    col7, col8,col9 = st.columns(3)
    
    with col7:
        st.image("armoiries_bfa.png", use_container_width=True)
    
    with col8:
        st.image("armoiries_bfa.png", use_container_width=True)
    with col9:
        st.image("armoiries_bfa.png", use_container_width=True)

st.sidebar.image("centresante.png", use_container_width=True)





####Importation du dataset
fosa=pd.read_csv("Dataset_Fosa.csv",sep=';', decimal=',',encoding='ISO-8859-1')
st.write("**Tableau1: Base de données pour la prediction des performances des formations sanitaires**")
st.write(fosa.head())
# Nombre de lignes
nb_lignes = fosa.shape[0]
st.markdown(f"##### 1. La base initiale des formations sanitaires compte {nb_lignes} lignes")

#Choix des variables d'interet
data=fosa.select_dtypes(exclude=["object","int64"])
# Trouver les lignes contenant des valeurs manquantes
lignes_avec_na = data.isnull().any(axis=1)
# Compter le nombre de ces lignes
nombre_lignes_avec_na = lignes_avec_na.sum()
st.markdown(f"##### 2. Nombre de lignes contenant des valeurs manquantes est de {nombre_lignes_avec_na} ")
data=data.dropna()

#############INFORMATION SUR LA BASE FINALE
nb_lignes2 = data.shape[0]
st.markdown(f"##### 3. La base finale des formations sanitaires compte {nb_lignes2} lignes✅")
###
# Ramener a 100 celles superieurs à 100
data[data>100]=100
df=data.copy()
columns=df.columns.tolist()

st.write("**Tableau2: La liste des variables de la base finale**")
st.write(columns)

df.columns=["Completude_RMA", "PEC_PCIME", "Mise_sein_precoce","Taux_abandon_Penta1_Penta3", "Confirmation_palu","Femmes_vues_1ertrimestre_CPN1", "Consultation_postnatale_J1","Consultation_post_natale_J42","Accouchements_partogramme",'Performance_FS']
columns=df.columns

st.write("**tableau3: Correlation entre les variables**")
correlation=df.corr()
st.write(correlation)


###################
# Fractionner les données
x= df.drop('Performance_FS', axis = 1).values # variables prédicteurs
y = df['Performance_FS'].values # variable cible

# importer StandardScaler
from sklearn.preprocessing import StandardScaler
# Instancier StandardScaler
scaler = StandardScaler()
# Normaliser x
x = scaler.fit_transform(x)


###########
from sklearn.model_selection import train_test_split
# Splitter les données en train, val et test
x_train, x_vt,y_train,y_vt = train_test_split(x,y , test_size = 0.2, random_state = 42)
# Splitter les données en val et test
x_val, x_test, y_val, y_test = train_test_split(x_vt, y_vt, test_size = 0.5, random_state = 42)

#######Random Forest Regressor
# Recherche les paramètes optimaux du Random Forest Regressor
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
# Entrainer le modèle sur les paramètres optimaux
rf = RandomForestRegressor(max_depth=9, n_estimators= 90)
# entrainement
rf.fit(x_train, y_train)

###Evaluation du Random Forest
from sklearn.metrics import r2_score, mean_squared_error
# Calculer le R2 score et Mean Squarred Error
y_pred=rf.predict(x_val)
st.write(f"Le r2 score sur les données de validation est de: : {round(r2_score(y_pred, y_val),2)}")
st.write(f"Le mean squard erreur est : {round(mean_squared_error(y_pred, y_val),2)}")

# Calculer le R2 score sur les données d'entrainement
y_pred_t=rf.predict(x_train)
st.write(f"le R2 score sur les données d'entrainement est de: {round(r2_score(y_pred_t, y_train),2)}")

##################################################

st.write(f"**Tableau4: Verification de la prediction sur les données de test**")
x_test_20 = x_test[:20]
y_test_20 = y_test[:20]
#Predire  les labels
y_pred_20 = rf.predict(x_test_20)
for i in range(20):
  st.write("La FS ", str(i+ 1), "a un SCORE de ", round(y_pred_20[i], 2), '%', "----",round(y_test_20[i],2),'%')

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


##################
message2="CLIQUER SUR LE LIEN POUR ACCEDER A LA PAGE DE PREDICTION DE LA PERFORMANCE DES FORMATIONS SANITAIRES AU BURKINA FASO"

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
    <div class="custom-text">{message2}</div>
    """,    unsafe_allow_html=True
    )




#st.markdown(f"##### le lien vous permet de predire la performance des formations sanitaires apres introductions du niveau des indicateurs suivant: ")

st.markdown("[PAGE DE LA PREDICTION DES PERFORMANCES](https://huggingface.co/spaces/kaboradama/Projet_DIT_PerformanceFS)")

