import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

st.set_page_config(page_title="Dashboard Analisis Chi-Square", layout="wide")

st.title("📊 Dashboard Analisis Chi-Square & EDA")
st.markdown("Dashboard interaktif untuk EDA, korelasi, dan uji Chi-Square berbasis dataset tingkat provinsi")

# =====================
# LOAD DATA
# =====================
@st.cache_data
def load_data():
    return pd.read_csv("dataset_cleaned.csv")

df = load_data()

# =====================
# PREPROCESSING
# =====================
# Kategorisasi untuk kebutuhan Chi-Square

df['Kemiskinan_Kategori'] = pd.cut(
    df['Kemiskinan_Persen'],
    bins=[0, 5, 10, 100],
    labels=['Rendah', 'Sedang', 'Tinggi']
)

df['Internet_Kategori'] = pd.cut(
    df['Internet_Total'],
    bins=[0, 80, 90, 100],
    labels=['Rendah', 'Sedang', 'Tinggi']
)

# =====================
# SIDEBAR FILTER
# =====================
st.sidebar.header("Filter Data")

provinsi = st.sidebar.multiselect(
    "Provinsi",
    options=df['Provinsi'].unique(),
    default=df['Provinsi'].unique()
)

filtered_df = df[df['Provinsi'].isin(provinsi)]

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
    filtered_df['Kemiskinan_Persen'].plot(kind='hist', bins=15, ax=ax)
    ax.set_title("Distribusi Persentase Kemiskinan")
    st.pyplot(fig)

    st.write("Statistik Deskriptif")
    st.dataframe(filtered_df[['Kemiskinan_Persen', 'Internet_Total']].describe())

# =====================
# 2. EDA - TREN & KATEGORI
# =====================
with row1_col2:
    st.subheader("EDA – Perbandingan Kategori")
    fig2, ax2 = plt.subplots()
    filtered_df.groupby('Internet_Kategori')['Kemiskinan_Persen'].mean().plot(kind='bar', ax=ax2)
    ax2.set_title("Rata-rata Kemiskinan berdasarkan Kategori Internet")
    st.pyplot(fig2)

# =====================
# 3. UJI CHI-SQUARE
# =====================
with row1_col3:
    st.subheader("Uji Chi-Square")

    contingency = pd.crosstab(filtered_df['Internet_Kategori'], filtered_df['Kemiskinan_Kategori'])
    chi2, p, dof, expected = chi2_contingency(contingency)

    st.write("Tabel Kontingensi")
    st.dataframe(contingency)

    fig3, ax3 = plt.subplots()
    im = ax3.imshow(contingency, aspect='auto')
    ax3.set_xticks(range(len(contingency.columns)))
    ax3.set_yticks(range(len(contingency.index)))
    ax3.set_xticklabels(contingency.columns)
    ax3.set_yticklabels(contingency.index)
    ax3.set_title("Heatmap Kontingensi")
    plt.colorbar(im, ax=ax3)
    st.pyplot(fig3)

    st.markdown(f"""
    **Chi-Square** : {chi2:.3f}  
    **p-value** : {p:.5f}  
    **Derajat Bebas (df)** : {dof}
    """)

# =====================
# 4. KORELASI & MODEL
# =====================
with row2_col1:
    st.subheader("Korelasi")

    corr = filtered_df[['Internet_Total', 'Kemiskinan_Persen']].corr()
    fig4, ax4 = plt.subplots()
    im2 = ax4.imshow(corr)
    ax4.set_xticks(range(len(corr.columns)))
    ax4.set_yticks(range(len(corr.columns)))
    ax4.set_xticklabels(corr.columns)
    ax4.set_yticklabels(corr.columns)
    ax4.set_title("Matriks Korelasi")
    plt.colorbar(im2, ax=ax4)
    st.pyplot(fig4)

# =====================
# 5. METADATA VARIABEL
# =====================
with row2_col2:
    st.subheader("Metadata Variabel")

    metadata = pd.DataFrame({
        'Variabel': ['Provinsi', 'Internet_Perkotaan', 'Internet_Perdesaan', 'Internet_Total', 'Kemiskinan_Persen'],
        'Tipe Data': ['Kategorikal', 'Numerik', 'Numerik', 'Numerik', 'Numerik'],
        'Deskripsi': [
            'Nama provinsi',
            'Persentase akses internet wilayah perkotaan',
            'Persentase akses internet wilayah perdesaan',
            'Total persentase akses internet',
            'Persentase penduduk miskin'
        ]
    })

    st.dataframe(metadata)

# =====================
# 6. KESIMPULAN & REKOMENDASI
# =====================
with row2_col3:
    st.subheader("Kesimpulan & Rekomendasi")

    if p < 0.05:
        st.success("Terdapat hubungan signifikan antara akses internet dan tingkat kemiskinan (p < 0.05)")
    else:
        st.warning("Tidak terdapat hubungan signifikan antara akses internet dan tingkat kemiskinan (p ≥ 0.05)")

    st.markdown("""
    **Insight:**
    - Provinsi dengan akses internet lebih tinggi cenderung memiliki tingkat kemiskinan lebih rendah

    **Rekomendasi:**
    - Peningkatan infrastruktur internet di wilayah dengan kemiskinan tinggi

    **Batasan:**
    - Data agregat provinsi
    - Kategorisasi bersifat diskret
    """)

st.caption("Dashboard Streamlit – Analisis Chi-Square & EDA")
