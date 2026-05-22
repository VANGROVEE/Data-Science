# VANGROVE: AgroAnalytics Hub & Early Warning System

Sistem pemantauan kesehatan tanaman berbasis AI dan Web-GIS untuk wilayah Provinsi Sumatera Utara.

## 📁 Struktur Repositori
* `app.py`: Aplikasi dashboard interaktif menggunakan Streamlit dan Plotly (Web-GIS & Early Warning System).
* `preprocessing.ipynb`: Tahap data gathering dari Kaggle, pembersihan duplikat, dan ekstraksi tabel.
* `feature_engineering.ipynb`: Tahap penambahan fitur geolokasi (Sumut), waktu simulatif, rekomendasi agronomis, dan analisis EDA.
* `cleaned_dataset_final.csv`: Dataset akhir yang sudah siap digunakan untuk Dashboard dan Modeling.

## 💻 Cara Menjalankan Dashboard Secara Lokal
Untuk menjalankan dashboard Streamlit di komputer lokal Anda, ikuti langkah-langkah berikut:

1. **Clone Repositori:**
   git clone [https://github.com/VANGROVEE/Data-Science.git](https://github.com/VANGROVEE/Data-Science.git)
   cd Data-Science

2. **Buat dan Aktifkan Virtual Environment (Direkomendasikan):**

         python -m venv venv

         Windows (PowerShell):  .\venv\Scripts\Activate.ps1

         Mac/Linux:  source venv/bin/activate

3. **Install Library yang Dibutuhkan:**
   ```bash
   pip install -r requirements.txt

4. **Jalankan Aplikasi Streamlit:**
streamlit run app.py


## 📊 Dataset

Dataset citra tanaman menggunakan data sekunder dari Kaggle:
[Kaggle: Data Science Data](https://www.kaggle.com/datasets/pppiiiy/data-science-data)

> **Catatan:** Jangan mengunggah folder citra mentah ke dalam repositori ini karena batasan ukuran file GitHub. Gunakan `cleaned_dataset_final.csv` untuk referensi data analitik.

## 🚀 Analisis EDA & Fitur Dashboard

Kami telah melakukan analisis mendalam terhadap 47.516 baris data citra yang mencakup:

* **Peta Sebaran Web-GIS:** Visualisasi geografis interaktif titik koordinat kasus di Provinsi Sumatera Utara, tepatnya pada Kabupaten Karo, Simalungun, Dairi, Langkat, dan Deli Serdang menggunakan Plotly OpenStreetMap.
* **Early Warning System (EWS):** Grafik tren bulanan interaktif dari April 2024 hingga April 2026 untuk memantau lonjakan kasus dan mendeteksi potensi wabah secara dini.
* **Analisis Bisnis Komprehensif:** Pemetaan proporsi tanaman paling rentan, sebaran kasus per kabupaten, dan distribusi penyakit spesifik untuk menjawab 5 pertanyaan bisnis utama.
* **Actionable Insights & Solusi:** Panel panduan rekomendasi otomatis yang menampilkan pemicu lingkungan serta saran penanganan agronomis berdasarkan jenis penyakit dominan yang terdeteksi (seperti *Late Blight* pada Tomat dan *Rust* pada Jagung).

Dikembangkan sebagai bagian dari Proyek Capstone VANGROVE.
