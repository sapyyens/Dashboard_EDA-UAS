import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import warnings
warnings.filterwarnings("ignore")

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(layout="wide", page_title="Dashboard EDA & Chi-Square")

st.markdown("## 📊 Dashboard Analisis EDA & Uji Chi-Square")
st.markdown("Dataset: Akses Internet dan Tingkat Kemiskinan per Provinsi")

# ======================================================
# LOAD DATA
# ======================================================
@st.cache_data
def load_data():
    return pd.read_csv("dataset_cleaned.csv")

df = load_data()

# ======================================================
# SIDEBAR (CONTROL PANEL)
# ======================================================
st.sidebar.markdown("### 🎛️ Panel Kontrol")

provinsi = st.sidebar.multiselect(
    "Pilih Provinsi",
    options=df['Provinsi'].unique(),
    default=df['Provinsi'].unique()
)

filtered_df = df[df['Provinsi'].isin(provinsi)]

# ======================================================
# PREPROCESSING (UNTUK CHI-SQUARE)
# ======================================================
filtered_df['Internet_Kategori'] = pd.cut(
    filtered_df['Internet_Total'],
    bins=[0, 80, 90, 100],
    labels=['Rendah', 'Sedang', 'Tinggi']
)

filtered_df['Kemiskinan_Kategori'] = pd.cut(
    filtered_df['Kemiskinan_Persen'],
    bins=[0, 5, 10, 100],
    labels=['Rendah', 'Sedang', 'Tinggi']
)

# ======================================================
# LAYOUT BARIS 1 (2 KOLOM)
# ======================================================
container1 = st.container()
col1, col2 = st.columns(2)

with container1:
    with col1:
        st.subheader("📈 EDA – Distribusi Data")
        st.markdown("Menampilkan distribusi variabel numerik utama dalam dataset.")
        # Histogram / Boxplot ditempatkan di sini

    with col2:
        st.subheader("📊 EDA – Perbandingan Kategori")
        st.markdown("Membandingkan rata-rata kemiskinan berdasarkan kategori akses internet.")
        # Bar chart kategori ditempatkan di sini

# ======================================================
# LAYOUT BARIS 2 (2 KOLOM)
# ======================================================
container2 = st.container()
col3, col4 = st.columns(2)

with container2:
    with col3:
        st.subheader("🧪 Uji Chi-Square")
        st.markdown("Menguji hubungan antara kategori akses internet dan tingkat kemiskinan.")
        # Tabel kontingensi + heatmap + nilai statistik

    with col4:
        st.subheader("🔗 Korelasi Variabel")
        st.markdown("Menampilkan hubungan linear antara variabel numerik.")
        # Scatter plot / correlation matrix

# ======================================================
# LAYOUT BARIS 3 (2 KOLOM)
# ======================================================
container3 = st.container()
col5, col6 = st.columns(2)

with container3:
    with col5:
        st.subheader("🗂️ Metadata Variabel")
        st.markdown("Informasi struktur dan definisi setiap variabel dalam dataset.")
        # Tabel metadata

    with col6:
        st.subheader("📝 Kesimpulan & Insight")
        st.markdown("Ringkasan hasil analisis statistik dan rekomendasi berbasis data.")
        # Interpretasi hasil

# ======================================================
st.caption("Dashboard Streamlit – Struktur Analisis EDA & Chi-Square")
