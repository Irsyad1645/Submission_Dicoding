# Bike Sharing Dashboard 🚲

Dashboard interaktif untuk mengeksplorasi dan menganalisis data penyewaan sepeda (*Bike Sharing Dataset*) menggunakan Python dan Streamlit.

## 🌐 Live Dashboard

Akses dashboard melalui tautan berikut:

**[Bike Sharing Dashboard — Streamlit] **
(https://dashboard-irsyad.streamlit.app/)


## 📌 Deskripsi Proyek

Proyek ini menyajikan analisis data penyewaan sepeda dalam dashboard interaktif. Dashboard dibuat menggunakan Streamlit agar pengguna dapat melihat visualisasi dan mengeksplorasi informasi dari data dengan lebih mudah.

Analisis berfokus pada pola penyewaan sepeda berdasarkan waktu, kondisi cuaca, dan musim. Proyek ini menggunakan analisis data dan visualisasi, bukan model machine learning.

## 🎯 Pertanyaan Bisnis

1. Pada jam berapa puncak penyewaan terjadi pada hari kerja dibandingkan hari non-kerja, dan berapa rata-rata penyewaan per jam pada jam puncak tersebut selama 2011–2012?
2. Berapa persen penurunan rata-rata penyewaan harian saat cuaca berkabut atau hujan/salju ringan dibandingkan cuaca cerah?
3. Pada musim apa rata-rata penyewaan harian tertinggi dan terendah selama 2011–2012?

## 🔎 Analisis yang Dilakukan

- Membandingkan pola penyewaan sepeda per jam pada hari kerja dan hari non-kerja.
- Menganalisis rata-rata penyewaan berdasarkan kondisi cuaca.
- Membandingkan rata-rata penyewaan harian berdasarkan musim.
- Menggunakan *manual grouping* untuk mengelompokkan segmen waktu.
- Menggunakan *binning* untuk mengelompokkan suhu dan tingkat permintaan.
- Menampilkan hasil analisis melalui dashboard interaktif Streamlit.

## 🧰 Tools dan Teknologi

- **Python** — bahasa pemrograman untuk analisis data.
- **Pandas** — membaca dan mengolah dataset.
- **Streamlit** — membangun dashboard interaktif.
- **Joblib** — memuat objek atau data tersimpan apabila digunakan oleh aplikasi.
- **CSV** — format penyimpanan dataset.
- **GitHub** — menyimpan kode sumber proyek.

## 📁 Struktur File

```text
submission/
├── dashboard.py       # Kode utama dashboard Streamlit
├── requirements.txt   # Daftar library Python
└── viz_data.joblib    # File data/objek pendukung dashboard
```

Struktur di atas mengikuti file yang digunakan untuk deployment. Jika kode membutuhkan file tambahan, file tersebut juga harus tersedia di repository.

## ⚙️ Instalasi dan Menjalankan Secara Lokal

### Menggunakan Anaconda

```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

### Menggunakan Shell/Terminal dengan Pipenv

Jalankan dari direktori proyek yang berisi `dashboard.py` dan `requirements.txt`:

```bash
pipenv install
pipenv shell
pip install -r requirements.txt
```

### Menjalankan dashboard

```bash
streamlit run dashboard.py
```

Dashboard lokal dapat dibuka melalui `http://localhost:8501`.

## ☁️ Deployment

Dashboard dipublikasikan melalui Streamlit Community Cloud dan dapat diakses secara online melalui:

https://dashboard-irsyad.streamlit.app/

## 📊 Dataset

Dataset yang digunakan adalah **Bike Sharing Dataset** dari UCI Machine Learning Repository, yang memuat data penyewaan sepeda pada tahun 2011–2012.

Sumber: [UCI Bike Sharing Dataset](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset)

Referensi publikasi dataset:

Fanaee-T, H. dan Gama, J. (2013). *Event labeling combining ensemble detectors and background knowledge*. Progress in Artificial Intelligence.

