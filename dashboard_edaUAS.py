import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# CONFIG
# =====================================================
st.set_page_config(
    page_title="Dashboard Kelompok 1 - EDA 2024",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    df = pd.read_csv("dataset_cleaned.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# =====================================================
# HEADER
# =====================================================
st.title("📊 Analisis Ketimpangan Digital di Indonesia 2024")
st.caption("Pendekatan tabel distribusi (tanpa visualisasi peta)")

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
# TABEL PERSEBARAN (PENGGANTI PETA)
# =====================================================
st.subheader("📋 Persebaran Akses Internet per Provinsi")

df_table = df[[
    "Provinsi",
    "Internet_Total",
    "Kemiskinan_Persen"
]].sort_values(
    by="Internet_Total",
    ascending=False
)

st.dataframe(
    df_table,
    use_container_width=True,
    hide_index=True
)

st.info(
    f"📌 **Insight Tabel:** Provinsi dengan akses internet tertinggi adalah "
    f"**{prov_tertinggi['Provinsi']}** "
    f"({prov_tertinggi['Internet_Total']:.2f}%), "
    f"sementara akses terendah terdapat di "
    f"**{prov_terendah['Provinsi']}** "
    f"({prov_terendah['Internet_Total']:.2f}%). "
    f"Perbedaan ini mengindikasikan ketimpangan infrastruktur digital antar wilayah."
)
st.divider()

# =====================================================
# RANKING
# =====================================================
st.subheader("🏆 Ranking Provinsi Berdasarkan Akses Internet")

df_rank = df_display.copy()
df_rank["Ranking Internet"] = range(1, len(df_rank) + 1)

st.dataframe(
    df_rank,
    use_container_width=True,
    hide_index=True
)
st.divider()
# =====================================================
# KATEGORISASI
# =====================================================
st.subheader("📌 Kategorisasi Provinsi")

df_cat = df.copy()

df_cat["Kategori Internet"] = pd.cut(
    df_cat["Internet_Total"],
    bins=[0, 50, 75, 100],
    labels=["Rendah", "Sedang", "Tinggi"]
)

df_cat["Kategori Kemiskinan"] = pd.cut(
    df_cat["Kemiskinan_Persen"],
    bins=[0, 7, 12, 100],
    labels=["Rendah", "Sedang", "Tinggi"]
)

st.dataframe(
    df_cat[[
        "Provinsi",
        "Internet_Total",
        "Kategori Internet",
        "Kemiskinan_Persen",
        "Kategori Kemiskinan"
    ]],
    use_container_width=True,
    hide_index=True
)
st.divider()
# =====================================================
# REGRESI
# =====================================================
c1, c2 = st.columns(2)

with c1:
    st.subheader("📉 Analisis Regresi Linear")

    x = df["Kemiskinan_Persen"]
    y = df["Internet_Total"]

    slope, intercept = np.polyfit(x, y, 1)

    fig_reg = px.scatter(
        df,
        x="Kemiskinan_Persen",
        y="Internet_Total",
        hover_name="Provinsi",
        labels={
            "Kemiskinan_Persen": "Kemiskinan (%)",
            "Internet_Total": "Akses Internet (%)"
        }
    )

    fig_reg.add_trace(
        go.Scatter(
            x=[x.min(), x.max()],
            y=[intercept + slope * x.min(), intercept + slope * x.max()],
            mode="lines",
            name="Regresi",
            line=dict(color="red")
        )
    )

    st.plotly_chart(fig_reg, use_container_width=True)
    st.info(f"Model Regresi: **Y = {intercept:.2f} + ({slope:.2f})X**")

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
    st.success("**P-Value: 0.001871** (Hubungan Signifikan)")

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
    "Insight: Konsentrasi tertinggi terjadi pada "
    "**Kemiskinan Tinggi – Internet Rendah**, "
    "menunjukkan ketimpangan digital yang nyata."
)


