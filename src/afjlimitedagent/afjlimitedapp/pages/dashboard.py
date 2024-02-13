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
    return df

df = get_data()


st.markdown("# Dashboard page 📊")
st.sidebar.markdown("# Dashboard page 📊")

# top-level filters
job_filter = st.selectbox("Select the Condition", pd.unique(df["condition"]))

# creating a single-element container
placeholder = st.empty()

df = df[df["condition"] == job_filter]

with placeholder.container():

        # # create three columns
        # kpi1, kpi2, kpi3 = st.columns(3)

        # # fill in those three columns with respective metrics or KPIs
        # kpi1.metric(
        #     label="Age ⏳",
        #     value=round(avg_age),
        #     delta=round(avg_age) - 10,
        # )
        
        # kpi2.metric(
        #     label="Married Count 💍",
        #     value=int(count_married),
        #     delta=-10 + count_married,
        # )
        
        # kpi3.metric(
        #     label="A/C Balance $",
        #     value=f"$ {round(balance,2)} ",
        #     delta=-round(balance / count_married) * 100,
        # )

        # # create two columns for charts
        # fig_col1, fig_col2 = st.columns(2)
        # with fig_col1:
        #     st.markdown("### First Chart")
        #     fig = px.density_heatmap(
        #         data_frame=df, y="age_new", x="marital"
        #     )
        #     st.write(fig)
            
        # with fig_col2:
        #     st.markdown("### Second Chart")
        #     fig2 = px.histogram(data_frame=df, x="age_new")
        #     st.write(fig2)

        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)

# chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

# st.bar_chart(chart_data)

# import streamlit as st
# import pandas as pd
# import numpy as np

# chart_data = pd.DataFrame(
#    {
#        "col1": list(range(20)) * 3,
#        "col2": np.random.randn(60),
#        "col3": ["A"] * 20 + ["B"] * 20 + ["C"] * 20,
#    }
# )

# st.bar_chart(chart_data, x="col1", y="col2", color="col3")