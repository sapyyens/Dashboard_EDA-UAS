import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Dashboard Ketimpangan Digital 2024", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("dataset_cleaned.csv")
    # Pembersihan kolom (menghapus spasi jika ada)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# --- SIDEBAR (Filter) ---
st.sidebar.header("Filter Data")
selected_prov = st.sidebar.multiselect("Pilih Provinsi:", options=df['Provinsi'].unique(), default=df['Provinsi'].unique())
filtered_df = df[df['Provinsi'].isin(selected_prov)]

# --- HEADER ---
st.title("📊 Analisis Ketimpangan Kemiskinan & Akses Internet 2024")
st.markdown("Dashboard ini merepresentasikan hasil penelitian pada **Tugas Besar EDA Kelompok 1**.")

# --- ROW 1: KPI CARDS (Data Aktual) ---
avg_poverty = df['Kemiskinan_Persen'].mean()
avg_internet = df['Internet_Total'].mean()
correlation = df['Kemiskinan_Persen'].corr(df['Internet_Total'])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Rata-rata Kemiskinan", f"{avg_poverty:.2f}%")
col2.metric("Rata-rata Akses Internet", f"{avg_internet:.2f}%")
col3.metric("Korelasi (Pearson r)", f"{correlation:.4f}", delta_color="inverse")
col4.metric("Koefisien Determinasi (R²)", "0.6796")

st.divider()

# --- ROW 2: ANALISIS REGRESI ---
st.subheader("1. Analisis Regresi Linear (Pendekatan Numerik)")
c1, c2 = st.columns([2, 1])

with c1:
    fig_reg = px.scatter(filtered_df, x="Kemiskinan_Persen", y="Internet_Total", 
                         trendline="ols", trendline_color_override="red",
                         hover_name="Provinsi", 
                         labels={"Kemiskinan_Persen": "Kemiskinan (%)", "Internet_Total": "Akses Internet (%)"},
                         title="Tren Hubungan Kemiskinan vs Akses Internet")
    st.plotly_chart(fig_reg, use_container_width=True)

with c2:
    st.info("**Model Regresi:**")
    st.latex(r"Y = 108.05 - 1.95X")
    st.write(f"""
    **Interpretasi Utama:**
    Setiap kenaikan **1% tingkat kemiskinan** di sebuah provinsi, diprediksi akan menurunkan **akses internet sebesar 1.95%**.
    
    * **Kekuatan Hubungan:** Sangat Kuat (r = {correlation:.4f}).
    * **R-Squared:** 67.96% variasi akses internet dijelaskan oleh tingkat kemiskinan.
    """)

# --- ROW 3: TABEL KONTINGENSI & CHI-SQUARE ---
st.subheader("2. Analisis Chi-Square (Uji Signifikansi)")
c3, c4 = st.columns([1, 1])

with c3:
    # Data Heatmap berdasarkan hasil di Notebook/Skripsi
    heatmap_data = pd.DataFrame(
        [[10, 2, 1], [3, 12, 2], [1, 2, 5]], 
        index=['Rendah', 'Sedang', 'Tinggi'],
        columns=['Rendah', 'Sedang', 'Tinggi']
    )
    fig_heat = px.imshow(heatmap_data, 
                        labels=dict(x="Kategori Internet", y="Kategori Kemiskinan", color="Jumlah Provinsi"),
                        color_continuous_scale='RdBu_r', text_auto=True,
                        title="Tabel Kontingensi: Kemiskinan vs Internet")
    st.plotly_chart(fig_heat, use_container_width=True)

with c4:
    st.success("**P-Value: 0.001871**")
    st.markdown("""
    **Statistik Uji:**
    * **Chi-Square Stat:** 17.0731
    * **Cramer's V:** 0.4739 (Hubungan Kuat)
    
    **Kesimpulan:** H0 ditolak. Terdapat hubungan yang signifikan secara statistik antara tingkat kemiskinan dan akses internet antarprovinsi di Indonesia.
    """)

# --- ROW 4: ANALISIS RESIDUAL (POINT KRITIS SKRIPSI) ---
st.divider()
st.subheader("3. Analisis Residual Terstandarisasi")
st.write("Mengidentifikasi kelompok yang menjadi pemicu utama ketimpangan:")

res_df = pd.DataFrame({
    'Kategori Internet': ['Rendah', 'Sedang', 'Tinggi'],
    'Kemiskinan Rendah': ["1.442", "0.127", "1.710"],
    'Kemiskinan Sedang': ["-0.894", "0.667", "0.000"],
    'Kemiskinan Tinggi': ["2.693", "-0.798", "-1.622"]
})

# Highlight nilai kritis > 2
def highlight_cells(val):
    color = 'yellow' if val == "2.693" else 'white'
    return f'background-color: {color}'

st.table(res_df)

st.warning("""
**Temuan Penting untuk Skripsi:**
Sel **Kemiskinan Tinggi - Akses Internet Rendah** memiliki residual sebesar **2.693** (melebihi ambang batas ±2). 
Kelompok ini menyumbang **42.47%** terhadap total nilai Chi-Square, yang berarti ini adalah faktor utama yang memperkuat fenomena ketimpangan digital.
""")

# --- DATA TABLE ---
with st.expander("Lihat Data Mentah"):
    st.dataframe(filtered_df)

st.caption("Dashboard Tugas Besar EDA - Kelompok 1 - Sains Data UPNVJT")
