import streamlit as st
import plotly.express as px
import pandas as pd

st.title("Layout avec Streamlit")
authenticator.logout("logout", "sidebar")

"""
Streamlit permet de gérer la disposition des widgets de manière très simple avec la fonction ```st.columns```. Il permet
d'organiser les widgets (ou du texte selon ce que l'on souhaite afficher) en colonne en divisant l'interface. Le nombre
de colonne est passé en argument à la fonction. Par exemple:
"""

col1, col2 = st.columns(2)

with col1:
    """
    ## What is Lorem Ipsum?
    Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's 
    standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a 
    type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, 
    remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing 
    Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of 
    Lorem Ipsum.
    """

with col2:
    """
    ## Why do we use it?
    It is a long established fact that a reader will be distracted by the readable content of a page when looking at its
     layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to 
     using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web 
     page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web 
     sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on 
     purpose (injected humour and the like).
    """

"""
C'est un bon moyens de concevoir des tableaux de bord en disposant plusieurs graphiques sur une même ligne. Cependant,
si l'on dispose des graphiques ainsi et  que l'on modifie la taille de la page, les graphuques ne vont pas s'adapter à 
cette dernière. Si nous souhaitons avoir des éléments qui adapte automatiquement sa largeur à la page, il faut inclure 
ces éléments dans un **conteneur**. Cela peut se faire avec la commande ```st.container```. Il faut également inclure 
dans la fonction de sortie l'argument ```use_container_width```. Imaginons que l'on souhaite afficher 2 graphiques sur 
la même ligne:
"""


@st.cache_data
def database():
    # On importe ka base de données et on retire les colonnes indésirables
    return pd.read_csv("app_4/Cancer_Data.csv").drop(["id", "Unnamed: 32"], axis=1)


with st.container():
    col3, col4 = st.columns(2)
    with col3:
        diagnosis_count = (
            database().groupby("diagnosis").size().reset_index(name="Counts")
        )
        diagnosis_distribution = px.bar(
            data_frame=diagnosis_count,
            x="diagnosis",
            y="Counts",
            color="diagnosis",
            title="Distribution de la variable diagnosis",
        )
        st.plotly_chart(diagnosis_distribution, use_container_width=True)

    with col4:
        show_column = st.selectbox(
            label="Colonne", options=database().drop(["diagnosis"], axis=1).columns
        )
        variable_distribution = px.histogram(database(), x=f"{show_column}")
        st.plotly_chart(variable_distribution, use_container_width=True)

"""
En modifiant les dimensions de la page, les 2 graphiques vont ajuster leurs dimensions et leurs positions 
automatiquement.
"""

st.file_uploader("choose a file", key="data")
