import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Analisis PM10",
    page_icon="🌫️",
    layout="wide"
)

sns.set_style("whitegrid")

# CSS
st.markdown("""
<style>
.main-title {
    font-size: 52px !important;
    font-weight: 900 !important;
    color: #16324f !important;
    margin-bottom: 0px !important;
    line-height: 1.2 !important;
}
.sub-title {
    font-size: 20px !important;
    color: #5b6573 !important;
    margin-top: 6px !important;
    margin-bottom: 20px !important;
}
.section-title {
    font-size: 30px !important;
    font-weight: 800 !important;
    color: #16324f !important;
    border-left: 6px solid #4c78a8 !important;
    padding-left: 12px !important;
    margin-top: 20px !important;
    margin-bottom: 12px !important;
}
.insight-box {
    background-color: #f4f8fb;
    padding: 16px;
    border-radius: 10px;
    border-left: 6px solid #4c78a8;
    margin-top: 10px;
    margin-bottom: 20px;
}
.small-note {
    font-size: 13px;
    color: #6b7280;
}
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    base_path = Path(__file__).parent
    file_path = base_path / "main_data.csv"
    df = pd.read_csv(file_path)

    df["datetime"] = pd.to_datetime(df["datetime"])
    df["year"] = df["datetime"].dt.year
    df["month"] = df["datetime"].dt.month
    df["month_name"] = df["datetime"].dt.month_name()

    df["PM10_category"] = pd.cut(
        df["PM10"],
        bins=[0, 50, 100, 150, 200, 500, 1000],
        labels=["Good", "Moderate", "Unhealthy", "Very Unhealthy", "Hazardous", "Extreme"],
        include_lowest=True
    )

    return df

air_quality_df = load_data()

# Sidebar
with st.sidebar:
    st.title("🎛️ Filter Dashboard")
    st.markdown("Atur tampilan data sesuai kebutuhan.")

    station_options = sorted(air_quality_df["station"].dropna().unique().tolist())
    selected_stations = st.multiselect(
        "📍 Pilih stasiun",
        options=station_options,
        default=station_options
    )

    year_options = sorted(air_quality_df["year"].dropna().unique().tolist())
    selected_years = st.multiselect(
        "📅 Pilih tahun",
        options=year_options,
        default=year_options
    )

    st.markdown("---")
    st.markdown("### ℹ️ Keterangan")
    st.markdown(
        """
        Dashboard ini menampilkan analisis konsentrasi **PM10** berdasarkan:
        - Tren waktu,
        - Faktor lingkungan,
        - Perbandingan antar stasiun,
        - Distribusi dan kategori kualitas udara.
        """
    )

filtered_df = air_quality_df[
    (air_quality_df["station"].isin(selected_stations)) &
    (air_quality_df["year"].isin(selected_years))
].copy()

if filtered_df.empty:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
    st.stop()

# Header
st.markdown(
    '<p class="main-title">🌫️ Dashboard Analisis Kualitas Udara (PM10)</p>',
    unsafe_allow_html=True
)
st.markdown(
    '<p class="sub-title">Analisis konsentrasi PM10 pada 12 stasiun pengamatan selama periode Maret 2013 hingga Februari 2017.</p>',
    unsafe_allow_html=True
)

# Statistik Deskriptif
st.markdown('<p class="section-title">📌 Ringkasan Utama</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Rata-rata PM10", f"{filtered_df['PM10'].mean():.2f}")
col2.metric("Median PM10", f"{filtered_df['PM10'].median():.2f}")
col3.metric("PM10 Maksimum", f"{filtered_df['PM10'].max():.2f}")
col4.metric("Jumlah Observasi", f"{len(filtered_df):,}")

st.markdown(
    '<p class="small-note">Nilai maksimum merepresentasikan data setelah proses cleaning dan pembatasan outlier.</p>',
    unsafe_allow_html=True
)

st.markdown("---")

# 1. Tren PM10
st.markdown('<p class="section-title">📈 1. Tren Konsentrasi PM10</p>', unsafe_allow_html=True)

pm10_monthly = (
    filtered_df
    .resample(rule="ME", on="datetime")
    .agg({"PM10": "mean"})
    .reset_index()
)

monthly_pattern = (
    filtered_df
    .groupby("month")["PM10"]
    .mean()
    .reset_index()
)

highest_month = monthly_pattern.loc[monthly_pattern["PM10"].idxmax(), "month"]
highest_value = monthly_pattern["PM10"].max()
lowest_month = monthly_pattern.loc[monthly_pattern["PM10"].idxmin(), "month"]
lowest_value = monthly_pattern["PM10"].min()

col1, col2 = st.columns([2, 1])

with col1:
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(pm10_monthly["datetime"], pm10_monthly["PM10"], marker="o", linewidth=2.2, color="#2a6f97")
    ax.set_title("Tren Rata-rata PM10 Bulanan")
    ax.set_xlabel("Waktu")
    ax.set_ylabel("Rata-rata PM10")
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.lineplot(data=monthly_pattern, x="month", y="PM10", marker="o", color="#468faf", linewidth=2.2, ax=ax)
    ax.set_title("Pola Musiman PM10")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata PM10")
    ax.set_xticks(range(1, 13))
    st.pyplot(fig)

st.markdown(f"""
<div class="insight-box">
<b>🔎 Insight:</b><br>
Konsentrasi PM10 menunjukkan pola yang fluktuatif dan cenderung dipengaruhi oleh musim. 
Secara umum, nilai PM10 lebih tinggi pada awal hingga akhir tahun, lalu menurun di pertengahan tahun. 
Pada pola musiman, rata-rata tertinggi terjadi pada <b>bulan {int(highest_month)}</b> dengan nilai sekitar <b>{highest_value:.2f}</b>, 
sedangkan rata-rata terendah terjadi pada <b>bulan {int(lowest_month)}</b> dengan nilai sekitar <b>{lowest_value:.2f}</b>. 
Ini menunjukkan bahwa ada periode tertentu yang lebih rentan mengalami penurunan kualitas udara.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 2. Faktor lingkungan
st.markdown('<p class="section-title">🌍 2. Hubungan PM10 dengan Faktor Lingkungan</p>', unsafe_allow_html=True)

corr_temp = filtered_df["PM10"].corr(filtered_df["TEMP"])
corr_wspm = filtered_df["PM10"].corr(filtered_df["WSPM"])

# sampling
sample_n = min(8000, len(filtered_df))
sample_df = filtered_df.sample(n=sample_n, random_state=42)

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.regplot(
        data=sample_df,
        x="TEMP",
        y="PM10",
        scatter_kws={"alpha": 0.18, "s": 12},
        line_kws={"color": "red"},
        ax=ax
    )
    ax.set_title("PM10 vs Suhu (TEMP)")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.regplot(
        data=sample_df,
        x="WSPM",
        y="PM10",
        scatter_kws={"alpha": 0.18, "s": 12},
        line_kws={"color": "red"},
        ax=ax
    )
    ax.set_title("PM10 vs Kecepatan Angin (WSPM)")
    st.pyplot(fig)

faktor_dominan = "WSPM" if abs(corr_wspm) > abs(corr_temp) else "TEMP"

st.markdown(f"""
<div class="insight-box">
<b>🔎 Insight:</b><br>
Hubungan antara PM10 dan suhu (<b>TEMP</b>) terlihat sangat lemah dengan korelasi <b>{corr_temp:.2f}</b>, 
sehingga suhu bukan faktor utama yang mempengaruhi perubahan PM10. 
Sebaliknya, kecepatan angin (<b>WSPM</b>) memiliki hubungan negatif dengan korelasi <b>{corr_wspm:.2f}</b>, 
yang berarti semakin tinggi kecepatan angin, konsentrasi PM10 cenderung menurun. 
Dengan demikian, <b>{faktor_dominan}</b> merupakan faktor lingkungan yang lebih berpengaruh dibandingkan suhu.
</div>
""", unsafe_allow_html=True)

st.caption("📎 Scatter plot menggunakan sampel data agar visualisasi lebih cepat tanpa mengubah pola utama.")

st.markdown("---")

# 3. Perbandingan antar stasiun
st.markdown('<p class="section-title">🏭 3. Perbandingan Konsentrasi PM10 antar Stasiun</p>', unsafe_allow_html=True)

station_avg = (
    filtered_df.groupby("station")["PM10"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

worst_station = station_avg.iloc[0]["station"]
best_station = station_avg.iloc[-1]["station"]

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(8, 5))
    
    sns.barplot(
        data=station_avg,
        x="PM10",
        y="station",
        color="#2a6f97",        
        edgecolor="black",
        linewidth=0.6,
        ax=ax
    )
    
    for i, v in enumerate(station_avg["PM10"]):
        ax.text(v + 2, i, f"{v:.1f}", va='center', fontsize=9)
    
    ax.set_title("Rata-rata PM10 per Stasiun")
    ax.set_xlabel("Rata-rata PM10")
    ax.set_ylabel("Stasiun")
    
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(8, 5))

    sns.boxplot(
        data=filtered_df,
        x="PM10",
        y="station",
        color="#468faf",
        linewidth=1.2,
        fliersize=2,
        ax=ax
    )

    ax.set_title("Distribusi PM10 per Stasiun")
    ax.set_xlabel("PM10")
    ax.set_ylabel("Stasiun")

    st.pyplot(fig)

if len(selected_stations) == 1:
    station_note = f"Karena hanya satu stasiun dipilih, perbandingan antar stasiun menjadi terbatas. Fokus saat ini ada pada stasiun {selected_stations[0]}."
else:
    station_note = f"Stasiun dengan rata-rata PM10 tertinggi adalah {worst_station}, sedangkan yang terendah adalah {best_station}."

st.markdown(f"""
<div class="insight-box">
<b>🔎 Insight:</b><br>
Terdapat perbedaan konsentrasi PM10 antar stasiun, meskipun selisih antar beberapa lokasi tidak terlalu jauh. 
<b>{station_note}</b> 
Secara umum, stasiun dengan nilai lebih tinggi cenderung memiliki kualitas udara yang lebih buruk. 
Boxplot juga menunjukkan adanya banyak nilai ekstrem di berbagai stasiun, yang menandakan bahwa lonjakan polusi terjadi di lebih dari satu lokasi.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. Distribusi dan kategori PM10
st.markdown('<p class="section-title">⚠️ 4. Distribusi Konsentrasi dan Kategori PM10</p>', unsafe_allow_html=True)

category_counts = (
    filtered_df["PM10_category"]
    .value_counts()
    .sort_index()
    .reset_index()
)
category_counts.columns = ["Kategori", "Jumlah"]

dominant_category = filtered_df["PM10_category"].value_counts().idxmax()

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(filtered_df["PM10"], bins=40, kde=True, color="#468faf", ax=ax)
    ax.set_title("Distribusi PM10")
    ax.set_xlabel("PM10")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=category_counts, x="Kategori", y="Jumlah", palette="viridis", ax=ax)
    ax.set_title("Distribusi Kategori PM10")
    ax.set_xlabel("Kategori PM10")
    ax.set_ylabel("Jumlah")
    plt.xticks(rotation=20)
    st.pyplot(fig)

st.markdown(f"""
<div class="insight-box">
<b>🔎 Insight:</b><br>
Sebagian besar data PM10 berada pada kategori <b>{dominant_category}</b> serta kategori aman hingga sedang lainnya. 
Namun, masih terdapat cukup banyak observasi pada kategori yang lebih buruk seperti <b>Unhealthy</b> hingga <b>Hazardous</b>, 
yang menunjukkan bahwa pada waktu tertentu kualitas udara dapat memburuk dan berpotensi berdampak pada kesehatan. 
Kategori <b>Extreme</b> relatif jarang muncul, tetapi tetap menunjukkan adanya risiko kejadian polusi tinggi.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Kesimpulan 
st.markdown('<p class="section-title">📝 Kesimpulan Utama</p>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
<b>📌 Ringkasan:</b><br>
<ul>
<li>PM10 menunjukkan pola fluktuatif dengan kecenderungan musiman yang cukup jelas.</li>
<li>Kecepatan angin lebih berpengaruh terhadap perubahan PM10 dibandingkan suhu.</li>
<li>Terdapat perbedaan konsentrasi PM10 antar stasiun, dengan beberapa lokasi menunjukkan kualitas udara yang lebih buruk.</li>
<li>Meskipun mayoritas data berada pada kategori aman hingga sedang, tetap ada periode dengan kualitas udara buruk yang perlu diperhatikan.</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Rekomendasi
st.markdown('<p class="section-title">🎯 Rekomendasi / Action Item</p>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
<b>✅ Rekomendasi:</b><br>
<ul>
<li>Fokuskan pemantauan kualitas udara pada periode <b>November–Maret</b> karena konsentrasi PM10 cenderung lebih tinggi pada awal hingga akhir tahun.</li>
<li>Prioritaskan pengendalian polusi pada wilayah dengan rata-rata PM10 tinggi, terutama <b>Gucheng</b>, serta wilayah lain seperti <b>Wanshouxigong</b> dan <b>Wanliu</b>.</li>
<li>Gunakan kecepatan angin (<b>WSPM</b>) sebagai salah satu indikator pendukung dalam pemantauan kualitas udara, karena angin berperan dalam menurunkan konsentrasi PM10.</li>
<li>Tingkatkan kewaspadaan saat kualitas udara masuk kategori <b>Unhealthy</b> hingga <b>Hazardous</b>, misalnya dengan imbauan pengurangan aktivitas luar ruangan.</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.caption("Dashboard Analisis PM10 | Zahra Salma Dwi Meylinda")