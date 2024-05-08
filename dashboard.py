import streamlit as st
import pandas as pd

from deta import Deta
import pydeck as pdk


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
db_survey = deta.Base("df_survey")
drive = deta.Drive("df_pictures")

db_content_observations = pd.DataFrame(db_observations.fetch().items)
db_content_surveys = pd.DataFrame(db_survey.fetch().items)

project = st.selectbox("Project", ["Zaandam","Badhoevedorp"],key="project")
db_content_observations = db_content_observations[db_content_observations["project"]==project]
db_content_surveys = db_content_surveys[db_content_surveys["Locatie"]==project]


st.dataframe(data=db_content_observations, width=None, height=None, use_container_width=True, hide_index=True, column_order=None, column_config=None)
st.dataframe(data=db_content_surveys, width=None, height=None, use_container_width=True, hide_index=True, column_order=None, column_config=None)


ICON_URL = {"verblijplaatz":"https://cdn2.iconfinder.com/data/icons/map-and-navigation-line-filled-1/154/Home_house_location_Map_and_Navigation-512.png",
            "forageren": "https://th.bing.com/th/id/OIP.xXDvwPQPQcgfpPEIkk2KEQHaHa?rs=1&pid=ImgDetMain",
            "Zwermen": "https://th.bing.com/th/id/R.f265b1bfdcf77d2cd550882c15bf7977?rik=RZGpl03FYAwWJQ&riu=http%3a%2f%2fwww.pngall.com%2fwp-content%2fuploads%2f2017%2f05%2fMap-Marker-PNG-Picture.png&ehk=wBDODeX2dBoxrTGgrpwu4xXzVNnUycDEZEY4PR1dy9k%3d&risl=&pid=ImgRaw&r=0",}

icon_data = {
    # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
    # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
    "url": ICON_URL["Zwermen"],
    # "width": 120,
    # "height": 120,
    # "anchorY": 125,
}

data = db_content_observations
# data["icon_data"] = data.apply(lambda x: ICON[x["sp"]] if ((x["soortgroup"]=="Vogels") & (x["functie"]!="nestlocatie")) 
#                                        else (ICON["Swift_nest"] if ((x["soortgroup"]=="Vogels") & (x["functie"]=="nestlocatie"))
#                                               else (ICON["Bat"] if x["soortgroup"]=="Vleermuizen"  
#                                                  else (ICON["Nest_bezet"] if x["onbewoond"]=="Ja" 
#                                                        else ICON["Nest_unbezet"]))), axis=1)
data["icon_data"] = None
for i in data.index:
    data["icon_data"][i] = icon_data
    
view = pdk.data_utils.compute_view(data[["lng", "lat"]])

icon_layer = pdk.Layer(
    type="IconLayer",
    data=data,
    get_icon="icon_data",
    get_size=4,
    size_scale=15,
    get_position=["lng", "lat"],
    pickable=True,
)

r = pdk.Deck(
    icon_layer,
    initial_view_state=view,
    tooltip={"text": "{sp}"},
    map_provider="mapbox",
    map_style=pdk.map_styles.SATELLITE,
)
st.pydeck_chart(r,use_container_width=True)
