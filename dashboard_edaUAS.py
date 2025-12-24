import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json

# =====================================================
# CONFIG
# =====================================================
st.set_page_config(
    page_title="Dashboard Kelompok 1 - EDA 2024",
    layout="wide"
)

# =====================================================
# LOAD GEOJSON
# =====================================================
@st.cache_data
def get_geojson():
    with open("38 Provinsi Indonesia - Provinsi.json", "r", encoding="utf-8") as f:
        return json.load(f)

# =====================================================
# LOAD DATA CSV
# =====================================================
@st.cache_data
def load_data():
    df = pd.read_csv("dataset_cleaned.csv")
    df.columns = df.columns.str.strip()

    # Standarisasi nama provinsi
    df["Prov_Match"] = (
        df["Provinsi"]
        .str.upper()
        .str.strip()
    )

    # 🔥 Mapping WAJIB mengikuti nama di GeoJSON
    mapping = {
        "DI YOGYAKARTA": "DAERAH ISTIMEWA YOGYAKARTA",
        "DAERAH KHUSUS IBUKOTA JAKARTA": "DKI JAKARTA",
        "KEPULAUAN RIAU": "KEP. RIAU",
        "KEPULAUAN BANGKA BELITUNG": "KEP. BANGKA BELITUNG",
        "PAPUA BARAT": "PAPUA BARAT DAYA",
    }

    df["Prov_Match"] = df["Prov_Match"].replace(mapping)

    return df

# =====================================================
# LOAD
# =====================================================
df = load_data()
geojson_data = get_geojson()

# =====================================================
# HEADER
# =====================================================
st.title("📈 Analisis Ketimpangan Digital di Indonesia 2024")

# =====================================================
# KPI
# =====================================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Rata-rata Kemiskinan", f"{df['Kemiskinan_Persen'].mean():.2f}%")
col2.metric("Rata-rata Akses Internet", f"{df['Internet_Total'].mean():.2f}%")
col3.metric("Korelasi (r)", "-0.8244", "Sangat Kuat")
col4.metric("R²", "0.6796")

st.divider()

# =====================================================
# VALIDASI (ANTI PETA PUTIH)
# =====================================================
geo_names = [f["properties"]["NAME_1"] for f in geojson_data["features"]]
assert df["Prov_Match"].isin(geo_names).all(), "❌ Nama provinsi tidak cocok dengan GeoJSON"

# =====================================================
# PETA CHOROPLETH
# =====================================================
st.subheader("📍 Peta Persebaran Akses Internet per Provinsi")

fig_map = px.choropleth(
    df,
    geojson=geojson_data,
    locations="Prov_Match",
    featureidkey="properties.NAME_1",
    color="Internet_Total",
    color_continuous_scale="RdYlGn",
    hover_name="Provinsi",
    labels={"Internet_Total": "Akses Internet (%)"}
)

fig_map.update_geos(
    fitbounds="locations",
    visible=False
)

fig_map.update_layout(
    margin=dict(r=0, t=0, l=0, b=0),
    height=520
)

st.plotly_chart(fig_map, use_container_width=True)

# =====================================================
# REGRESI
# =====================================================
st.divider()
c1, c2 = st.columns(2)

with c1:
    st.subheader("📉 Analisis Regresi Linear")

    x = df["Kemiskinan_Persen"]
    y = df["Internet_Total"]

    slope, intercept = np.polyfit(x, y, 1)
    line_x = np.array([x.min(), x.max()])
    line_y = slope * line_x + intercept

    fig_reg = px.scatter(
        df,
        x="Kemiskinan_Persen",
        y="Internet_Total",
        hover_name="Provinsi"
    )

    fig_reg.add_trace(
        go.Scatter(
            x=line_x,
            y=line_y,
            mode="lines",
            name="Regresi",
            line=dict(color="red")
        )
    )

    st.plotly_chart(fig_reg, use_container_width=True)
    st.info(f"**Model:** Y = {intercept:.2f} + {slope:.2f}X")

with c2:
    st.subheader("📊 Tabel Kontingensi (Chi-Square)")

    heatmap_data = pd.DataFrame(
        [[10, 2, 1],
         [3, 12, 2],
         [1, 2, 5]],
        index=[
            "Kemiskinan Rendah",
            "Kemiskinan Sedang",
            "Kemiskinan Tinggi"
        ],
        columns=[
            "Internet Rendah",
            "Internet Sedang",
            "Internet Tinggi"
        ]
    )

    fig_heat = px.imshow(
        heatmap_data,
        text_auto=True,
        color_continuous_scale="Blues"
    )

    st.plotly_chart(fig_heat, use_container_width=True)

# =====================================================
# RESIDUAL
# =====================================================
st.divider()
st.subheader("🎯 Analisis Residual Terstandarisasi")

res_df = pd.DataFrame({
    "Kategori Internet": ["Rendah", "Sedang", "Tinggi"],
    "Kemiskinan Rendah": ["1.442", "0.127", "1.710"],
    "Kemiskinan Tinggi": ["2.693", "-0.798", "-1.622"]
})

st.table(res_df)

st.warning(
    "Insight: Nilai **2.693** menunjukkan konsentrasi signifikan pada "
    "**Kemiskinan Tinggi – Internet Rendah**."
)
