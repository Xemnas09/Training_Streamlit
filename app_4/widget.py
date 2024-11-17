# --- IMPORTATION DES PACKAGES NECESSAIRES ---
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import pandas as pd

# Configurartion des informartions de la page web
st.set_page_config(page_title="Widget tutorial")


# On masque la barre laterale
st.markdown(
    """
<style>
section[data-testid="stSidebar"][aria-expanded="true"] {
    display: none;
}
</style>
""",
    unsafe_allow_html=True,
)

# --- AUTHENTIFICATION DES UTILISATEURS ---

# Generation des mots de passes des utilisateurs. Pour l'authentification des utilisateurs, on commence par les créer
# dans un fichier nommé "config.yaml" (ce fichier est disponible sur le github). Dans le champ password, on va y insérer
# un encodage généré par la fonction Hasher de streamlit authenticator. La fonction Hasher va prendre en paramètre une
# chaîne de caractère (ou une liste de chaîne de caractère si l'on souhaite créer plusieurs mots de passe) qui
# correspond au mot de passe à saisir dans l'application. L’encodage lui sera inscrit dans le fichier "config.yaml".
# Streamlit authenticator selon un algorithme, va decrypter l'encodage pour obtenir le mot de passe et vérifier ainsi
# l'authentification de l'utilisateur

# Lecture du fichier "config.yaml' pour récuperer la liste des utilisateurs et leurs informations
with open("pages/config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    credentials=config["credentials"],
    cookie_name=config["cookie"]["name"],
    key=config["cookie"]["key"],
    preauthorized=config["preauthorized"],
)


# --- PAGE DE CONNEXION ---
authentication_status, name = authenticator.login(single_session=True)


if authentication_status:
    # L’utilisateur etant connecté, on peut afficher maintenant la barre laterale
    st.markdown(
        """
    <style>
    section[data-testid="stSidebar"][aria-expanded="true"] {
        display: block;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # --- ACCEUIL DE L'UTILISATEUR ---
    st.sidebar.markdown(f"**Welcome {name} :coffee:**")
    authenticator.logout("logout", "sidebar")
    st.title("Familiarisation avec les Widgets de streamlit")

    """
    # Slider (barre de valeur)
    """

    st.divider()
    """
    Ce widget crée une barre horizontale de valeur. Par exemple:
    """
    st.divider()

    # Barre de défilement
    x = st.slider(label="x")

    """
    L'objet généré est contenu dans une variable (ici ```x```). On peut donc afficher la valeur:
    """

    st.code(f"La valeur de x est {x} \n" f"le carré de x est {x**2}")

    """
    # Text_input (zone de saisie de texte)
    """

    st.divider()
    """
    Ce widget permet à l'utilisateur de saisir du texte. Par exemple:
    """
    st.divider()

    # zone de saisie
    nom = st.text_input(label="Ton nom")

    st.markdown(" De même, il est possible d'afficher la saisie de l'utilisateur:")
    # Acces à la valeur saisie
    st.code(f"Ton nom est {nom}")

    """
    # checkbox
    """

    st.divider()
    """
    Ce widget permet entre autre d'afficher ou de masquer une section de son application. Par exemple, on peut decider
    d'afficher ou non la base de données:
    """
    st.divider()

    @st.cache_data
    def database():
        return pd.read_csv("app_4/Cancer_Data.csv")

    # Affichage de la base de données au choix de l’utilisateur
    if st.checkbox(label="Show database"):
        data = database()
        st.dataframe(data, hide_index=True)

    """
    En cochant la case, l'utilisateur peut faire apparaitre la base de données
    """

    """
    # Selectbox
    """

    st.divider()
    """Ce Widget lui est utilisé lorsqu'on veut faire un choix parmis plusieurs valeurs. Par exemple, 
    on peut l'utiliser pour sélectionner la colonne de notre base de données que l'on souhaite afficher"""
    st.divider()

    show_colomn = st.selectbox(label="Colonne", options=database().columns)
    st.dataframe(database().loc[:, [show_colomn]])

    """
    L'utilisateur choisis ainsi la colonne qu'il souhaite visualiser
    """

    st.divider()
    """
    **Note**: Il est possible de créer un widget sans avoir à le mettre dans une variable. Auquel cas, afin d'afficher 
    sa valeur, il est necessaire de lui associer une clé afin de pouvoir identifier de manière unique chaque widget 
    (car il est possible d'avoir plusieurs ```Slider``` ou ```Text input``` sur l'interface. Cela ce fait avec 
    l'argument ```key``` qui prend en valeur une chaîne de caractère. Lorsque cela est fait, la valeur du widget est 
    accesible via la commande ```st.session_state.key``` où ```key``` est la clé du widget. ```st.session_state``` est 
    un **dictionnaire** receuillant l'ensemble des valeurs des widgets dont on a initialisé la clé. 
    """

    """
    L'utilisation de la session est un bon moyen de stocker certains resultat entre plusieurs exécutions de 
    l'application (Streamlit réexecute entierement le script python à chaque fois que l'utilisateur va interagir avec un
    widget de l'application). **Les valeurs des widgets dans la session peuvent être utilisé dans toutes les pages d'une
    application streamlit.**
    """
    st.divider()
elif authentication_status is False:
    st.error("Nom d'utilisateur/mot de passe incorrecte")
elif authentication_status is None:
    st.warning(
        "Entrer le nom d'utilisateur et le mot de passe (Ces informations sont disponibles sur le github)"
    )
