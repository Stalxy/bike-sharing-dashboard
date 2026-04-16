import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
sns.set_style("whitegrid")

# ======================
# LOAD DATA
# ======================
df = pd.read_csv("main_data.csv")

# Convert date
df['dteday'] = pd.to_datetime(df['dteday'])

# Mapping weather 
if 'weather_label' not in df.columns:
    df['weather_label'] = df['weathersit'].map({
        1: 'Cerah',
        2: 'Berawan',
        3: 'Hujan Ringan',
        4: 'Hujan Lebat'
    })
    
# Mapping season
if 'season' in df.columns:
    df['season_label'] = df['season'].map({
        1: 'Spring',
        2: 'Summer',
        3: 'Fall',
        4: 'Winter'
    })
else:
    df['season_label'] = 'Unknown'

# ======================
# TITLE
# ======================
st.title("🚴 Bike Sharing Dashboard")
st.markdown("Analisis penyewaan sepeda berdasarkan waktu dan kondisi cuaca.")

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.header("🔍 Filter Data")

# Filter tanggal
start_date = st.sidebar.date_input("Tanggal Mulai", df['dteday'].min())
end_date = st.sidebar.date_input("Tanggal Akhir", df['dteday'].max())

# Filter cuaca
selected_weather = st.sidebar.multiselect(
    "Pilih Cuaca",
    options=df['weather_label'].unique(),
    default=df['weather_label'].unique()
)

# Filter season
selected_season = st.sidebar.multiselect(
    "Pilih Season",
    options=df['season_label'].unique(),
    default=df['season_label'].unique()
)

# Filter grafik
chart_type = st.sidebar.selectbox(
    "Pilih Jenis Grafik",
    ["Pie Chart", "Bar Chart"]
)

# ======================
# FILTER DATA
# ======================
filtered_df = df[
    (df['dteday'] >= pd.to_datetime(start_date)) &
    (df['dteday'] <= pd.to_datetime(end_date)) &
    (df['weather_label'].isin(selected_weather)) &
    (df['season_label'].isin(selected_season))
]

# ======================
# INFO DATA
# ======================
st.subheader("📊 Ringkasan Data")
st.write("Jumlah data setelah filter:", filtered_df.shape[0])

# ======================
# VISUALISASI 1
# ======================
st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")

weather_avg = (
    filtered_df.groupby('weather_label')['cnt']
    .mean()
    .reset_index()
    .sort_values(by='cnt', ascending=False)
)

fig, ax = plt.subplots()

if chart_type == "Pie Chart":
    ax.pie(
        weather_avg['cnt'],
        labels=weather_avg['weather_label'],
        autopct='%1.1f%%'
    )
else:
    sns.barplot(
        data=weather_avg,
        x='cnt',
        y='weather_label',
        palette='viridis',
        ax=ax
    )

ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Cuaca (2011–2012)")

st.pyplot(fig)

# ======================
# VISUALISASI 2
# ======================
st.subheader("Penyewaan: Hari Kerja vs Libur")

workingday_avg = (
    filtered_df.groupby('workingday')['cnt']
    .mean()
    .reset_index()
)

labels = ['Libur' if x == 0 else 'Hari Kerja' for x in workingday_avg['workingday']]

fig, ax = plt.subplots()

if chart_type == "Pie Chart":
    ax.pie(
        workingday_avg['cnt'],
        labels=labels,
        autopct='%1.1f%%',
        colors=['#FF9800', '#4CAF50']
    )
else:
    sns.barplot(
        x=labels,
        y=workingday_avg['cnt'],
        palette=['#FF9800', '#4CAF50'],
        ax=ax
    )

ax.set_title("Rata-rata Penyewaan Sepeda: Hari Kerja vs Libur")

st.pyplot(fig)