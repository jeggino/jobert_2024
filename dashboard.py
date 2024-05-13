import streamlit as st
from streamlit_option_menu import option_menu

import folium
from folium.plugins import Draw, Fullscreen, LocateControl, GroupedLayerControl
from streamlit_folium import st_folium

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

# --- COSTANT ---
ICON = {"Gierzwaluw":"https://cdn-icons-png.flaticon.com/128/732/732126.png",
        "Huismus":"https://cdn-icons-png.flaticon.com/128/8531/8531874.png",
        "Bat": "https://cdn-icons-png.flaticon.com/128/2250/2250418.png",
        "Nest_bezet": "icons/bat_bow_full.jpg",
        "Nest_unbezet": "icons/bat_box_empty.jpg",
        "Swift_nest": "icons/swift_nest.jpg"}

ICON_SIZE = (18,18)


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

selected = option_menu(None, ['🗒️ Werkblad','🗺️ Kaart','📷 media'], 
                       icons=None,
                       default_index=0,
                       orientation="horizontal",
                       )

if selected == '🗒️ Werkblad':
    
    st.dataframe(data=db_content_surveys, use_container_width=True, hide_index=True, column_order=["datum","t_1","t_2","Weersomstandigheden","rapport"], column_config=None)
    


elif selected == '🗺️ Kaart':
    # ICON_URL = {"verblijplaatz":"https://cdn2.iconfinder.com/data/icons/map-and-navigation-line-filled-1/154/Home_house_location_Map_and_Navigation-512.png",
    #             "forageren": "https://th.bing.com/th/id/OIP.xXDvwPQPQcgfpPEIkk2KEQHaHa?rs=1&pid=ImgDetMain",
    #             "Zwermen": "https://th.bing.com/th/id/R.fa1d67352a0b44b7a2ac3c07809b2777?rik=i%2bEbns2Dii9E0A&riu=http%3a%2f%2fcdn.onlinewebfonts.com%2fsvg%2fimg_412341.png&ehk=z3kw3bKlhHt92TZ8t6XG6ufo6UoGTKO%2bBFTZC0cM1Cg%3d&risl=&pid=ImgRaw&r=0",}
    
    # icon_data = {
    #     "url": ICON_URL["Zwermen"],
    #     "width": 250,
    #     "height": 250,
    #     "anchorY": 125,
    # }
    
    # data = db_content_observations
    # data["icon_data"] = None
    # for i in data.index:
    #     data["icon_data"][i] = icon_data
        
    # view = pdk.data_utils.compute_view(data[["lng", "lat"]])
    
    # icon_layer = pdk.Layer(
    #     type="IconLayer",
    #     data=data,
    #     get_icon="icon_data",
    #     get_size=2,
    #     size_scale=15,
    #     get_position=["lng", "lat"],
    #     pickable=True,
    # )
    
    # r = pdk.Deck(
    #     icon_layer,
    #     initial_view_state=view,
    #     tooltip={"text": "{sp}"},
    #     map_provider="mapbox",
    #     map_style=pdk.map_styles.SATELLITE,
    # )
    
    # st.pydeck_chart(r,use_container_width=True)
    try:

            
        df_2 = db_content_observations
        
        df_2["icon_data"] = df_2.apply(lambda x: ICON[x["sp"]] if ((x["soortgroup"]=="Vogels") & (x["functie"]!="nestlocatie")) 
                                       else (ICON["Swift_nest"] if ((x["soortgroup"]=="Vogels") & (x["functie"]=="nestlocatie"))
                                              else (ICON["Bat"] if x["soortgroup"]=="Vleermuizen"  
                                                 else (ICON["Nest_bezet"] if x["onbewoond"]=="Ja" 
                                                       else ICON["Nest_unbezet"]))), axis=1)

        df_2 
        
        
        map = folium.Map()
        LocateControl(auto_start=True).add_to(map)
        Fullscreen().add_to(map)
        
        fg = folium.FeatureGroup(name="Vleermuiskast")
        fg_2 = folium.FeatureGroup(name="Huismussen")
        fg_4 = folium.FeatureGroup(name="Gierzwaluwen")
        fg_3 = folium.FeatureGroup(name="Vleermuizen")
        map.add_child(fg)
        map.add_child(fg_2)
        map.add_child(fg_4)
        map.add_child(fg_3)
        folium.TileLayer(tiles="CartoDB Positron",overlay=False,show=False).add_to(map)
        folium.LayerControl().add_to(map)
       
    
        
        
        for i in range(len(df_2)):
    
            if df_2.iloc[i]['geometry_type'] == "Point":
    
                html = popup_html(i)
                popup = folium.Popup(folium.Html(html, script=True), max_width=300)
    
                if df_2.iloc[i]['soortgroup'] == "Vleermuiskast":
                    folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']],
                                  popup=popup,
                                  icon=folium.features.CustomIcon(df_2.iloc[i]["icon_data"], icon_size=ICON_SIZE)).add_to(fg)
    
                elif df_2.iloc[i]['soortgroup'] == "Vogels":
                    if df_2.iloc[i]['sp'] == "Huismus":
                        
                        folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']],
                                      popup=popup,
                                      icon=folium.features.CustomIcon(df_2.iloc[i]["icon_data"], icon_size=ICON_SIZE)).add_to(fg_2)
                        
                    elif df_2.iloc[i]['sp'] == "Gierzwaluw":
                        
                        folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']],
                                      popup=popup,
                                      icon=folium.features.CustomIcon(df_2.iloc[i]["icon_data"], icon_size=ICON_SIZE)).add_to(fg_4)
    
    
                else:
                    folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']],
                                  popup=popup,
                                  icon=folium.features.CustomIcon(df_2.iloc[i]["icon_data"], icon_size=ICON_SIZE)).add_to(fg_3)
                    
    
            elif df_2.iloc[i]['geometry_type'] == "LineString":
    
                folium.PolyLine(df_2.iloc[i]['coordinates']).add_to(fg)

    except:
        st.warning("problems")


elif selected == '📷 media':

    tab1, tab2 = st.tabs(["🎞️","📂"])

    with tab1:
        uploaded_file = st.file_uploader("Choose a file")
        try:
            st.image(uploaded_file, caption='Sunrise by the mountains')
        
            submitted = st.button("Gegevens opslaan")
            if submitted:          
                bytes_data = uploaded_file.getvalue()
                drive.put(uploaded_file.name, data=bytes_data)
                st.rerun()
    
        except:
            st.warning("upload a file")

    with tab2:    
        try:
            for file in drive.list()["names"]:
                res = drive.get(file).read()
                st.image(res)
        except:
            st.warning("no files")
