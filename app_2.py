import streamlit as st
import pandas as pd
from sklearn.datasets import  load_iris

st.title("Affichage d'une base de données")
@st.cache_data
def load_data():
    iris = load_iris()
    database = pd.DataFrame(
        data=iris.data,
        columns=iris.feature_names)

    database['target'] = iris.target
    return database

st.write(load_data())
