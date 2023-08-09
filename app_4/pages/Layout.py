import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Layout Streamlit", layout="wide")
st.title("Layout avec Streamlit")

"""
Streamlit permet de gérer la disposition des widgets de manière très simple avec la fonction ```st.columns```. Il permet
d'organiser les widgets (ou du texte selo, ce que l'on souhaite afficher) en colonne en divisant l'interface. Le nombre
de colonne est passé en argument à la fonction. Par exemple:
"""

col1, col2 = st.columns(2)

with col1:
    """
    Nous pouvons diviser la zone en 2 colonnes
    """

with col2:
    """
    Et disposer nos élément sur l'interface
    """

"""
C'est un bon moyens de concevoir des tableaux de bord en disposant plusieurs graphiques sur une même ligne. Imaginons
que l'on souhaite afficher 2 graphiques sur la même ligne:
"""

@st.cache_data
def database():
    # On importe ka base de données et on retire les colonnes indésirables
    return pd.read_csv("app_4/Cancer_Data.csv").drop(["id", "Unnamed: 32"], axis=1)


col3, col4 = st.columns(2)

with col3:
    diagnosis_count = database().groupby("diagnosis").size().reset_index(name="Counts")
    diagnosis_distribution = px.bar(
        data_frame=diagnosis_count,
        x="diagnosis",
        y="Counts",
        color="diagnosis",
        title="Distribution de la variable diagnosis"
    )
    st.plotly_chart(diagnosis_distribution)

with col4:
    show_column = st.selectbox(label="Colonne", options=database().drop(["diagnosis"], axis=1).columns)
    variable_distribution = px.histogram(database(), x=f"{show_column}")
    st.plotly_chart(variable_distribution)
