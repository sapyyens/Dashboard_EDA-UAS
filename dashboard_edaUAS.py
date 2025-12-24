import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Dashboard Ketimpangan Digital 2024", layout="wide")

# --- MOCKUP DATA (Berdasarkan hasil analisis di file .ipynb) ---
# Di dunia nyata, Anda bisa memuat file CSV: df = pd.read_csv("data_kemiskinan.csv")
data = {
    'Provinsi': ['Provinsi ' + str(i) for i in range(1, 39)],
    'Kemiskinan (%)': np.random.uniform(5, 25, 38),
    'Akses_Internet (%)': []
}
# Menghasilkan data Akses Internet berdasarkan rumus regresi: Y = 108.05 - 1.95X + Noise
for x in data['Kemiskinan (%)']:
    noise = np.random.normal(0, 5)
    y = 108.05 - 1.95 * x + noise
    data['Akses_Internet (%)'].append(clamp(y, 0, 100))

def clamp(n, minn, maxn):
    return max(min(n, maxn), minn)

df = pd.DataFrame(data)

# --- HEADER ---
st.title("📊 Dashboard Analisis Ketimpangan Kemiskinan & Akses Internet")
st.markdown("""
Dashboard ini menyajikan hasil analisis hubungan antara tingkat kemiskinan dan akses internet antarprovinsi di Indonesia tahun 2024 
berdasarkan metode **Regresi Linear** dan **Uji Chi-Square**.
""")

# --- ROW 1: KPI CARDS ---
st.subheader("Ringkasan Statistik Utama")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Rata-rata Kemiskinan", "11.15%")
col2.metric("Rata-rata Akses Internet", "86.27%")
col3.metric("Korelasi (r)", "-0.8244", "Sangat Kuat")
col4.metric("Koefisien Determinasi (R²)", "0.6796")

st.divider()

# --- ROW 2: ANALISIS REGRESI ---
st.subheader("1. Analisis Regresi Linear (Pendekatan Numerik)")
c1, c2 = st.columns([2, 1])

with c1:
    # Visualisasi Scatter Plot & Regresi
    fig_reg = px.scatter(df, x="Kemiskinan (%)", y="Akses_Internet (%)", 
                         trendline="ols", trendline_color_override="red",
                         hover_name="Provinsi", title="Tren Hubungan Kemiskinan vs Akses Internet")
    st.plotly_chart(fig_reg, use_container_width=True)

with c2:
    st.info("**Persamaan Regresi:**")
    st.latex(r"Y = 108.05 - 1.95X")
    st.write("""
    **Interpretasi:**
    * **Intercept (108.05):** Jika kemiskinan 0%, akses internet diprediksi mencapai 108.05% (secara teoretis).
    * **Koefisien (-1.95):** Setiap kenaikan **1% kemiskinan** akan menurunkan **1.95% akses internet**.
    * Model ini menjelaskan **67.96%** variasi data.
    """)

# --- ROW 3: ANALISIS CHI-SQUARE & RESIDUAL ---
st.subheader("2. Analisis Chi-Square (Pendekatan Kategorik)")
c3, c4 = st.columns([1, 1])

with c3:
    # Heatmap Tabel Kontingensi (Data Dummy untuk visualisasi)
    contingency_data = [[10, 2, 1], [3, 12, 2], [1, 2, 7]]
    categories = ['Rendah', 'Sedang', 'Tinggi']
    fig_heat = px.imshow(contingency_data, 
                        labels=dict(x="Akses Internet", y="Kemiskinan", color="Frekuensi"),
                        x=categories, y=categories,
                        color_continuous_scale='Blues', text_auto=True,
                        title="Heatmap Tabel Kontingensi")
    st.plotly_chart(fig_heat, use_container_width=True)

with c4:
    st.success(f"**P-Value: 0.001871** (Signifikan)")
    st.write(f"**Chi-Square Stat:** 17.0731")
    st.write(f"**Cramer's V:** 0.4739 (Hubungan Kuat)")
    st.warning("""
    **Insight Utama:**
    Terdapat hubungan signifikan secara statistik antara kategori tingkat kemiskinan dan tingkat akses internet.
    """)

# --- ROW 4: TABEL RESIDUAL (POINT PENTING SKRIPSI) ---
st.subheader("3. Analisis Residual Terstandarisasi")
st.write("Tabel ini menunjukkan kelompok mana yang paling berkontribusi pada ketimpangan.")

residual_df = pd.DataFrame({
    'Kategori Internet': ['Rendah', 'Sedang', 'Tinggi'],
    'Kemiskinan Rendah': [1.442, 0.127, 1.710],
    'Kemiskinan Sedang': [-0.894, 0.667, 0],
    'Kemiskinan Tinggi': [2.693, -0.798, -1.622]
})

st.table(residual_df)

st.error("""
**Temuan Kritis:** Sel **Kemiskinan Tinggi - Akses Internet Rendah** memiliki residual **2.693** ($> 2$). 
Ini adalah faktor utama ketimpangan, menyumbang **42.47%** terhadap total nilai Chi-Square.
""")

# --- FOOTER ---
st.caption("Dashboard Tugas Besar EDA - Kelompok 1 - Sains Data UPNVJT")
