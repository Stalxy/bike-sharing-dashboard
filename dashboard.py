import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

st.title("🚴 Dashboard Bike Sharing")

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    return df

df = load_data()

# ======================
# CLEAN DATA (kalau sudah clean bisa langsung pakai df)
# ======================
df_day_cleaned = df.copy()

# =========================================================
# 1. PENGARUH CUACA TERHADAP PENYEWAAN SEPEDA (BARPLOT)
# =========================================================
st.subheader("🌦️ Pengaruh Cuaca terhadap Rata-rata Penyewaan Sepeda")

weather_impact = (
    df_day_cleaned.groupby('weather_label')['cnt']
    .mean()
    .reset_index()
)

weather_impact_sorted = weather_impact.sort_values("cnt", ascending=False)

fig1, ax1 = plt.subplots(figsize=(10, 6))

sns.barplot(
    x='cnt',
    y='weather_label',
    data=weather_impact_sorted,
    hue='weather_label',
    palette='viridis',
    legend=False,
    ax=ax1
)

ax1.set_title('Pengaruh Cuaca terhadap Rata-rata Penyewaan Sepeda', fontsize=14, fontweight='bold')
ax1.set_xlabel('Rata-rata Jumlah Penyewaan Sepeda')
ax1.set_ylabel('Kondisi Cuaca')
ax1.grid(axis='x', linestyle='--', alpha=0.6)

st.pyplot(fig1)

# =========================================================
# 2. PERBANDINGAN HARI KERJA VS LIBUR (PIE CHART)
# =========================================================
st.subheader("📅 Perbandingan Penyewaan: Hari Kerja vs Hari Libur")

avg_workingday = df_day_cleaned.groupby('workingday')['cnt'].mean()

labels = ['Libur', 'Hari Kerja']

fig2, ax2 = plt.subplots(figsize=(6, 6))

ax2.pie(
    avg_workingday,
    labels=labels,
    autopct='%1.1f%%',
    colors=['lightcoral', 'skyblue']
)

ax2.set_title('Perbandingan Penyewaan Sepeda: Hari Kerja vs Hari Libur')

st.pyplot(fig2)