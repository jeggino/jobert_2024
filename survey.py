import streamlit as st

import pandas as pd
import datetime

from deta import Deta

# --- CONFIGURATION ---
st.set_page_config(
    page_title="jobert_2024_survey",
    page_icon="🦇",
    layout="wide",
    
)

# --- CONNECT TO DETA ---
deta = Deta(st.secrets["deta_key"])
db = deta.Base("df_survey")

# --- COSTANTS ---

LOCATIE = ["Zaandam","Badhoevedorp"]

Weersomstandigheden = ['Zonnig', 'Bewolkt', 'Lichte regen']

# --- FUNCTIONS ---
def load_dataset():
  return db.fetch().items

def insert_input(datum,t_1,t_2,locatie,temp,weersomstandigheden,rapport):

  return db.put({"datum":str(datum),"t_1":t_1,"t_2":t_2,"Locatie":locatie,"temp":temp,"Weersomstandigheden":weersomstandigheden,"rapport":rapport})

        
# --- APP ---
datum = st.date_input("Datum", datetime.datetime.today())
t_1 = st.time_input("begintijd invoegen", value=None,key="t_1")
t_2 = st.time_input("eindtijd invoegen", value=None,key="t_2")
locatie = st.selectbox('LOCATIE',LOCATIE,key='LOCATIE',placeholder="Kies een locatie...",index=None)
weersomstandigheden = st.selectbox('Weersomstandigheden',Weersomstandigheden,key='Weersomstandigheden',placeholder="Vul de weeromstandigheden in...",index=None)
temp = st.number_input("Temperatuur", value=None, placeholder="Voer de temperatuur in...")
rapport = st.text_input("Voeg een dagrapport toe", "")
"---"
st.write(datum)
st.write(t_1)
st.write(t_2)
st.write(locatie)
st.write(weersomstandigheden)
st.write(temp)
st.write(rapport)

submitted = st.button("Gegevens invoegen")

if submitted:

    if len(locatie) == 0 or t_1==None or t_2==None or temp==None:
        st.warning("Vul het formulier in, alstublieft")
        st.stop()

    insert_input(datum,t_1,t_2,locatie,temp,weersomstandigheden,rapport)
    st.write(f"Done!")
