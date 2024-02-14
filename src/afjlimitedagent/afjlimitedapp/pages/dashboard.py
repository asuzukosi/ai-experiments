import time 
import streamlit as st 
import plotly.express as px
import pandas as pd
import numpy as np
from ingest_data import DATA_DIRECTORY, load_dataset, postprocess_dataset

# read csv from a URL
@st.cache_data
def get_data() -> pd.DataFrame:
    df = load_dataset(DATA_DIRECTORY)
    df = postprocess_dataset(df)
    sources = pd.unique(df["source"])
    destinations = pd.unique(df["destination"])
    
    df = pd.concat([df, df])
    dfs = np.array_split(df, 100)
    return dfs, sources, destinations

dfs, sources, destinations = get_data()


st.markdown("# Dashboard page 📊")
st.sidebar.markdown("# Dashboard page 📊")


df = dfs[0]

 # top-level filters
source_filter = st.selectbox("Select the Source", sources)
destination_filter = st.selectbox("Select the Source", destinations)


placeholder = st.empty()



old_avg_ect =  0
old_avg_erpm = 0
old_avg_vs = 0


for i in range(1, 100):
    df = pd.concat([df, dfs[i]])
    
    with placeholder.container():
        # creating a single-element container
        df = df[df["source"] == source_filter]
        df = df[df["destination"] == destination_filter]
        
        new_avg_ect = np.mean(df["Engine Coolant Temperature [°C]"])
        new_avg_erpm  = np.mean(df["Engine RPM [RPM]"])
        new_avg_vs = np.mean(df["Vehicle Speed Sensor [km/h]"])
         # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs
        kpi1.metric(
            label="Avg. Engine Coolant Temperature",
            value=round(new_avg_ect),
            delta=round(new_avg_ect - old_avg_ect),
        )
        
        kpi2.metric(
            label="Avg. Engine RPM",
            value=round(new_avg_erpm),
            delta=-round(new_avg_erpm - old_avg_erpm),
        )
        
        kpi3.metric(
            label="Avg. Vehicle Speed",
            value=round(new_avg_vs),
            delta=-round(new_avg_vs - old_avg_vs),
        )

        # create two columns for charts
        fig_col2 = st.columns(1)[0]
        # with fig_col1:
        #     st.markdown("### First Chart")
        #     fig = px.density_heatmap(
        #         data_frame=df, y="age_new", x="marital"
        #     )
        #     st.write(fig)
            
        with fig_col2:
            st.markdown("### Vehicle speed per condition")
            fig2 = px.histogram(data_frame=df, x="condition")
            st.write(fig2)

        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)
        
        old_avg_erpm = new_avg_erpm
        old_avg_ect = old_avg_ect
        old_avg_vs = new_avg_vs
        

