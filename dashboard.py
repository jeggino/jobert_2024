import streamlit as st
from streamlit_option_menu import option_menu

import folium
from folium.plugins import Fullscreen, LocateControl
from streamlit_folium import st_folium

import pandas as pd
import random
import altair as alt

from deta import Deta





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

OUTPUT_height = 800
OUTPUT_width = 1050
ICON_SIZE = (18,18)
ZOOM = 20

# --- FUNCTIONS ---
def password_generator():
    password_length = 12

    characters = "abcde12345"

    password = ""   

    for index in range(password_length):
        password = password + random.choice(characters)
        
    return password

def insert_info(pict_name,info):

  return db_infopictures.put({"pict_name":pict_name,"info":info})
    
def popup_html(row):
    
    i = row
     
    datum=df_2['datum'].iloc[i] 
    soortgroup=df_2['soortgroup'].iloc[i]
    sp = df_2['sp'].iloc[i] 
    functie=df_2['functie'].iloc[i]
    gedrag=df_2['gedrag'].iloc[i]
    verblijf=df_2['verblijf'].iloc[i]
    bewoond=df_2['onbewoond'].iloc[i] 
    opmerking=df_2['opmerking'].iloc[i]
    aantal=df_2['aantal'].iloc[i]
    waarnemer=df_2['waarnemer'].iloc[i] 
       

    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"
    
    html = """<!DOCTYPE html>
    <html>
    <table style="height: 126px; width: 300;">
    <tbody>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Datum</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(datum) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Soortgroup</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(soortgroup) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Soort</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(sp) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Functie</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(functie) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Gedrag</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(gedrag) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Bewoond</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(bewoond) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Opmerking</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(opmerking) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Aantal</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(aantal) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Waarnemer</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(waarnemer) + """
    </tr>
    </tbody>
    </table>
    </html>
    """
    return html


# --- CONNECT TO DETA ---
deta = Deta(st.secrets["deta_key"])
db_observations = deta.Base("df_observations")
db_survey = deta.Base("df_survey")
db_infopictures = deta.Base("df_infopictures")
drive = deta.Drive("df_pictures")

db_content_observations = pd.DataFrame(db_observations.fetch().items)
db_content_surveys = pd.DataFrame(db_survey.fetch().items)
db_content_infopictures = pd.DataFrame(db_infopictures.fetch().items)

project = st.selectbox("Opdracht", ["Zaandam","Badhoevedorp"], key="project")

try:
    
    db_surveys_filtered = db_content_surveys[db_content_surveys["Locatie"]==project]
    db_observations_filtered = db_content_observations[db_content_observations["project"]==project]
    
except:
    st.warning("Nog geen waarnemingen")
    st.stop()


selected = option_menu(None, ['🗒️ Werkblad','🗺️ Kaart','📷 media'], 
                       icons=None,
                       default_index=0,
                       orientation="horizontal",
                       )

if selected == '🗒️ Werkblad':

    tab1, tab2= st.tabs(["🗒️", "📈"])
    
    tab1.dataframe(data=db_surveys_filtered, use_container_width=True, hide_index=True, 
                 column_order=["Datum","Moment","Starttijd","Eindtijd","Laagste temperatuur","Weersomstandigheden","rapport"], 
                 column_config=None)

        
    chart = alt.Chart(db_surveys_filtered).mark_point(size=30,
        opacity=0.8,
        stroke='black',
        strokeWidth=1,
        strokeOpacity=0.4
    ).encode(
        alt.X('Datum:T',axis=alt.Axis(grid=False,domain=True,ticks=False,),title=None, 
              scale=alt.Scale(domain=['2024','2025']))
        ,
        alt.Y('Moment:N',axis=alt.Axis(grid=False,domain=False,ticks=True,),sort=alt.EncodingSortField(field="Moment",  order='ascending'),title=None)
        ,
        tooltip=[
            alt.Tooltip("Moment"),
            alt.Tooltip("Datum:T"),
            alt.Tooltip("Starttijd"),
            alt.Tooltip("Eindtijd"),
            alt.Tooltip("Laagste temperatuur"),
            alt.Tooltip("Weersomstandigheden"),
        ],
    ).properties(
        width=450,
        height=300,
        title=alt.Title(
            text="",
            subtitle="",
            anchor='start'
        )
    )
    
    
    tab2.altair_chart(chart, theme=None, use_container_width=True)
    


elif selected == '🗺️ Kaart':

    try:
            
        df_2 = db_observations_filtered
        
        df_2["icon_data"] = df_2.apply(lambda x: ICON[x["sp"]] if ((x["soortgroup"]=="Vogels") & (x["functie"]!="nestlocatie")) 
                                       else (ICON["Swift_nest"] if ((x["soortgroup"]=="Vogels") & (x["functie"]=="nestlocatie"))
                                              else (ICON["Bat"] if x["soortgroup"]=="Vleermuizen"  
                                                 else (ICON["Nest_bezet"] if x["onbewoond"]=="Ja" 
                                                       else ICON["Nest_unbezet"]))), axis=1)

        
        
        map = folium.Map(zoom_start = ZOOM,location=(df_2["lat"].mean(), df_2["lng"].mean()))
        Fullscreen().add_to(map)
        
        fg_2 = folium.FeatureGroup(name="Huismussen")
        fg_4 = folium.FeatureGroup(name="Gierzwaluwen")
        fg_3 = folium.FeatureGroup(name="Vleermuizen")
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

        st_folium(map,
                  width=OUTPUT_width, height=OUTPUT_height,
                  feature_group_to_add=[fg_2,fg_3,fg_4])

    except:
        st.warning("Nog geen waarnemingen")


elif selected == '📷 media':

    tab1, tab2 = st.tabs(["🎞️","📂"])

    with tab1:    
        try:
            for file in drive.list()["names"]:
                res = drive.get(file).read()
                st.image(res)
                st.write(db_content_infopictures.loc[db_content_infopictures["pict_name"]==file,"info"].iloc[0])
                "---"
        except:
            st.warning("Nog geen foto's")

    with tab2:
        
        with st.form("my_form",clear_on_submit=True):
            uploaded_file = st.file_uploader("Een afbeelding uploaded",label_visibility="hidden")
            try:
                st.image(uploaded_file)
                info = st.text_input("Schrijf wat informatie over de foto...", "")
            
                submitted = st.form_submit_button("Gegevens opslaan")
                if submitted:
                    pict_name = password_generator()
                    bytes_data = uploaded_file.getvalue()
                    drive.put(f"{pict_name}", data=bytes_data)
                    insert_info(pict_name,info)
            except:
                st.stop()
