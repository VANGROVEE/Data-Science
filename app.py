import streamlit as st
import pandas as pd
import plotly.express as px  # <-- Tambahkan import ini

# 1. Konfigurasi Halaman Dasar
st.set_page_config(
    page_title="VANGROVE Dashboard",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 VANGROVE: AgroAnalytics Hub")
st.markdown("Sistem pemantauan kesehatan tanaman untuk wilayah Sumatera Utara.")
st.markdown("---")

# 2. Memuat Data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_dataset_final.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# 3. Membuat Sidebar untuk Filter Interaktif
st.sidebar.header("🔍 Filter Data")

lokasi_pilihan = st.sidebar.multiselect(
    "Pilih Kabupaten/Kota:",
    options=df['location'].unique(),
    default=df['location'].unique()
)

tanaman_pilihan = st.sidebar.multiselect(
    "Pilih Jenis Tanaman:",
    options=df['plant'].unique(),
    default=df['plant'].unique()
)

df_filtered = df[(df['location'].isin(lokasi_pilihan)) & (df['plant'].isin(tanaman_pilihan))]

# 4. Menampilkan Metrik Berdasarkan Filter
col1, col2, col3 = st.columns(3)
col1.metric("Total Kasus Laporan", f"{len(df_filtered):,}")
col2.metric("Jumlah Lokasi", df_filtered['location'].nunique())
col3.metric("Jumlah Penyakit Terdeteksi", df_filtered['disease'].nunique())

st.markdown("---")

# 5. MEMBAGI HALAMAN MENJADI TAB
tab1, tab2, tab3 = st.tabs(["🗺️ Peta Sebaran (Web-GIS)", "📊 Distribusi Penyakit", "📋 Data Mentah"])

# --- TAB 1: PETA WEB-GIS (VERSI LEBIH JELAS & BERWARNA) ---
with tab1:
    st.subheader("🗺️ Peta Sebaran Kasus Penyakit di Sumatera Utara")
    st.markdown("Titik penanda diwarnai berdasarkan **Jenis Tanaman** untuk mempermudah analisis visual di setiap daerah.")
    
    if not df_filtered.empty:
        # Membuat peta interaktif dengan Plotly Express
        fig = px.scatter_mapbox(
            df_filtered,
            lat="lat",
            lon="lon",
            color="plant",           # <-- Titik otomatis berwarna-warni berdasarkan jenis tanaman
            size_max=12,
            zoom=7.5,                # <-- Mengatur tingkat kedekatan kamera peta
            mapbox_style="open-street-map",  # <-- Gaya peta terang, jelas, dan penuh warna
            hover_name="location",   # <-- Memunculkan nama Kabupaten saat kursor digeser ke titik
            hover_data={             # <-- Informasi tambahan saat titik didekati kursor
                "plant": True,
                "disease": True,
                "condition": True,
                "lat": False,        # Menyembunyikan angka koordinat mentah agar rapi
                "lon": False
            },
            height=600               # <-- Mengatur tinggi peta di halaman web
        )
        
        # Menghilangkan margin kosong di sekitar peta agar terlihat penuh dan rapi
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
        # Menampilkan peta ke aplikasi Streamlit
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Tidak ada data untuk kombinasi filter yang dipilih.")

# --- TAB 2: GRAFIK BATANG ---
with tab2:
    st.subheader("📊 Distribusi Kasus Berdasarkan Penyakit")
    penyakit_count = df_filtered['disease'].value_counts().reset_index()
    penyakit_count.columns = ['Penyakit', 'Jumlah Kasus']
    st.bar_chart(data=penyakit_count, x='Penyakit', y='Jumlah Kasus')

# --- TAB 3: TABEL DATA ---
with tab3:
    st.subheader("📋 Detail Data Kasus")
    st.dataframe(df_filtered)