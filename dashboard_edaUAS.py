import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json

# --- CONFIG ---
st.set_page_config(page_title="Dashboard Analisis Kelompok 1", layout="wide")

# --- LOAD DATA & GEOJSON ---
@st.cache_data
def load_data():
    # Load CSV
    df = pd.read_csv("dataset_cleaned.csv")
    df.columns = df.columns.str.strip()
    
    # Normalisasi Nama Provinsi di CSV agar cocok dengan GeoJSON
    # Menghapus spasi berlebih dan merubah ke UPPERCASE
    df['Provinsi_Match'] = df['Provinsi'].str.strip().str.upper()
    
    # Penyesuaian nama khusus jika ada perbedaan (Mapping)
    mapping = {
        "DI YOGYAKARTA": "DAERAH ISTIMEWA YOGYAKARTA",
        "DKI JAKARTA": "DAERAH KHUSUS IBUKOTA JAKARTA",
        "PABUA": "PAPUA" # Contoh jika ada typo di CSV
    }
    df['Provinsi_Match'] = df['Provinsi_Match'].replace(mapping)
    return df

@st.cache_data
def load_geojson():
    with open("38 Provinsi Indonesia - Provinsi.json", "r") as f:
        return json.load(f)

df = load_data()
geojson_data = load_geojson()

if not df.empty:
    # --- HEADER ---
    st.title("📈 Dashboard Ketimpangan Digital Indonesia 2024")
    st.markdown("Menggunakan data spasial 38 Provinsi Indonesia.")

    # --- ROW 1: KPI CARDS ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rata-rata Kemiskinan", f"{df['Kemiskinan_Persen'].mean():.2f}%")
    col2.metric("Rata-rata Akses Internet", f"{df['Internet_Total'].mean():.2f}%")
    col3.metric("Korelasi (r)", "-0.8244")
    col4.metric("R-Square", "0.6796")

    st.divider()

    # --- ROW 2: MAP & REGRESI ---
    c1, c2 = st.columns([1.2, 1])

    with c1:
        st.subheader("📍 Peta Akses Internet per Provinsi")
        
        fig_map = px.choropleth(
            df,
            geojson=geojson_data,
            locations='Provinsi_Match', # Kolom yang sudah dinormalisasi
            featureidkey="properties.NAME_1", # Pastikan key ini ada di file JSON kamu
            color='Internet_Total',
            color_continuous_scale="RdYlGn",
            labels={'Internet_Total': 'Internet (%)'},
            hover_name='Provinsi'
        )
        fig_map.update_geos(fitbounds="locations", visible=False)
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=450)
        st.plotly_chart(fig_map, use_container_width=True)

    with c2:
        st.subheader("📉 Tren Regresi Linear")
        x = df["Kemiskinan_Persen"]
        y = df["Internet_Total"]
        slope, intercept = np.polyfit(x, y, 1)
        x_range = np.linspace(x.min(), x.max(), 100)
        y_range = intercept + slope * x_range

        fig_reg = px.scatter(df, x="Kemiskinan_Persen", y="Internet_Total", hover_name="Provinsi")
        fig_reg.add_trace(go.Scatter(x=x_range, y=y_range, mode='lines', name='Trendline', line=dict(color='red')))
        fig_reg.update_layout(height=450)
        st.plotly_chart(fig_reg, use_container_width=True)
        st.info(f"**Persamaan:** $Y = {intercept:.2f} {slope:.2f}X$")

    # --- ROW 3: TABEL KONTINGENSI & RESIDUAL ---
    st.divider()
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("📊 Tabel Kontingensi")
        heatmap_data = pd.DataFrame(
            [[10, 2, 1], [3, 12, 2], [1, 2, 5]], 
            index=['Rendah', 'Sedang', 'Tinggi'],
            columns=['Rendah', 'Sedang', 'Tinggi']
        )
        fig_heat = px.imshow(heatmap_data, text_auto=True, color_continuous_scale='Blues')
        st.plotly_chart(fig_heat, use_container_width=True)

    with c4:
        st.subheader("🎯 Analisis Residual")
        res_df = pd.DataFrame({
            'Kategori Internet': ['Rendah', 'Sedang', 'Tinggi'],
            'Kemiskinan Rendah': ["1.442", "0.127", "1.710"],
            'Kemiskinan Tinggi': ["2.693", "-0.798", "-1.622"]
        })
        st.table(res_df)
        st.warning("⚠️ **Insight:** Nilai **2.693** menunjukkan ketimpangan pada Kemiskinan Tinggi - Internet Rendah.")

else:
    st.error("Data CSV kosong atau tidak ditemukan.")
