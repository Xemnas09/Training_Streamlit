import streamlit as st
import pandas as pd
import altair as alt # Using Altair for more customizable charts

# Page Configuration
st.set_page_config(
    page_title="Iris Dashboard",
    page_icon="🌸",
    layout="wide"
)

# Authentication Check (copied from previous version)
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("🔒 Access denied. Please log in first from the main page.")
    st.stop()

user_email = st.session_state.user_info.get("email", "N/A") if st.session_state.user_info else "N/A"
st.title(f"🌸 Iris Dataset Dashboard")
st.caption(f"Logged in as: {user_email}")

# Load Data with Caching
@st.cache_data
def load_data(csv_path):
    try:
        df = pd.read_csv(csv_path)
        # Standardize column names (e.g., replace '.' with '_')
        df.columns = [col.replace('.', '_') for col in df.columns]
        return df
    except FileNotFoundError:
        st.error(f"Error: The data file was not found at {csv_path}")
        return pd.DataFrame() # Return empty DataFrame on error

iris_df = load_data("data/iris.csv")

if iris_df.empty:
    st.warning("Iris dataset could not be loaded. Dashboard cannot be displayed.")
    st.stop()

st.header("Iris Dataset Explorer")

# Sidebar for Filters
st.sidebar.header("Filters")
species_options = iris_df['variety'].unique().tolist()
selected_species = st.sidebar.multiselect(
    "Select Species to Display:",
    options=species_options,
    default=species_options
)

if not selected_species:
    st.warning("Please select at least one species to display data.")
    filtered_df = pd.DataFrame() # Empty dataframe
else:
    filtered_df = iris_df[iris_df['variety'].isin(selected_species)]

# --- Main Page Layout ---
st.subheader("1. Dataset Overview")
col1_ov, col2_ov = st.columns([1, 2])

with col1_ov:
    st.metric("Total Samples", len(iris_df))
    st.metric("Selected Samples", len(filtered_df))
    if not filtered_df.empty:
        st.write("Quick Look (Filtered Data):")
        st.dataframe(filtered_df.head(), use_container_width=True)
    else:
        st.info("No data to display based on current filters.")

with col2_ov:
    if not filtered_df.empty:
        st.write("Summary Statistics (Filtered Data):")
        st.dataframe(filtered_df.describe(), use_container_width=True)
    else:
        st.info("No summary statistics to display.")

st.divider()
st.subheader("2. Interactive Data Editor (View & Filter)")
st.info("You can sort and filter the data directly in the table below. This is a view-only editor.")
if not filtered_df.empty:
    edited_df = st.data_editor(
        filtered_df,
        disabled=True, # Make it view-only, no actual editing of source
        use_container_width=True,
        num_rows="dynamic" # Allow dynamic height adjustment
    )
else:
    st.info("No data to display in the editor based on current filters.")

st.divider()
st.subheader("3. Visualizations")

if not filtered_df.empty:
    numerical_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']

    # Scatter Plot
    st.markdown("#### Interactive Scatter Plot")
    col1_viz, col2_viz = st.columns(2)
    with col1_viz:
        x_axis = st.selectbox("Select X-axis feature:", numerical_cols, index=0)
    with col2_viz:
        y_axis = st.selectbox("Select Y-axis feature:", numerical_cols, index=2)

    if x_axis and y_axis:
        scatter_chart = alt.Chart(filtered_df).mark_circle(size=100, opacity=0.7).encode(
            x=alt.X(x_axis, title=x_axis.replace('_', ' ').title()),
            y=alt.Y(y_axis, title=y_axis.replace('_', ' ').title()),
            color='variety',
            tooltip=numerical_cols + ['variety']
        ).interactive()
        st.altair_chart(scatter_chart, use_container_width=True)
    else:
        st.warning("Please select features for both X and Y axes for the scatter plot.")

    st.markdown("#### Feature Distributions (Histograms)")
    selected_feature_hist = st.selectbox(
        "Select feature for Histogram:",
        numerical_cols,
        index=0
    )
    if selected_feature_hist:
        hist_chart = alt.Chart(filtered_df).mark_bar(opacity=0.7).encode(
            alt.X(selected_feature_hist, bin=alt.Bin(maxbins=30), title=selected_feature_hist.replace('_', ' ').title()),
            alt.Y('count()', title='Frequency'),
            color='variety',
            tooltip=[alt.Tooltip('count()', title='Frequency'), 'variety']
        ).interactive()
        st.altair_chart(hist_chart, use_container_width=True)
    else:
        st.warning("Please select a feature to display its distribution.")

    st.markdown("#### Feature Comparison (Box Plots)")
    selected_feature_box = st.selectbox(
        "Select feature for Box Plot:",
        numerical_cols,
        index=1 # Default to a different feature
    )
    if selected_feature_box:
        box_plot = alt.Chart(filtered_df).mark_boxplot(extent='min-max').encode(
            x=alt.X('variety:N', title='Variety'),
            y=alt.Y(selected_feature_box + ':Q', title=selected_feature_box.replace('_', ' ').title()),
            color='variety:N'
        ).interactive()
        st.altair_chart(box_plot, use_container_width=True)
    else:
        st.warning("Please select a feature to display box plots.")

else:
    st.info("No data to visualize. Please adjust filters in the sidebar.")

st.sidebar.info("Dashboard powered by Streamlit. Using the Iris dataset.")
