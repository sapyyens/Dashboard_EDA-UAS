import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

st.set_page_config(page_title="Dashboard Analisis Chi-Square", layout="wide")

st.title("📊 Dashboard Analisis Chi-Square & EDA")
st.markdown("Dashboard interaktif untuk eksplorasi data, uji Chi-Square, korelasi, dan insight analitis")

# =====================
# LOAD DATA
# =====================
@st.cache_data
def load_data():
    # Sesuaikan dengan dataset final hasil EDA kamu
    return pd.read_csv("dataset_cleaned.csv")

df = load_data()

# =====================
# SIDEBAR FILTER
# =====================
st.sidebar.header("Filter Data")

provinsi = st.sidebar.multiselect(
    "Provinsi",
    options=df['Provinsi'].unique(),
    default=df['Provinsi'].unique()
)

tahun = st.sidebar.multiselect(
    "Tahun",
    options=df['Tahun'].unique(),
    default=df['Tahun'].unique()
)

filtered_df = df[(df['Provinsi'].isin(provinsi)) & (df['Tahun'].isin(tahun))]

# =====================
# GRID 3x2 LAYOUT
# =====================
row1_col1, row1_col2, row1_col3 = st.columns(3)
row2_col1, row2_col2, row2_col3 = st.columns(3)

# =====================
# 1. EDA - DISTRIBUSI
# =====================
with row1_col1:
    st.subheader("EDA – Distribusi")
    fig, ax = plt.subplots()
    filtered_df['Jumlah'].plot(kind='hist', bins=20, ax=ax)
    ax.set_title("Distribusi Jumlah")
    st.pyplot(fig)

    st.write("Statistik Deskriptif")
    st.dataframe(filtered_df['Jumlah'].describe())

# =====================
# 2. EDA - TREN & KATEGORI
# =====================
with row1_col2:
    st.subheader("EDA – Tren & Kategori")
    fig2, ax2 = plt.subplots()
    filtered_df.groupby('Tahun')['Jumlah'].sum().plot(marker='o', ax=ax2)
    ax2.set_title("Tren Jumlah per Tahun")
    st.pyplot(fig2)

    fig3, ax3 = plt.subplots()
    filtered_df.groupby('Kategori')['Jumlah'].sum().plot(kind='bar', ax=ax3)
    ax3.set_title("Jumlah per Kategori")
    st.pyplot(fig3)

# =====================
# 3. UJI CHI-SQUARE
# =====================
with row1_col3:
    st.subheader("Uji Chi-Square")

    contingency = pd.crosstab(filtered_df['Kategori'], filtered_df['Provinsi'])
    chi2, p, dof, expected = chi2_contingency(contingency)

    st.write("Tabel Kontingensi")
    st.dataframe(contingency)

    fig4, ax4 = plt.subplots()
    im = ax4.imshow(contingency, aspect='auto')
    ax4.set_title("Heatmap Kontingensi")
    plt.colorbar(im, ax=ax4)
    st.pyplot(fig4)

    st.markdown(f"""
    **Chi-Square** : {chi2:.3f}  
    **p-value** : {p:.5f}  
    **Derajat Bebas (df)** : {dof}
    """)

# =====================
# 4. KORELASI & MODEL
# =====================
with row2_col1:
    st.subheader("Korelasi & Model")

    corr = filtered_df[['Jumlah']].corr()
    fig5, ax5 = plt.subplots()
    im2 = ax5.imshow(corr)
    ax5.set_title("Matriks Korelasi")
    plt.colorbar(im2, ax=ax5)
    st.pyplot(fig5)

    st.write("Ringkasan:")
    st.info("Analisis korelasi terbatas pada variabel numerik yang tersedia.")

# =====================
# 5. METADATA VARIABEL
# =====================
with row2_col2:
    st.subheader("Metadata Variabel")

    metadata = pd.DataFrame({
        'Nama Variabel': ['Provinsi', 'Tahun', 'Kategori', 'Jumlah'],
        'Tipe Data': ['Kategorikal', 'Ordinal', 'Kategorikal', 'Numerik'],
        'Kategori': ['Wilayah', 'Waktu', 'Status Gizi', 'Jumlah Kasus'],
        'Deskripsi': [
            'Nama provinsi',
            'Tahun pengamatan',
            'Kategori stunting',
            'Jumlah kasus stunting'
        ]
    })

    st.dataframe(metadata)

# =====================
# 6. KESIMPULAN & REKOMENDASI
# =====================
with row2_col3:
    st.subheader("Kesimpulan & Rekomendasi")

    if p < 0.05:
        st.success("Terdapat hubungan signifikan antar variabel (p < 0.05)")
    else:
        st.warning("Tidak terdapat hubungan signifikan antar variabel (p ≥ 0.05)")

    st.markdown("""
    **Insight:**
    - Distribusi stunting berbeda antar provinsi dan kategori
    - Pola tren dapat diamati secara temporal

    **Rekomendasi:**
    - Fokus intervensi pada kategori dengan frekuensi tinggi
    - Lakukan analisis lanjutan dengan variabel tambahan

    **Batasan:**
    - Data agregat
    - Tidak mencerminkan kausalitas
    """)

st.caption("Dashboard Streamlit – Analisis Chi-Square & EDA")
