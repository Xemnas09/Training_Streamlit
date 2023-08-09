import streamlit as st
import pandas as pd

# On change le titre de l’onglet du navigateur web
st.set_page_config(page_title="Widget Streamlit", layout="wide")
st.title("Familiarisation avec les Widgets de streamlit")

"""
# Slider (barre de valeur)
"""

"""
Ce widget crée une barre horizontale de valeur. Par exemple:
"""

# Barre de défilement
x = st.slider(label="x")

"""
L'objet généré est contenu dans une variable (ici ```x```). On peut donc afficher la valeur:
"""

st.code(f"La valeur de x est {x} \n" f"le carré de x est {x**2}")

"""
# Text input (zone de saisie de texte)
"""

"""
Ce widget permet à l'utilisateur de saisir du texte. Par exemple:
"""
# zone de saisie
nom = st.text_input(label="Ton nom")

st.markdown(" De même, il est possible d'afficher la saisie de l'utilisateur:")
# Acces à la valeur saisie
st.code(f"Ton nom est {nom}")

"""
# chechbox
"""
"""
Ce widget permet entre autre d'afficher ou de masquer une section de son application. Par exemple, on peut decider
d'afficher ou non une base de données:
"""


@st.cache_data
def database():
    return pd.read_csv("app_4/Cancer_Data.csv")


data = database()

# Affichage de la base de données au choix de l’utilisateur
if st.checkbox(label="Show database"):
    data = database()
    st.dataframe(data.style.highlight_max(axis=0))

"""
En cochant la case, l'utilisateur peut faire apparaitre la base de données
"""


"""
# Selectbox
"""

"""
Ce Widget lui est utilisé lorsqu'on veut faire un choix parmis plusieurs valeurs. Par exemple, on peut l'utiliser pour 
selectionner la colonne de notre base de données que l'on souhaite afficher
"""
show_colomn = st.selectbox(
    label="Colonne",
    options=database().columns
)
st.dataframe(database().loc[:, [show_colomn]])

"""
L'utilisateur choisis ainsi la colonne qu'il souhaite visualiser
"""


"""
**Note**: Il est possible de créer un widget sans avoir à le mettre dans une variable. Auquel cas, afin d'afficher sa
 valeur, il est necessaire de lui associer une clé afin de pouvoir identifier de manière unique chaque widget (car il 
 est possible d'avoir plusieurs ```Slider``` ou ```Text input``` sur l'interface. Cela ce fait avec l'argument ```key```
 qui prend en valeur une chaîne de caractère. Lorsque cela est fait, la valeur du widget est accesible via la commande
  ```st.session_state.key``` où ```key``` est la clé du widget
"""
