# VANGROVE: AgroAnalytics Hub & Early Warning System

Sistem pemantauan kesehatan tanaman berbasis AI dan Web-GIS untuk wilayah Sumatera Utara.

## 📁 Struktur Repositori
* `preprocessing.ipynb`: Tahap data gathering dari Kaggle, pembersihan duplikat, dan ekstraksi tabel.
* `feature_engineering.ipynb`: Tahap penambahan fitur geolokasi (Sumut), waktu simulatif, rekomendasi agronomis, dan analisis EDA.
* `cleaned_dataset_final.csv`: Dataset akhir yang sudah siap digunakan untuk Dashboard dan Modeling.

## 📊 Dataset
Dataset citra tanaman menggunakan data sekunder dari Kaggle:
[Kaggle: Data Science Data](https://www.kaggle.com/datasets/pppiiiy/data-science-data)

> **Catatan:** Jangan mengunggah folder citra mentah ke dalam repositori ini karena batasan ukuran file GitHub. Gunakan `base_dataset.csv` untuk referensi path gambar.

## 🚀 Analisis EDA
Kami telah melakukan analisis mendalam terhadap 47.516 baris data citra yang mencakup:
* Sebaran kasus di Kabupaten Karo, Simalungun, Dairi, Langkat, dan Deli Serdang.
* Tren laporan penyakit dari Mei 2024 hingga Mei 2026.
* Identifikasi penyakit dominan seperti Late Blight pada Tomat dan Rust pada Jagung.

---
Dikembangkan sebagai bagian dari Proyek Capstone VANGROVE.
