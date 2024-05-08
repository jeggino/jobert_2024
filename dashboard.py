import streamlit as st
import pandas as pd

from deta import Deta


# --- CONFIGURATION LAYOUT ---
st.set_page_config(
    page_title="dashboard_jobert_2024",
    page_icon="🗺️",
    initial_sidebar_state="collapsed",
    layout="wide",
    
)


st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
#GithubIcon {
  visibility: hidden;
}
</style> """, unsafe_allow_html=True)

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)




# --- CONNECT TO DETA ---
deta = Deta(st.secrets["deta_key"])
db_observations = deta.Base("df_observations")
db_survey = deta.Base("db_survey")
drive = deta.Drive("df_pictures")

# --- FUNCTIONS ---
# db_content_observations = pd.DataFrame(db_observations.fetch().items)
# db_content_surveys = pd.DataFrame(db_survey.fetch().items)

# project = st.selectbox("Project", ["Zaandam","Badhoevedorp"],key="project")
# db_content_observations = db_content_observations[db_content_observations["project"]==project]


# st.dataframe(data=db_content_observations, width=None, height=None, use_container_width=False, hide_index=True, column_order=None, column_config=None)
st.dataframe(data=db_content_surveys, width=None, height=None, use_container_width=False, hide_index=True, column_order=None, column_config=None)
