# 🌫️ Proyek Analisis Data - Air Quality Analysis Dashboard

## 📌 Deskripsi
Proyek ini melakukan analisis kualitas udara dengan fokus pada konsentrasi **PM10** menggunakan Air Quality Dataset periode Maret 2013 hingga Februari 2017, dengan tujuan memahami pola perubahan kualitas udara dari waktu ke waktu serta faktor-faktor yang mempengaruhinya. Hasil analisis disajikan dalam bentuk **notebook** dan **dashboard interaktif menggunakan Streamlit**.

---

## 📂 Struktur Direktori
```
submission/
│
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
│
├── data/
├── notebook.ipynb
├── requirements.txt
├── url.txt
└── README.md
```

---

## 📊 Isi Dashboard
Dashboard menampilkan analisis PM10 secara interaktif dengan fitur:

- Filter data berdasarkan **stasiun** dan **tahun**
- Ringkasan statistik deskriptif (rata-rata, median, maksimum, jumlah data)
- Tren PM10 dari waktu ke waktu (bulanan & musiman)
- Hubungan PM10 dengan faktor lingkungan (suhu & kecepatan angin)
- Perbandingan kondisi PM10 antar stasiun
- Distribusi kategori kualitas udara
- Insight singkat dan rekomendasi dari hasil analisis

```

## Setup Environment - Anaconda

```
conda create --name air-quality-ds python=3.9
conda activate air-quality-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

```
mkdir submission
cd submission
pip install -r requirements.txt
```

## Run Streamlit App

```
streamlit run dashboard/dashboard.py
```

## 🛠️ Tools & Library
- Python  
- Pandas  
- Matplotlib  
- Seaborn  
- Streamlit  

---

## 👤 Author
Zahra Salma Dwi Meylinda