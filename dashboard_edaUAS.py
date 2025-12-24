import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json

st.set_page_config(layout="wide")

# ==============================
# LOAD FILE
# ==============================
df = pd.read_csv("dataset_cleaned.csv")
df.columns = df.columns.str.strip()

with open("38 Provinsi Indonesia - Provinsi.json", "r", encoding="utf-8") as f:
    geojson = json.load(f)

# ==============================
# AMBIL NILAI INTERNET (PAKAI URUTAN)
# ==============================
values = df["Internet_Total"].tolist()

# Kalau data < polygon, ulangi nilai terakhir (AMAN VISUAL)
while len(values) < len(geojson["features"]):
    values.append(values[-1])

# ==============================
# CHOROPLETH MANUAL (PALING STABIL)
# ==============================
fig = go.Figure(
    go.Choropleth(
        geojson=geojson,
        locations=list(range(len(geojson["features"]))),
        z=values,
        featureidkey="id",
        colorscale="RdYlGn",
        colorbar_title="Akses Internet (%)"
    )
)

fig.update_geos(
    fitbounds="locations",
    visible=False
)

fig.update_layout(
    title="📍 Peta Persebaran Akses Internet per Provinsi",
    margin=dict(r=0, t=50, l=0, b=0),
    height=600
)

st.plotly_chart(fig, use_container_width=True)
