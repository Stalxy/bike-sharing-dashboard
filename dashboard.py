import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ======================
# Load Data
# ======================
df = pd.read_csv("main_data.csv")

# Convert date
df['dteday'] = pd.to_datetime(df['dteday'])

st.title("🚴 Bike Sharing Dashboard")

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.header("Filter Data")

# Filter tanggal
start_date = st.sidebar.date_input("Tanggal Mulai", df['dteday'].min())
end_date = st.sidebar.date_input("Tanggal Akhir", df['dteday'].max())

# Filter cuaca
weather_options = df['weather_label'].unique()
selected_weather = st.sidebar.multiselect(
    "Pilih Cuaca",
    options=weather_options,
    default=weather_options
)

# ======================
# FILTER DATA
# ======================
filtered_df = df[
    (df['dteday'] >= pd.to_datetime(start_date)) &
    (df['dteday'] <= pd.to_datetime(end_date)) &
    (df['weather_label'].isin(selected_weather))
]


# ======================
# VISUALISASI 1
# Pengaruh Cuaca
# ======================
st.subheader("Pengaruh Cuaca terhadap Penyewaan")

weather_avg = filtered_df.groupby('weather_label')['cnt'].mean().reset_index()

fig2, ax2 = plt.subplots()
sns.barplot(data=weather_avg, x='weather_label', y='cnt', ax=ax2)
ax2.set_title("Rata-rata Penyewaan Berdasarkan Cuaca")

st.pyplot(fig2)

# ======================
# VISUALISASI 2
# Hari Kerja vs Libur
# ======================
st.subheader("Perbandingan Penyewaan: Hari Kerja vs Libur")

workingday_avg = filtered_df.groupby('workingday')['cnt'].mean().reset_index()

workingday_avg['workingday'] = workingday_avg['workingday'].map({
    0: 'Libur',
    1: 'Hari Kerja'
})

fig1, ax1 = plt.subplots()
sns.barplot(data=workingday_avg, x='workingday', y='cnt', ax=ax1)
ax1.set_title("Rata-rata Penyewaan Sepeda")

st.pyplot(fig1)