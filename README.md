# 🌫️ Proyek Analisis Data - Air Quality Dataset

## 📌 Deskripsi
Proyek ini melakukan analisis kualitas udara dengan fokus pada konsentrasi **PM10** menggunakan Air Quality Dataset periode Maret 2013 hingga Februari 2017.  
Hasil analisis disajikan dalam bentuk **notebook** dan **dashboard interaktif menggunakan Streamlit**.

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

- 🎯 **Filter Data**
  - Filter berdasarkan **stasiun**
  - Filter berdasarkan **tahun**

- 📌 **Ringkasan Statistik**
  - Rata-rata PM10
  - Median PM10
  - Nilai maksimum
  - Jumlah observasi

- 📈 **Tren PM10**
  - Tren bulanan PM10 (time series)
  - Pola musiman PM10

- 🌡️ **Analisis Faktor Lingkungan**
  - Hubungan PM10 dengan suhu (TEMP)
  - Hubungan PM10 dengan kecepatan angin (WSPM)

- 🏭 **Perbandingan Antar Stasiun**
  - Rata-rata PM10 per stasiun
  - Distribusi PM10 per stasiun (boxplot)

- 🚦 **Distribusi Kategori PM10**
  - Kategori kualitas udara (Good, Moderate, dll)

- 💡 **Insight & Rekomendasi**
  - Ringkasan hasil analisis
  - Rekomendasi berdasarkan pola data

---

## ⚙️ Cara Menjalankan Dashboard

### 1. Install dependencies
```
pip install -r requirements.txt
```

### 2. Jalankan Streamlit
```
streamlit run dashboard/dashboard.py
```

### 3. Buka di browser
```
http://localhost:8501
```

---

## 🛠️ Tools & Library
- Python  
- Pandas  
- Matplotlib  
- Seaborn  
- Streamlit  

---

## 👤 Author
Zahra Salma Dwi Meylinda