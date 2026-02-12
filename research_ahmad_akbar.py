"""
Research Visualization Dashboard - Ahmad Akbar 2026
Efektivitas Pembelajaran Berbasis Media Google Sites pada Materi Kelistrikan Otomotif di SMK
Aplikasi visualisasi hasil penelitian dengan Streamlit - POWERFUL & INTERACTIVE
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import scipy.stats as stats
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(
    page_title="Penelitian Ahmad Akbar 2026",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0a1929, #1a237e, #283593);
        color: #e3f2fd;
    }
    .stMetric {
        background: rgba(13,27,42,0.65);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #4caf50;
    }
    h1, h2, h3 {
        color: #64b5f6 !important;
    }
    .highlight-box {
        background: rgba(76,175,80,0.18);
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #4caf50;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Data penelitian Ahmad Akbar
class ResearchDataAhmadAkbar:
    def __init__(self):
        # Data Pretest & Posttest
        self.pretest_data = pd.DataFrame({
            'Statistik': ['Nilai Terendah', 'Nilai Tertinggi', 'Rata-rata', 'Median', 'Standar Deviasi', 'Rentang'],
            'Eksperimen': [53, 61, 57.09, 57.00, 2.29, 8],
            'Kontrol': [46, 57, 51.03, 51.00, 2.76, 11],
            'Kategori_Eks': ['Kurang Baik', 'Kurang Baik', '—', '—', '—', '—'],
            'Kategori_Kon': ['Kurang', 'Kurang Baik', '—', '—', '—', '—']
        })
        
        self.posttest_data = pd.DataFrame({
            'Statistik': ['Nilai Terendah', 'Nilai Tertinggi', 'Rata-rata', 'Median', 'Standar Deviasi', 'Rentang'],
            'Eksperimen': [78, 86, 82.03, 82.00, 2.26, 8],
            'Kontrol': [69, 82, 75.83, 76.00, 3.09, 13],
            'Kategori_Eks': ['Baik', 'Sangat Baik', '—', '—', '—', '—'],
            'Kategori_Kon': ['Cukup', 'Baik', '—', '—', '—', '—']
        })
        
        # Data sampel
        self.sample_data = pd.DataFrame({
            'Kelas': ['XI TKRO A', 'XI TKRO B'],
            'Jumlah Siswa': [32, 35],
            'Kelompok': ['Eksperimen', 'Kontrol'],
            'Perlakuan': ['Google Sites', 'Konvensional']
        })
        
        # Data uji prasyarat
        self.normalitas_data = pd.DataFrame({
            'Uji': ['Kolmogorov-Smirnov', 'Shapiro-Wilk'],
            'Statistic': [0.103, 0.964],
            'df': [32, 32],
            'Sig': [0.200, 0.342],
            'Keputusan': ['Normal', 'Normal']
        })
        
        self.homogenitas_data = pd.DataFrame({
            'Basis': ['Based on Mean', 'Based on Median', 'Based on Median (adjusted)', 'Based on Trimmed Mean'],
            'Levene_Statistic': [2.632, 2.479, 2.479, 2.593],
            'df1': [1, 1, 1, 1],
            'df2': [65, 65, 58.081, 65],
            'Sig': [0.110, 0.120, 0.121, 0.112],
            'Keputusan': ['Homogen', 'Homogen', 'Homogen', 'Homogen']
        })
        
        # Data uji t-test
        self.ttest_data = {
            'assumsi': 'Equal variances assumed',
            't_value': 9.294,
            'df': 65,
            'sig_2tailed': 0.000,
            'mean_difference': 6.203,
            'std_error': 0.667,
            'ci_lower': 4.870,
            'ci_upper': 7.536
        }
        
        # Calculasi N-Gain
        self.ngain_eksperimen = (82.03 - 57.09) / (100 - 57.09)
        self.ngain_kontrol = (75.83 - 51.03) / (100 - 51.03)
        
        # Data perbandingan
        self.comparison_data = pd.DataFrame({
            'Metrik': ['Pretest', 'Posttest', 'Peningkatan', 'N-Gain', 'Kategori N-Gain'],
            'Eksperimen': [57.09, 82.03, 24.94, self.ngain_eksperimen, 'Sedang'],
            'Kontrol': [51.03, 75.83, 24.80, self.ngain_kontrol, 'Sedang']
        })

# Fungsi visualisasi
def create_comparison_bar(data, title, x_col='Statistik', y_cols=['Eksperimen', 'Kontrol']):
    """Bar chart untuk perbandingan"""
    fig = go.Figure()
    
    colors = {'Eksperimen': '#4caf50', 'Kontrol': '#2196f3'}
    
    for col in y_cols:
        fig.add_trace(go.Bar(
            name=col,
            x=data[x_col],
            y=data[col],
            text=data[col].round(2),
            textposition='outside',
            marker=dict(color=colors.get(col, '#64b5f6'))
        ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color='#64b5f6')),
        xaxis_title=x_col,
        yaxis_title='Nilai',
        barmode='group',
        template='plotly_dark',
        height=500,
        plot_bgcolor='rgba(13,27,42,0.65)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig

def create_line_comparison(data, title):
    """Line chart untuk tren"""
    fig = go.Figure()
    
    for col in ['Eksperimen', 'Kontrol']:
        color = '#4caf50' if col == 'Eksperimen' else '#2196f3'
        fig.add_trace(go.Scatter(
            x=data['Metrik'],
            y=data[col],
            mode='lines+markers+text',
            name=col,
            line=dict(color=color, width=3),
            marker=dict(size=12),
            text=data[col].round(2),
            textposition='top center'
        ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color='#64b5f6')),
        template='plotly_dark',
        height=500,
        plot_bgcolor='rgba(13,27,42,0.65)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig

# Main App
def main():
    # Header
    st.title("🎓 Dashboard Penelitian Tesis - Ahmad Akbar")
    st.markdown("### Efektivitas Pembelajaran Berbasis Media Google Sites pada Materi Kelistrikan Otomotif di SMK")
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/250x100/1a237e/ffffff?text=UNM+Makassar", use_container_width=True)
        st.markdown("---")
        st.markdown("### 👨‍🎓 Peneliti")
        st.info("""
        **Ahmad Akbar**  
        NIM: 240020301090
        
        **Pembimbing:**
        I. Prof. Dr. Ir. H. Muh. Yahya, M.Kes., M.Eng., IPU., ASEAN Eng.
        II. Prof. Dr. Darmawang, M.Kes
        
        **Lokasi:**
        SMK Negeri 1 Campalagian
        Kab. Polewali Mandar, Sulawesi Barat
        """)
        
        st.markdown("---")
        menu = st.radio(
            "📊 Navigasi Menu",
            ["Abstrak", "Latar Belakang", "Data Sampel",
             "Hasil Pretest", "Hasil Posttest", "Perbandingan Pre-Post",
             "Analisis N-Gain", "Uji Statistik", "Kesimpulan",
             "📥 Ekspor Data"]
        )
    
    # Inisialisasi data
    research = ResearchDataAhmadAkbar()
    
    # Content
    if menu == "Abstrak":
        st.markdown("""
        <div class="highlight-box">
        <h2>📄 Abstrak Penelitian</h2>
        <p><strong>AHMAD AKBAR, 2026:</strong> "Efektivitas Pembelajaran Berbasis Media Google Sites 
        pada Materi Kelistrikan Otomotif di SMK". Tesis. Program Studi Pendidikan Teknologi Kejuruan. 
        Pascasarjana. Universitas Negeri Makassar.</p>
        
        <p><strong>Kata Kunci:</strong> Google Sites, Media Pembelajaran Digital, Hasil Belajar, 
        Pemeliharaan Kelistrikan Kendaraan Ringan, Pendidikan Kejuruan</p>
        
        <p>Penelitian ini bertujuan untuk mengetahui efektivitas penggunaan media pembelajaran berbasis 
        Google Sites terhadap peningkatan hasil belajar siswa pada mata pelajaran Pemeliharaan Kelistrikan 
        Kendaraan Ringan di SMK. Penelitian ini menggunakan pendekatan kuantitatif dengan metode quasi 
        eksperimen dan desain nonequivalent pretest-posttest control group.</p>
        
        <p><strong>Hasil:</strong> Penggunaan media pembelajaran berbasis Google Sites memberikan pengaruh 
        yang signifikan terhadap peningkatan hasil belajar siswa. Kelas eksperimen memperoleh nilai rata-rata 
        posttest (82,03) dan N-Gain yang lebih tinggi dibandingkan kelas kontrol (75,83).</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Total Sampel", "67 Siswa", "32 Eks + 35 Kon")
        with col2:
            st.metric("📈 Posttest Eksperimen", "82.03", "+24.94 dari pretest")
        with col3:
            st.metric("🎯 N-Gain Eksperimen", f"{research.ngain_eksperimen:.3f}", "Kategori Sedang")
        with col4:
            st.metric("✅ Signifikansi", "p < 0.001", "Sangat Signifikan")
    
    elif menu == "Latar Belakang":
        st.header("🎯 Latar Belakang Penelitian")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="highlight-box">
            <h3>❗ Permasalahan</h3>
            <ul>
            <li>Pembelajaran kelistrikan otomotif masih banyak mengandalkan media sederhana (PowerPoint, poster, buku)</li>
            <li>Pendekatan kurang interaktif dan sulit visualisasi rangkaian listrik</li>
            <li>Akses mandiri dan umpan balik langsung terbatas</li>
            <li>Hasil belajar bervariasi dan peningkatan tidak merata</li>
            <li>Keterbatasan waktu praktik dan akses simulasi</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="highlight-box">
            <h3>✨ Solusi: Google Sites</h3>
            <ul>
            <li>Platform gratis dan mudah dibuat tanpa coding</li>
            <li>Responsif di berbagai perangkat</li>
            <li>Terintegrasi dengan ekosistem Google (YouTube, Forms, Drive)</li>
            <li>Penyajian multimedia dan akses self-paced</li>
            <li>Kolaborasi real-time dan evaluasi formatif</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("🎓 Rumusan Masalah")
        st.markdown("""
        <div class="highlight-box">
        <ol>
        <li>Bagaimana proses penggunaan media pembelajaran berbasis Google Sites pada materi Pemeliharaan 
        Kelistrikan Kendaraan Ringan?</li>
        <li>Bagaimana hasil belajar siswa pada mata pelajaran tersebut?</li>
        <li>Apakah terdapat perbedaan hasil belajar yang signifikan antara siswa yang menggunakan Google Sites 
        dengan pembelajaran konvensional?</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    
    elif menu == "Data Sampel":
        st.header("👥 Data Sampel Penelitian")
        
        # Tabel sampel
        st.dataframe(research.sample_data, use_container_width=True)
        
        # Visualisasi
        fig = go.Figure(data=[
            go.Bar(name='Jumlah Siswa', 
                   x=research.sample_data['Kelas'], 
                   y=research.sample_data['Jumlah Siswa'],
                   text=research.sample_data['Jumlah Siswa'],
                   textposition='outside',
                   marker_color=['#4caf50', '#2196f3'])
        ])
        
        fig.update_layout(
            title="Distribusi Sampel Penelitian",
            template='plotly_dark',
            height=400,
            plot_bgcolor='rgba(13,27,42,0.65)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.success("""
            **Kelas Eksperimen (XI TKRO A)**
            - Jumlah: 32 siswa
            - Perlakuan: Google Sites
            - Media interaktif dengan video, diagram, kuis
            """)
        with col2:
            st.info("""
            **Kelas Kontrol (XI TKRO B)**
            - Jumlah: 35 siswa
            - Perlakuan: Konvensional
            - Ceramah, diskusi, lembar kerja
            """)
    
    elif menu == "Hasil Pretest":
        st.header("📝 Hasil Pretest - Kemampuan Awal")
        
        # Tabel
        st.dataframe(research.pretest_data, use_container_width=True)
        
        # Visualisasi
        fig = create_comparison_bar(
            research.pretest_data, 
            "Perbandingan Statistik Pretest"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Rata-rata Eksperimen", "57.09", delta="Kurang Baik")
            st.info("""
            - Nilai terendah: 53
            - Nilai tertinggi: 61
            - Median: 57.00
            - Std Dev: 2.29 (homogen)
            """)
        
        with col2:
            st.metric("Rata-rata Kontrol", "51.03", delta="Kurang Baik")
            st.info("""
            - Nilai terendah: 46
            - Nilai tertinggi: 57
            - Median: 51.00
            - Std Dev: 2.76
            """)
        
        st.warning("⚠️ Kemampuan awal kedua kelompok setara dengan kategori Kurang Baik")
    
    elif menu == "Hasil Posttest":
        st.header("📝 Hasil Posttest - Setelah Perlakuan")
        
        # Tabel
        st.dataframe(research.posttest_data, use_container_width=True)
        
        # Visualisasi
        fig = create_comparison_bar(
            research.posttest_data,
            "Perbandingan Statistik Posttest"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Rata-rata Eksperimen", "82.03", delta="+24.94 poin", delta_color="normal")
            st.success("""
            - Nilai terendah: 78 (Baik)
            - Nilai tertinggi: 86 (Sangat Baik)
            - Median: 82.00
            - Std Dev: 2.26 (sangat homogen!)
            - Rentang: hanya 8 poin
            """)
        
        with col2:
            st.metric("Rata-rata Kontrol", "75.83", delta="+24.80 poin", delta_color="normal")
            st.info("""
            - Nilai terendah: 69 (Cukup)
            - Nilai tertinggi: 82 (Baik)
            - Median: 76.00
            - Std Dev: 3.09
            - Rentang: 13 poin
            """)
        
        st.success("✅ Kelas eksperimen mencapai kategori Baik dengan hasil sangat homogen")
    
    elif menu == "Perbandingan Pre-Post":
        st.header("📊 Perbandingan Pretest → Posttest")
        
        # Line chart
        fig = create_line_comparison(
            research.comparison_data[research.comparison_data['Metrik'].isin(['Pretest', 'Posttest'])],
            "Tren Peningkatan Hasil Belajar"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabel perbandingan
        st.subheader("📋 Ringkasan Perbandingan")
        st.dataframe(research.comparison_data, use_container_width=True)
        
        # Metrics peningkatan
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Peningkatan Eksperimen", "+24.94", "57.09 → 82.03")
        with col2:
            st.metric("Peningkatan Kontrol", "+24.80", "51.03 → 75.83")
        with col3:
            st.metric("Selisih Posttest", "+6.20", "Eksperimen lebih tinggi")
    
    elif menu == "Analisis N-Gain":
        st.header("📈 Analisis N-Gain (Normalized Gain)")
        
        st.markdown("""
        <div class="highlight-box">
        <h3>📊 Tentang N-Gain</h3>
        <p><strong>N-Gain = (Posttest - Pretest) / (100 - Pretest)</strong></p>
        <p>Kategori: Tinggi (≥0.7), Sedang (0.3-0.69), Rendah (<0.3)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Visualisasi N-Gain
        fig = go.Figure(data=[
            go.Bar(
                x=['Eksperimen', 'Kontrol'],
                y=[research.ngain_eksperimen, research.ngain_kontrol],
                text=[f"{research.ngain_eksperimen:.3f}", f"{research.ngain_kontrol:.3f}"],
                textposition='outside',
                marker_color=['#4caf50', '#2196f3']
            )
        ])
        
        fig.update_layout(
            title="Perbandingan N-Gain Score",
            yaxis_title="N-Gain",
            template='plotly_dark',
            height=500,
            plot_bgcolor='rgba(13,27,42,0.65)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrics
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"""
            **Kelas Eksperimen**
            - N-Gain: {research.ngain_eksperimen:.3f}
            - Kategori: Sedang
            - Persentase: {research.ngain_eksperimen*100:.1f}%
            """)
        
        with col2:
            st.info(f"""
            **Kelas Kontrol**
            - N-Gain: {research.ngain_kontrol:.3f}
            - Kategori: Sedang
            - Persentase: {research.ngain_kontrol*100:.1f}%
            """)
        
        st.warning(f"📌 Selisih N-Gain: {(research.ngain_eksperimen - research.ngain_kontrol):.3f} (Eksperimen lebih tinggi)")
    
    elif menu == "Uji Statistik":
        st.header("🔬 Hasil Uji Statistik")
        
        # Uji Normalitas
        st.subheader("1️⃣ Uji Normalitas (Posttest)")
        st.dataframe(research.normalitas_data, use_container_width=True)
        st.success("✅ Data berdistribusi normal (p > 0.05) → Layak uji parametrik")
        
        # Uji Homogenitas
        st.subheader("2️⃣ Uji Homogenitas Varians (Levene's Test)")
        st.dataframe(research.homogenitas_data, use_container_width=True)
        st.success("✅ Varians homogen (p > 0.05) → Asumsi terpenuhi")
        
        # Uji t-Test
        st.subheader("3️⃣ Independent Samples t-Test")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("t-value", f"{research.ttest_data['t_value']:.3f}")
        with col2:
            st.metric("Sig. (2-tailed)", f"{research.ttest_data['sig_2tailed']:.3f}", "< 0.05")
        with col3:
            st.metric("Mean Difference", f"{research.ttest_data['mean_difference']:.3f}")
        
        # Visualisasi t-test
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['t-statistic'],
            y=[research.ttest_data['t_value']],
            text=[f"{research.ttest_data['t_value']:.3f}"],
            textposition='outside',
            marker_color='#4caf50'
        ))
        
        fig.update_layout(
            title=f"t = {research.ttest_data['t_value']:.3f}, p = {research.ttest_data['sig_2tailed']:.3f} → SIGNIFIKAN ✓",
            template='plotly_dark',
            height=400,
            plot_bgcolor='rgba(13,27,42,0.65)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Kesimpulan
        st.markdown(f"""
        <div class="highlight-box">
        <h2 style="text-align:center; color:#4caf50;">✅ H₀ DITOLAK - ADA PERBEDAAN SIGNIFIKAN</h2>
        <p style="text-align:center; font-size:1.2em;">
        Karena p-value ({research.ttest_data['sig_2tailed']:.3f}) < α (0.05), maka H₀ ditolak.
        </p>
        <p style="text-align:center; font-size:1.2em;">
        <strong>Kesimpulan:</strong> Media pembelajaran berbasis Google Sites secara signifikan lebih efektif 
        meningkatkan hasil belajar siswa dibandingkan metode konvensional pada mata pelajaran Pemeliharaan 
        Kelistrikan Kendaraan Ringan.
        </p>
        <p style="text-align:center;">
        Confidence Interval (95%): [{research.ttest_data['ci_lower']:.3f}, {research.ttest_data['ci_upper']:.3f}]
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    elif menu == "Kesimpulan":
        st.header("🎯 Kesimpulan Penelitian")
        
        st.markdown("""
        <div class="highlight-box">
        <h2>📋 Kesimpulan Utama</h2>
        
        <h3>1️⃣ Proses Pembelajaran dengan Google Sites</h3>
        <p>Media pembelajaran berbasis Google Sites dapat digunakan dengan baik pada materi Pemeliharaan 
        Kelistrikan Kendaraan Ringan. Platform ini memungkinkan penyajian materi secara interaktif, 
        multimedia (video, diagram), dan terintegrasi dengan kuis Google Form.</p>
        
        <h3>2️⃣ Peningkatan Hasil Belajar Signifikan</h3>
        <ul>
        <li>Kelas Eksperimen: Pretest 57.09 → Posttest 82.03 (+24.94)</li>
        <li>Kelas Kontrol: Pretest 51.03 → Posttest 75.83 (+24.80)</li>
        <li>N-Gain Eksperimen: 0.581 (Sedang) vs Kontrol: 0.507 (Sedang)</li>
        <li>Posttest eksperimen 6.20 poin lebih tinggi</li>
        </ul>
        
        <h3>3️⃣ Perbedaan Statistik Signifikan</h3>
        <p><strong>Uji Independent t-Test:</strong></p>
        <ul>
        <li>t-value = 9.294</li>
        <li>p-value = 0.000 < 0.05 (Sangat Signifikan)</li>
        <li>Mean difference = 6.203 poin</li>
        <li>Kesimpulan: H₀ ditolak → Google Sites lebih efektif</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("💡 Implikasi Penelitian")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="highlight-box">
            <h3>🎓 Untuk Pendidik</h3>
            <ul>
            <li>Adopsi Google Sites untuk pembelajaran kelistrikan</li>
            <li>Integrasikan multimedia dan kuis interaktif</li>
            <li>Manfaatkan akses mandiri dan self-paced learning</li>
            <li>Tingkatkan literasi digital guru</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="highlight-box">
            <h3>🏫 Untuk Institusi SMK</h3>
            <ul>
            <li>Sediakan pelatihan penggunaan Google Sites</li>
            <li>Fasilitasi infrastruktur internet memadai</li>
            <li>Kembangkan bank konten digital</li>
            <li>Dorong inovasi media pembelajaran</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Final message
        st.markdown("---")
        st.markdown("""
        <h1 style="text-align:center; color:#4caf50; font-size:3em; margin:40px 0;">
        ✨ TERIMA KASIH ✨
        </h1>
        <p style="text-align:center; font-size:1.5em;">
        <strong>Ahmad Akbar</strong><br>
        NIM: 240020301090<br>
        Program Studi Pendidikan Teknologi Kejuruan<br>
        Pascasarjana - Universitas Negeri Makassar<br>
        2026
        </p>
        """, unsafe_allow_html=True)
    
    elif menu == "📥 Ekspor Data":
        st.header("📥 Ekspor Data Penelitian")
        
        st.info("💾 Download data penelitian dalam format Excel atau CSV")
        
        # Export Excel
        from io import BytesIO
        import openpyxl
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            research.sample_data.to_excel(writer, sheet_name='Sampel', index=False)
            research.pretest_data.to_excel(writer, sheet_name='Pretest', index=False)
            research.posttest_data.to_excel(writer, sheet_name='Posttest', index=False)
            research.comparison_data.to_excel(writer, sheet_name='Perbandingan', index=False)
            research.normalitas_data.to_excel(writer, sheet_name='Uji Normalitas', index=False)
            research.homogenitas_data.to_excel(writer, sheet_name='Uji Homogenitas', index=False)
        
        output.seek(0)
        
        st.download_button(
            label="📊 Download Semua Data (Excel)",
            data=output,
            file_name=f"penelitian_ahmad_akbar_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Dataset", "6 sheets")
        with col2:
            st.metric("Total Sampel", "67 siswa")
        with col3:
            st.metric("Lokasi", "SMKN 1 Campalagian")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding:20px; color:#90caf9;">
    <p>© 2026 Ahmad Akbar | Universitas Negeri Makassar</p>
    <p>Dashboard Visualisasi Penelitian - Efektivitas Google Sites dalam Pembelajaran Kelistrikan Otomotif</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
