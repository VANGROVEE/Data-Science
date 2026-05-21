import streamlit as st
import pandas as pd
import plotly.express as px

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

# 5. MEMBAGI HALAMAN MENJADI 5 TAB (Tambah Tab Solusi)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ Peta Sebaran (Web-GIS)", 
    "📈 Tren Waktu (EWS)", 
    "📊 Distribusi Penyakit", 
    "💡 Solusi & Rekomendasi",  # <-- TAB BARU KITA
    "📋 Data Mentah"
])

# --- TAB 1: PETA WEB-GIS ---
with tab1:
    st.subheader("🗺️ Peta Sebaran Kasus Penyakit di Sumatera Utara")
    if not df_filtered.empty:
        fig_map = px.scatter_mapbox(
            df_filtered, lat="lat", lon="lon", color="plant",
            size_max=12, zoom=7.5, mapbox_style="open-street-map",
            hover_name="location",
            hover_data={"plant": True, "disease": True, "condition": False, "lat": False, "lon": False},
            height=600
        )
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("⚠️ Tidak ada data untuk kombinasi filter yang dipilih.")

# --- TAB 2: TREN WAKTU (EARLY WARNING SYSTEM) ---
with tab2:
    st.subheader("📈 Analisis Tren Laporan Kasus Bulanan")
    if not df_filtered.empty:
        tren_data = df_filtered.groupby([pd.Grouper(key='date', freq='ME'), 'disease']).size().reset_index(name='Jumlah Kasus')
        fig_line = px.line(tren_data, x='date', y='Jumlah Kasus', color='disease', markers=True, line_shape='spline')
        fig_line.update_layout(xaxis_title="Bulan", yaxis_title="Jumlah Kasus", hovermode="x unified")
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.warning("⚠️ Tidak ada data untuk kombinasi filter yang dipilih.")

# --- TAB 3: GRAFIK BATANG ---
with tab3:
    st.subheader("📊 Distribusi Kasus Berdasarkan Penyakit")
    penyakit_count = df_filtered['disease'].value_counts().reset_index()
    penyakit_count.columns = ['Penyakit', 'Jumlah Kasus']
    fig_bar = px.bar(penyakit_count, x='Penyakit', y='Jumlah Kasus', color='Penyakit')
    st.plotly_chart(fig_bar, use_container_width=True)

# --- TAB 4: SOLUSI & REKOMENDASI (ACTIONABLE INSIGHTS) ---
with tab4:
    st.subheader("💡 Panduan Penanganan Agronomis")
    st.markdown("Rekomendasi tindakan respons cepat berdasarkan penyakit yang terdeteksi dari filter Anda saat ini.")
    
    if not df_filtered.empty:
        # Mengambil daftar penyakit unik yang sedang terfilter
        penyakit_unik = df_filtered['disease'].unique()
        
        for p in penyakit_unik:
            # Mengambil 1 baris sampel untuk setiap penyakit guna mendapatkan kondisi & rekomendasinya
            sampel = df_filtered[df_filtered['disease'] == p].iloc[0]
            kondisi = sampel['condition']
            rekomendasi = sampel['recommendation']
            
            # Membuat kotak (expander) yang rapi untuk setiap penyakit
            with st.expander(f"🛠️ Tindakan untuk: **{p}**"):
                st.write(f"**Pemicu Lingkungan:** {kondisi}")
                st.info(f"**Saran Penanganan:** {rekomendasi}")
    else:
        st.warning("⚠️ Tidak ada data untuk kombinasi filter yang dipilih.")

# --- TAB 5: TABEL DATA ---
with tab5:
    st.subheader("📋 Detail Data Kasus")
    st.dataframe(df_filtered)