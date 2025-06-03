import streamlit as st
from streamlit_oauth import OAuth2Component
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Interactive Dashboard App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded" # Keep sidebar open initially
)

# OAuth2 Configuration (ensure these are loaded correctly)
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
AUTHORIZE_URL = os.environ.get("GOOGLE_AUTHORIZE_URL")
TOKEN_URL = os.environ.get("GOOGLE_TOKEN_URL")
REFRESH_TOKEN_URL = os.environ.get("GOOGLE_REFRESH_TOKEN_URL")
REVOKE_TOKEN_URL = os.environ.get("GOOGLE_REVOKE_TOKEN_URL")
REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")
SCOPE = os.environ.get("GOOGLE_SCOPE")

oauth2 = None
if not (CLIENT_ID and CLIENT_SECRET and AUTHORIZE_URL and TOKEN_URL and REDIRECT_URI and SCOPE):
    st.sidebar.warning("OAuth2 client is not configured. Google Sign-In will not be available.")
else:
    oauth2 = OAuth2Component(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        authorize_endpoint=AUTHORIZE_URL,
        token_endpoint=TOKEN_URL,
        refresh_token_endpoint=REFRESH_TOKEN_URL,
        revoke_token_endpoint=REVOKE_TOKEN_URL
    )

# Initialize session state variables
if 'token' not in st.session_state:
    st.session_state.token = None
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

# --- Logout Function ---
def logout():
    # Conceptual token revocation - actual implementation depends on library and provider
    # if st.session_state.token and oauth2 and REVOKE_TOKEN_URL:
    #     try:
    #         # This is a placeholder; actual revocation might need specific handling
    #         # oauth2.revoke_token(st.session_state.token) # This method might not exist or work this way
    #         pass
    #     except Exception as e:
    #         st.error(f"Error during token revocation: {e}")

    st.session_state.token = None
    st.session_state.authenticated = False
    st.session_state.user_info = None
    # Ensure we are on the main page after logout
    # This part needs careful handling with st.switch_page as it can't be called directly after a button press that modifies state in the same run.
    # Instead, the rerun itself will bring the user to the "logged out" state of app.py.
    # If st.query_params.get('page') indicated we were on a sub-page, Streamlit's default behavior on rerun
    # without authenticated state should correctly show app.py.
    # A direct st.switch_page("app.py") here might be problematic if not handled carefully with rerun logic.
    st.rerun()


# --- Sidebar Content ---
if st.session_state.authenticated:
    user_email = st.session_state.user_info.get("email", "Unknown User") if st.session_state.user_info else "Unknown User"
    st.sidebar.success(f"Logged in as: {user_email}")
    st.sidebar.page_link("pages/1_Dashboard.py", label="Dashboard", icon="📈")
    if st.sidebar.button("Logout"):
        logout()
else:
    st.sidebar.info("Please log in to access the dashboard.")


# --- Main Page Logic ---
st.title("Welcome to the Interactive Dashboard App")

if not st.session_state.authenticated:
    st.write("Please log in to access the dashboard.")

    if oauth2: # Only show Google button if configured
        result = oauth2.authorize_button(
            name="Sign in with Google",
            icon="https://www.google.com.tw/favicon.ico",
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            key="google_login",
            use_container_width=True,
            pkce='S256',
        )
        if result and "token" in result:
            st.session_state.token = result.get("token")
            # In a real app, decode id_token or call userinfo endpoint
            st.session_state.user_info = {"email": "user@example.com (Google)"} # Placeholder
            st.session_state.authenticated = True
            st.success("Logged in successfully with Google!")
            st.toast("Redirecting to dashboard...")
            st.switch_page("pages/1_Dashboard.py") # Automatic redirection
        elif result and "error" in result:
            st.error(f"Google login failed: {result.get('error_description', result.get('error'))}")
    else:
        # This message is shown if OAuth is not configured, below the sidebar warning
        st.info("Google Sign-In is not available due to missing configuration. Use the development login if needed.")

    st.markdown("---")
    st.subheader("For Development Only")
    if st.button("Simulate Login (Dev)"):
        st.session_state.authenticated = True
        st.session_state.user_info = {"email": "dev_user@example.com"}
        st.success("Simulated login successful!")
        st.toast("Redirecting to dashboard...")
        st.switch_page("pages/1_Dashboard.py") # Automatic redirection
else:
    # This part of app.py is shown if the user is logged in but somehow lands on app.py
    # (e.g. by manually changing URL or if st.switch_page was to app.py)
    st.write("You are logged in.")
    st.write("You can navigate to the Dashboard using the sidebar or the link below.")
    st.page_link("pages/1_Dashboard.py", label="Go to Dashboard", icon="📈")


st.info("This is the main application page. If you are logged in, use the sidebar to navigate to the dashboard or to log out.")
