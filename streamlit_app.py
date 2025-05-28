import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Simulated sample data based on your screenshot
np.random.seed(42)
timestamps = pd.date_range("2025-04-27", periods=100, freq="H")
tags = ["SCHP_3382_Sgd", "SCHP_3381_Sgd"]

data = []
for tag in tags:
    for ts in timestamps:
        value = np.random.normal(loc=100, scale=10)
        spike = value > 115  # Spike condition
        data.append({
            "tagname": tag,
            "timestamp": ts,
            "value": value,
            "collectionoffset": np.random.randint(0, 100),
            "spikelogic": spike,
            "hiengineeringunits": "Nm3/hr",
            "hiscale": 120,
            "collectorcompression": "Standard",
            "collectorcompressiontimeout": 1000,
            "conditioncollectioncomparison": "OutOfRange",
            "conditioncollectionmarkers": spike
        })

df = pd.DataFrame(data)

# Streamlit app
st.set_page_config(page_title="ERF Air Flow Dashboard", layout="wide")
st.title("🌬️ ERF Air Flow Monitoring Dashboard")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📘 Overview", "📊 Visuals", "🚨 Alerts", "🧹 Data Prep"])

with tab1:
    st.header("Overview")
    st.markdown("""
    This dashboard monitors the **Air Flow System** at the ERF site using sensor readings.
    
    - Real-time flow metrics by tag
    - Spike detection using `spikelogic`
    - Engineering units: Nm3/hr
    """)

    st.write("Latest timestamp:", df['timestamp'].max())
    st.write("Sensors available:", df['tagname'].nunique())

with tab2:
    st.header("Air Flow Trends")
    selected_tags = st.multiselect("Select Sensors", df["tagname"].unique(), default=df["tagname"].unique())
    filtered = df[df["tagname"].isin(selected_tags)]

    fig = px.line(filtered, x="timestamp", y="value", color="tagname", title="Sensor Values Over Time")
    st.plotly_chart(fig, use_container_width=True)

    st.metric("Latest Value", f"{filtered['value'].iloc[-1]:.2f} Nm3/hr")

with tab3:
    st.header("Spike & Anomaly Alerts")

    alerts = df[df["spikelogic"] == True]
    st.warning(f"⚠️ {len(alerts)} spike events detected.")

    st.dataframe(alerts[["timestamp", "tagname", "value"]])

    csv = alerts.to_csv(index=False).encode()
    st.download_button("Download Alerts", csv, "airflow_alerts.csv", "text/csv")

with tab4:
    st.header("Data Preparation Documentation")
    st.markdown("""
    - **Null Handling**: N/A (data simulated)
    - **Spike Detection**: `value > 115`
    - **Engineering units**: All values are in Nm3/hr
    - **Transformations**: None applied yet
    """)

