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
# =====================
# PENJELASAN DASHBOARD (KONTEKS SKRIPSI)
# =====================
st.markdown("""
Dashboard ini digunakan sebagai media penyajian **Visualisasi dan Penjelasan Hasil Analisis Data** pada Bab IV (Hasil dan Pembahasan).

Struktur penyajian disesuaikan dengan kaidah penulisan skripsi Program Studi Sains Data, yang meliputi:
1. Analisis Univariat
2. Analisis Bivariat
3. Kategorisasi Variabel
4. Model Prediktif Regresi Linear
5. Uji Statistik Chi-Square

Seluruh visualisasi disajikan secara **statis**, sehingga hasil analisis bersifat konsisten, dapat direplikasi, dan mudah dikonversi menjadi tabel atau gambar dalam dokumen skripsi.
""")

filtered_df = df.copy()

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
        st.subheader("📈 Visualisasi dan Penjelasan Analisis Univariat")
        st.markdown("Distribusi tingkat kemiskinan antar provinsi.")
        fig1 = plt.figure(figsize=(6,4))
        ax1 = fig1.add_subplot(111)
        filtered_df['Kemiskinan_Persen'].plot.hist(bins=15, alpha=0.7, ax=ax1)
        ax1.set_xlabel("Persentase Kemiskinan")
        ax1.set_title("Distribusi Tingkat Kemiskinan per Provinsi")
        st.pyplot(fig1)

    with col2:
        st.subheader("📊 Visualisasi dan Penjelasan Analisis Bivariat")
        st.markdown("Rata-rata kemiskinan berdasarkan kategori akses internet.")
        fig2 = plt.figure(figsize=(6,4))
        ax2 = fig2.add_subplot(111)
        filtered_df.groupby('Internet_Kategori')['Kemiskinan_Persen'].mean().plot.bar(ax=ax2, alpha=0.8)
        ax2.set_ylabel("Rata-rata Kemiskinan (%)")
        ax2.set_title("Hubungan Akses Internet dan Tingkat Kemiskinan")
        st.pyplot(fig2)

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
        st.subheader("📋 Tabel Hasil Uji Chi-Square")
        st.markdown("Hubungan antara kategori akses internet dan tingkat kemiskinan.")
        contingency = pd.crosstab(filtered_df['Internet_Kategori'], filtered_df['Kemiskinan_Kategori'])
        chi2, p, dof, exp = chi2_contingency(contingency)
        st.dataframe(contingency)
        fig3 = plt.figure(figsize=(5,4))
        ax3 = fig3.add_subplot(111)
        im = ax3.imshow(contingency)
        ax3.set_xticks(range(len(contingency.columns)))
        ax3.set_yticks(range(len(contingency.index)))
        ax3.set_xticklabels(contingency.columns)
        ax3.set_yticklabels(contingency.index)
        ax3.set_title("Tabel Kontingensi Akses Internet dan Kemiskinan")
        plt.colorbar(im, ax=ax3)
        st.pyplot(fig3)
        st.markdown(f"**Chi-Square:** {chi2:.3f}  \
        **p-value:** {p:.4f}  \
        **df:** {dof}")

    with col4:
        st.subheader("📈 Visualisasi dan Penjelasan Model Prediktif Regresi Linear")
        st.markdown("Hubungan linear antara akses internet dan kemiskinan.")
        fig4 = plt.figure(figsize=(6,4))
        ax4 = fig4.add_subplot(111)
        ax4.scatter(filtered_df['Internet_Total'], filtered_df['Kemiskinan_Persen'], alpha=0.7)
        ax4.set_xlabel("Akses Internet (%)")
        ax4.set_ylabel("Kemiskinan (%)")
        ax4.set_title("Model Regresi Linear: Internet terhadap Kemiskinan")
        st.pyplot(fig4)

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
        st.subheader("📋 Tabel Kategorisasi Variabel")
        metadata = pd.DataFrame({
            'Variabel': ['Provinsi', 'Internet_Total', 'Kemiskinan_Persen'],
            'Tipe': ['Kategorikal', 'Numerik', 'Numerik'],
            'Deskripsi': [
                'Nama provinsi di Indonesia',
                'Persentase penduduk dengan akses internet',
                'Persentase penduduk miskin'
            ]
        })
        st.dataframe(metadata)

    with col6:
        st.subheader("📝 Ringkasan Hasil Analisis")
        if p < 0.05:
            st.success("Terdapat hubungan signifikan antara akses internet dan tingkat kemiskinan.")
        else:
            st.warning("Tidak terdapat hubungan signifikan antara akses internet dan tingkat kemiskinan.")
        st.markdown("""
        **Insight utama:**
        - Provinsi dengan akses internet lebih tinggi cenderung memiliki tingkat kemiskinan lebih rendah.

        **Catatan:**
        - Analisis menggunakan data agregat provinsi.
        - Chi-Square berbasis kategorisasi variabel kontinu.
        """)

st.caption("Dashboard Streamlit – EDA, Korelasi, dan Uji Chi-Square")("Dashboard Streamlit – Struktur Analisis EDA & Chi-Square")
