import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd
import altair as alt

import datetime

from deta import Deta

from collections import Counter

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

def insert_input(datum,t_1,t_2,Locatie,temp,Weersomstandigheden,rapport):

  return db.put({"datum":str(datum),"t_1":t_1,"t_2":t_2,"Locatie":Locatie,"temp":temp,"Weersomstandigheden":Weersomstandigheden,"rapport":rapport})

        
# --- APP ---
datum = st.date_input("Datum", datetime.datetime.today())
t_1 = st.time_input("begintijd invoegen", value=None,key="t_1")
t_2 = st.time_input("eindtijd invoegen", value=None,key="t_2")
locatie = st.selectbox('LOCATIE',LOCATIE,key='LOCATIE',placeholder="Kies een locatie...",index=None)
Weersomstandigheden = st.selectbox('Weersomstandigheden',Weersomstandigheden,key='Weersomstandigheden',placeholder="Vul de weeromstandigheden in...",index=None)
temp = number = st.number_input("Temperatuur", value=None, placeholder="Voer de temperatuur in...")
rapport = st.text_input("Voeg een dagrapport toe", "")

submitted = st.button("Gegevens invoegen")

if submitted:

    if len(waarnemer) == 0 or gebied==None or doel==None:
        st.warning("Vul het formulier in, alstublieft")
        st.stop()

    insert_input(datum,t_1,t_2,Locatie,temp,Weersomstandigheden,rapport)
    st.write(f"Done!")
