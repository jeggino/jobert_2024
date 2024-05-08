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

DOEL = ["groepsvorming en zwermen laatvlieger","kraamperiode (1e avond)","kraamperiode (2e avond)","kraamperiode (1e ochtend)",
       "kraamperiode (2e en 3e ochtend)","kraamperiode (4e ochtend)","eind kraamperiode"]

GEBIED = ['P', 'O']

# --- FUNCTIONS ---
def load_dataset():
  return db.fetch().items

def insert_input(datum,gebied,doel,waarnemer):

  return db.put({"datum":str(datum),"gebied":gebied,"doel":doel,"waarnemer":waarnemer})

def stream_data():
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)

def get_elements(l):
    ret = []
    for elem in l:
        if type(elem) == list:
            ret.extend(get_elements(elem))
        else:
            ret.append(elem)
    return ret
        
# --- APP ---
# horizontal menu
selected = option_menu(None, ['✍️','📊','📋'], 
                       icons=None,
                       default_index=0,
                       orientation="horizontal",
                       )

if selected == '✍️':
    datum = st.date_input("Datum", datetime.datetime.today())
    gebied = st.selectbox('Gebied',GEBIED,key='area',placeholder="Kies een gebied...",index=None)
    doel = st.selectbox('Doel',DOEL,key='doel',placeholder="Kies een doel...",index=None)
    waarnemer = st.multiselect('Waarnemer(s)',['Luigi', 'Alko', 'Tobias'],key='waarnemer',placeholder="Kies voor een waarnemer...")
    
    submitted = st.button("Gegevens invoegen")
    
    if submitted:

        if len(waarnemer) == 0 or gebied==None or doel==None:
            st.warning("Vul het formulier in, alstublieft")
            st.stop()
    
        insert_input(datum,gebied,doel,waarnemer)
        st.write(f"Done!")
    
if selected == '📊':

    db_content = load_dataset()
    df = pd.DataFrame(db_content)
    df['img'] = "https://png.pngtree.com/png-clipart/20231021/original/pngtree-bat-face-illustration-png-image_13395424.png"

    tab1, tab2= st.tabs(["🔍", "🦸‍♂️"])


    chart = alt.Chart(df).mark_point(size=30,
        # opacity=0.8,
        # stroke='black',
        # strokeWidth=1,
        # strokeOpacity=0.4
    ).encode(
        alt.X('datum:T',axis=alt.Axis(grid=False,domain=True,ticks=False,),title=None, 
              scale=alt.Scale(domain=['2024','2025']))
        ,
        alt.Y('gebied:N',axis=alt.Axis(grid=False,domain=False,ticks=True,),sort=alt.EncodingSortField(field="gebied",  order='ascending'),title=None)
        ,
        url="img",
        tooltip=[
            alt.Tooltip("waarnemer:N"),
            alt.Tooltip("datum:T"),
            alt.Tooltip("gebied:N"),
            alt.Tooltip("doel:N"),
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
    
    # Add annotations
    ANNOTATIONS = [
        ("April 15, 2024", "Groepsvorming en zwermen laatvlieger"),
        ("May 15, 2024", "Kraamperiode (1e avond en 1e ochtend)"),
        ("June 15, 2024", "Kraamperiode (2e avond)"),
        ("June 1, 2024", "Kraamperiode (2e en 3e ochtend)"),
        ("July 1, 2024", "Kraamperiode (4e ochtend)"),
        ("July 15, 2024", "Eind kraamperiode"),
    ]
    annotations_df = pd.DataFrame(ANNOTATIONS, columns=["datum", "doel"])
    annotations_df.datum = pd.to_datetime(annotations_df.datum)
    

    
    rule = alt.Chart(annotations_df).mark_rule(color="red").encode(
        x="datum:T",
        tooltip=["doel"],
        color=alt.Color('doel:N').legend(None),
        size=alt.value(2),
    ).interactive()
    
    
    
    chart = chart  + rule

    tab1.altair_chart(chart, theme=None, use_container_width=True)
    
    waarnemer = df.waarnemer.to_list()
    data = Counter(get_elements(waarnemer))
    
    data_df = pd.DataFrame.from_dict(data, orient='index').rename(columns={0:"antaal"})
    
    tab2.data_editor(
        data_df,
        column_config={
                "antaal": st.column_config.ProgressColumn(
                    "Aantal werkdagen",
                    format="%f",
                    min_value=0,
                    max_value=30,
                ),
            },
        hide_index=False,
        use_container_width = True
    )

if selected == '📋':

    db_content = load_dataset()
    df = pd.DataFrame(db_content)
    df.drop("key",axis=1,inplace=True)
    
    st.data_editor(
        df,
        hide_index=True,
        use_container_width = True
    )
    

    st.download_button(
        label="Download data as CSV",
        data=df.to_csv(),
        file_name='df.csv',
        mime='text/csv',
    )

    
