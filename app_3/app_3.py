import streamlit as st
import pandas as pd
# Editeur de base de données
from mitosheet.streamlit.v1 import spreadsheet

st.set_page_config(
    page_title="Use Pygwalker In Streamlit",
    layout="wide"
)

st.title("Introduction de Pygwalker pour la visualisation des données")
st.markdown("Avec la librairie ```Mitosheet```, il est possible d'afficher efficacement la base de données et de la "
            "visualiser aavec des graphiques. Toutefois les fonctionnalités sont limités ( Besoin d'un abonnement"
            "pro pour profiter de toutes les fonctionnalités. Ce package ne sera pas utilisé pour nos tableaux de "
            "bord")

st.sidebar.title("INFORMATION")
st.sidebar.write("Element 1 ")


data = pd.read_csv("app_3/Cancer_Data.csv")

# Affichage du dataframe dans l'editeur Mito
final_data, code = spreadsheet(data)
st.write(final_data)

# Affichage du code python equivalent
st.code(code)

