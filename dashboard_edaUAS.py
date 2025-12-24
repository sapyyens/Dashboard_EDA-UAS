import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIG ---
st.set_page_config(page_title="Dashboard Kelompok 1 - EDA 2024", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("dataset_cleaned.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# --- HEADER ---
st.title("📈 Analisis Ketimpangan Digital di Indonesia 2024")
st.markdown("""
Dashboard ini menyajikan hasil penelitian mengenai hubungan **Tingkat Kemiskinan** terhadap **Akses Internet** antarprovinsi di Indonesia. Data bersumber dari BPS 2024.
""")

# --- ROW 1: KPI CARDS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Rata-rata Kemiskinan", f"{df['Kemiskinan_Persen'].mean():.2f}%")
col2.metric("Rata-rata Akses Internet", f"{df['Internet_Total'].mean():.2f}%")
col3.metric("Korelasi (r)", "-0.8244", "Sangat Kuat")
col4.metric("Koefisien Determinasi (R²)", "0.6796")

st.divider()

# --- ROW 2: PETA INDONESIA (CHOROPLETH) ---
st.subheader("📍 Peta Persebaran Akses Internet per Provinsi")
geojson_url = "https://raw.githubusercontent.com/superpau/indonesia-geojson/master/indonesia-province.json"

fig_map = px.choropleth(
    df,
    geojson=geojson_url,
    locations='Provinsi',
    featureidkey="properties.NAME_1",
    color='Internet_Total',
    color_continuous_scale="RdYlGn",
    labels={'Internet_Total': 'Akses Internet (%)'},
    hover_name='Provinsi'
)
fig_map.update_geos(fitbounds="locations", visible=False)
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=500)
st.plotly_chart(fig_map, use_container_width=True)

# --- ROW 3: REGRESI & CHI-SQUARE ---
st.divider()
c1, c2 = st.columns(2)

with c1:
    st.subheader("📉 Analisis Regresi Linear")
    fig_reg = px.scatter(df, x="Kemiskinan_Persen", y="Internet_Total", 
                         trendline="ols", trendline_color_override="red",
                         hover_name="Provinsi",
                         labels={"Kemiskinan_Persen": "Kemiskinan (%)", "Internet_Total": "Akses Internet (%)"})
    st.plotly_chart(fig_reg, use_container_width=True)
    st.info("**Model:** $Y = 108.05 - 1.95X$")

with c2:
    st.subheader("📊 Tabel Kontingensi (Chi-Square)")
    # Data sesuai hasil perhitungan di notebook
    heatmap_data = pd.DataFrame(
        [[10, 2, 1], [3, 12, 2], [1, 2, 5]], 
        index=['Rendah', 'Sedang', 'Tinggi'],
        columns=['Rendah', 'Sedang', 'Tinggi']
    )
    fig_heat = px.imshow(heatmap_data, text_auto=True, color_continuous_scale='Blues',
                         labels=dict(x="Akses Internet", y="Kemiskinan"))
    st.plotly_chart(fig_heat, use_container_width=True)
    st.success("**P-Value: 0.001871** (Hubungan Signifikan)")

# --- ROW 4: RESIDUAL TERSTANDARISASI (TEMUAN KRITIS) ---
st.divider()
st.subheader("🎯 Temuan Kritis: Analisis Residual")
st.write("Kelompok provinsi yang paling berkontribusi terhadap ketimpangan:")

res_df = pd.DataFrame({
    'Kategori Internet': ['Rendah', 'Sedang', 'Tinggi'],
    'Kemiskinan Rendah': ["1.442", "0.127", "1.710"],
    'Kemiskinan Sedang': ["-0.894", "0.667", "0.000"],
    'Kemiskinan Tinggi': ["2.693", "-0.798", "-1.622"]
})

st.table(res_df)

st.warning("""
**Insight Skripsi:** Nilai residual **2.693** pada kelompok **Kemiskinan Tinggi & Internet Rendah** menandakan ketimpangan digital yang sangat nyata. Kelompok ini menyumbang **42.47%** terhadap total nilai Chi-Square.
""")

st.caption("Dikembangkan oleh Kelompok 1 - Sains Data UPNVJT")
