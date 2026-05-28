import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman Dasar
st.set_page_config(
    page_title="VANGROVE Dashboard",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 VANGROVE")
st.markdown("Sistem pemantauan kesehatan tanaman untuk wilayah Provinsi Sumatera Utara")
st.markdown("---")

# 2. Memuat Data
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/cleaned_dataset_final.csv")
    df['date'] = pd.to_datetime(df['date'])
    # Mengubah format penamaan penyakit menjadi Title Case dan menghapus underscore (_)
    df['disease'] = df['disease'].astype(str).str.replace('_', ' ', regex=False).str.title()
    # Mengubah format penamaan tanaman menjadi Title Case
    df['plant'] = df['plant'].astype(str).str.title()
    return df

df = load_data()

# 3. Menggunakan seluruh data tanpa filter
df_filtered = df.copy()

# 4. Menampilkan Metrik Berdasarkan Filter
col1, col2, col3 = st.columns(3)
col1.metric("Total Kasus Laporan", f"{len(df_filtered):,}")
col2.metric("Jumlah Lokasi", df_filtered['location'].nunique())
col3.metric("Jumlah Penyakit Terdeteksi", df_filtered['disease'].nunique())

st.markdown("---")

# 5. MEMBAGI HALAMAN MENJADI 5 TAB
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ Peta Sebaran (Web-GIS)", 
    "📈 Tren Waktu (EWS)", 
    "📊 Analisis Bisnis & EDA", 
    "💡 Solusi & Rekomendasi", 
    "📋 Data Mentah"
])

# --- TAB 1: PETA WEB-GIS ---
with tab1:
    st.subheader("🗺️ Peta Sebaran Kasus Penyakit di Sumatera Utara")
    if not df_filtered.empty:
        # Warna peta dikembalikan berdasarkan 'plant' karena tanaman bisa dipilih banyak
        df_filtered['disease_label'] = df_filtered['disease'].apply(
            lambda x: 'Healthy' if x.lower() == 'healthy' else f'<b>Penyakit:</b> {x.title()}'
        )

        df_filtered['plant'] = df_filtered['plant'].str.title()

        fig_map = px.scatter_mapbox(
            df_filtered, lat="lat", lon="lon", color="plant",
            size_max=12, zoom=7.5, mapbox_style="open-street-map",
            hover_name="location",
            hover_data={"plant": False, "disease": False, "condition": False, "lat": False, "lon": False},
            height=600,
            custom_data=['plant', 'disease_label']
        )

        fig_map.update_traces(
            hovertemplate=
            "<b>Kabupaten:</b> %{hovertext}<br>" +
            "<b>Tanaman:</b> %{customdata[0]}<br>" +
            "%{customdata[1]}<extra></extra>"
        )

        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("⚠️ Tidak ada data untuk kombinasi filter yang dipilih.")

# --- TAB 2: TREN WAKTU (EARLY WARNING SYSTEM) ---
with tab2:
    st.subheader("📈 Analisis Tren Laporan Kasus Bulanan")

    if not df_filtered.empty:

        # Grouping data tren bulanan
        tren_data = (
            df_filtered
            .groupby([pd.Grouper(key='date', freq='MS'), 'disease'])
            .size()
            .reset_index(name='Jumlah Kasus')
        )

        # Mapping disease -> plant
        plant_map = (
            df_filtered[['disease', 'plant']]
            .drop_duplicates()
        )

        # Merge informasi tanaman
        tren_data = tren_data.merge(
            plant_map,
            on='disease',
            how='left'
        )

        # Title Case
        tren_data['disease'] = tren_data['disease'].str.title()
        tren_data['plant'] = tren_data['plant'].str.title()

        tren_data['disease_label'] = tren_data['disease'].apply(
            lambda x: 'Healthy' if x == 'Healthy' else f'<b>Penyakit:</b> {x}'
        )

        # Membuat line chart
        fig_line = px.line(
            tren_data,
            x='date',
            y='Jumlah Kasus',
            color='disease',
            markers=True,
            line_shape='spline',

            custom_data=['plant', 'disease_label'],

            labels={
                'plant': 'Tanaman',
                'disease': 'Penyakit',
                'date': 'Tanggal',
                'Jumlah Kasus': 'Jumlah Kasus'
            }
        )

        fig_line.update_traces(
            hovertemplate=
            "<b>Tanaman:</b> %{customdata[0]}<br>" +
            "%{customdata[1]}<br>" +
            "<b>Bulan:</b> %{x|%b %Y}<br>" +
            "<b>Jumlah Kasus:</b> %{y}<extra></extra>"
        )

        # Layout chart
        fig_line.update_layout(
            xaxis_title="Bulan",
            yaxis_title="Jumlah Kasus",
            hovermode="closest"
        )

        st.plotly_chart(fig_line, use_container_width=True)

    else:
        st.warning("⚠️ Tidak ada data untuk kombinasi filter yang dipilih.")

# --- TAB 3: ANALISIS BISNIS & EDA ---
with tab3:
    st.subheader("📊 Analisis Komprehensif (Menjawab Pertanyaan Bisnis)")
    
    if not df_filtered.empty:

        # Title Case
        df_filtered['plant'] = df_filtered['plant'].str.title()
        df_filtered['disease'] = df_filtered['disease'].str.title()
        df_filtered['location'] = df_filtered['location'].str.title()
        
        colA, colB = st.columns(2)
        
        with colA:
            # Grafik 1: Kembali menampilkan proporsi perbandingan antar jenis tanaman
            st.markdown("**1. Proporsi Kasus Berdasarkan Jenis Tanaman**")
            plant_count = df_filtered['plant'].value_counts().reset_index()
            plant_count.columns = ['Tanaman', 'Jumlah Kasus']

            fig_plant = px.pie(
                plant_count,
                values='Jumlah Kasus',
                names='Tanaman',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )

            # Hover custom
            fig_plant.update_traces(
                hovertemplate=
                "<b>Tanaman:</b> %{label}<br>" +
                "<b>Jumlah Kasus:</b> %{value}<br>" +
                "<b>Persentase:</b> %{percent}<extra></extra>"
            )

            st.plotly_chart(fig_plant, use_container_width=True)
            
        with colB:
            # Grafik 2: wilayah
            st.markdown("**2. Sebaran Kasus per Wilayah (Kabupaten)**")
            loc_count = df_filtered['location'].value_counts().reset_index()
            loc_count.columns = ['Lokasi', 'Jumlah Kasus']
            fig_loc = px.bar(
                loc_count,
                x='Lokasi',
                y='Jumlah Kasus',
                color='Lokasi',
                text_auto=True
            )

            fig_loc.update_layout(showlegend=False, yaxis_tickformat=",")

            # Hover custom
            fig_loc.update_traces(
                hovertemplate=
                "<b>Kabupaten:</b> %{x}<br>" +
                "<b>Jumlah Kasus:</b> %{y:,}<extra></extra>",

                texttemplate='%{y:,}'
            )

            st.plotly_chart(fig_loc, use_container_width=True)

        st.markdown("---")
        
        # Grafik 3: Menampilkan distribusi penyakit spesifik
        st.markdown("**3. Distribusi Kasus Berdasarkan Jenis Penyakit (Spesifik)**")

        # Mengecualikan Healthy (karena tidak termasuk ke penyakit)
        penyakit_filtered = df_filtered[df_filtered['disease'] != 'Healthy']
        penyakit_count = (
            penyakit_filtered
            .groupby(['disease', 'plant'])
            .size()
            .reset_index(name='Jumlah Kasus')
        )

        penyakit_count.columns = ['Penyakit', 'Tanaman', 'Jumlah Kasus']
        fig_bar = px.bar(
            penyakit_count,
            x='Jumlah Kasus',
            y='Penyakit',
            color='Penyakit',
            orientation='h',
            text_auto=True,
            custom_data=['Tanaman']
        )

        fig_bar.update_layout(
            yaxis={'categoryorder':'total ascending'},
            showlegend=False
        )

        # Hover custom
        fig_bar.update_traces(
            hovertemplate=
            "<b>Tanaman:</b> %{customdata[0]}<br>" +
            "<b>Penyakit:</b> %{y}<br>" +
            "<b>Jumlah Kasus:</b> %{x}<extra></extra>"
        )

        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("⚠️ Tidak ada data untuk kombinasi filter yang dipilih.")

# --- TAB 4: SOLUSI & REKOMENDASI (AKSI OPSI B) ---
with tab4:
    st.subheader("💡 Panduan Penanganan Agronomis")
    if not df_filtered.empty:
        # Mengambil kombinasi unik yang berpasangan antara Jenis Tanaman dan Jenis Penyakit
        kombinasi_unik = df_filtered[['plant', 'disease']].drop_duplicates().sort_values(by=['plant', 'disease'])
        
        for _, row in kombinasi_unik.iterrows():
            t_nama = row['plant']
            p_nama = row['disease']
            
            # Mengambil data baris pertama yang cocok dengan kombinasi tanaman & penyakit tersebut
            sampel = df_filtered[(df_filtered['plant'] == t_nama) & (df_filtered['disease'] == p_nama)].iloc[0]
            kondisi = sampel['condition']
            rekomendasi = sampel['recommendation']
            
            # Menggabungkan nama tanaman dan nama penyakit di bagian Header Expander 
            label_penyakit = (
                f"Penyakit {p_nama}"
                if p_nama != "Healthy"
                else "Healthy"
            )

            with st.expander(
                f"🛠️ Tindakan untuk: Tanaman **{t_nama}** - **{label_penyakit}**"
            ):
                st.write(f"**Pemicu Lingkungan:** {kondisi}")
                st.info(f"**Saran Penanganan:** {rekomendasi}")
    else:
        st.warning("⚠️ Tidak ada data untuk kombinasi filter yang dipilih.")

# --- TAB 5: TABEL DATA ---
with tab5:
    st.subheader("📋 Detail Data Kasus")
    st.dataframe(df_filtered)