import streamlit as st
import pandas as pd
import datetime
import json
import os
import matplotlib.pyplot as plt

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Sistem Pencatatan & Pelaporan TPMB (Kemenkes RI)",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 26px;
        font-weight: bold;
        color: #1E3A8A;
        border-bottom: 2px solid #3B82F6;
        padding-bottom: 8px;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 18px;
        font-weight: bold;
        color: #1F2937;
        margin-top: 15px;
    }
    .stButton>button {
        background-color: #2563EB;
        color: white;
        font-weight: bold;
        border-radius: 6px;
    }
    .badge-info {
        background-color: #E0F2FE;
        color: #0369A1;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# File Penyimpanan Data Sederhana (JSON)
DATA_FILE = "data_tpmb.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {"persalinan": [], "nifas": [], "neonatus": [], "homecare": [], "rujukan": []}
    return {"persalinan": [], "nifas": [], "neonatus": [], "homecare": [], "rujukan": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4, default=str)

db = load_data()

# Sidebar Navigation
st.sidebar.title("🩺 Aplikasi TPMB Kemenkes")
st.sidebar.caption("Standar Pencatatan & Pelaporan Kebidanan")

menu = st.sidebar.radio(
    "Pilih Modul Pelayanan:",
    [
        "🏠 Dashboard & Rekapitulasi",
        "🤰 Pendokumentasian Persalinan",
        "📈 Pemantauan Partograf",
        "🤱 Asuhan Nifas (KF)",
        "👶 Pelayanan Neonatus (KN)",
        "🏡 Kunjungan Rumah (Home Care)",
        "🚑 Rujukan Maternal & Neonatal"
    ]
)

# ==========================================
# 1. DASHBOARD & REKAPITULASI
# ==========================================
if menu == "🏠 Dashboard & Rekapitulasi":
    st.markdown("<div class='main-header'>🏠 Dashboard Pelaporan & Rekapitulasi TPMB</div>", unsafe_allow_html=True)
    st.info("Aplikasi Pencatatan dan Pelaporan Mandiri Bidan sesuai Standar Permenkes No. 21 Tahun 2021 & Panduan Kemenkes RI.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Persalinan", len(db.get("persalinan", [])))
    with col2:
        st.metric("Kunjungan Nifas (KF)", len(db.get("nifas", [])))
    with col3:
        st.metric("Pelayanan Neonatus (KN)", len(db.get("neonatus", [])))
    with col4:
        st.metric("Kasus Rujukan", len(db.get("rujukan", [])))

    st.markdown("<div class='sub-header'>📊 Rekapitulasi Data Registrasi TPMB</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Persalinan", "Asuhan Nifas", "Pelayanan Neonatus", "Rujukan"])
    
    with tab1:
        if db.get("persalinan"):
            df = pd.DataFrame(db["persalinan"])
            st.dataframe(df, use_container_width=True)
        else:
            st.write("Belum ada data persalinan tersimpan.")
            
    with tab2:
        if db.get("nifas"):
            df = pd.DataFrame(db["nifas"])
            st.dataframe(df, use_container_width=True)
        else:
            st.write("Belum ada data kunjungan nifas tersimpan.")

    with tab3:
        if db.get("neonatus"):
            df = pd.DataFrame(db["neonatus"])
            st.dataframe(df, use_container_width=True)
        else:
            st.write("Belum ada data pelayanan neonatus tersimpan.")

    with tab4:
        if db.get("rujukan"):
            df = pd.DataFrame(db["rujukan"])
            st.dataframe(df, use_container_width=True)
        else:
            st.write("Belum ada data rujukan tersimpan.")

# ==========================================
# 2. PENDOKUMENTASIAN PERSALINAN
# ==========================================
elif menu == "🤰 Pendokumentasian Persalinan":
    st.markdown("<div class='main-header'>🤰 Pendokumentasian Persalinan (Kala I - IV)</div>", unsafe_allow_html=True)
    st.caption("Standardisasi Asuhan Persalinan Normal (APN) & Rekam Medis Kebidanan")

    with st.form("form_persalinan"):
        st.markdown("### A. Data Ibu & Registrasi RM")
        c1, c2, c3 = st.columns(3)
        with c1:
            no_rm = st.text_input("No. Rekam Medis", value="RM-2026-001")
            nama_ibu = st.text_input("Nama Ibu", value="Ny. Anisa")
            umur_ibu = st.number_input("Umur Ibu (Tahun)", min_value=15, max_value=50, value=26)
        with c2:
            gravida = st.number_input("Gravida (G)", min_value=1, value=1)
            partus = st.number_input("Partus (P)", min_value=0, value=0)
            abortus = st.number_input("Abortus (A)", min_value=0, value=0)
        with c3:
            hpht = st.date_input("HPHT", value=datetime.date(2026, 1, 1))
            tp = st.date_input("Taksiran Persalinan (TP)", value=datetime.date(2026, 10, 8))
            alamat = st.text_area("Alamat / Kontak", value="Jl. Merdeka No. 12")

        st.markdown("### B. Evaluasi Kala II (Persalinan Bayi)")
        c1, c2, c3 = st.columns(3)
        with c1:
            tgl_lahir = st.date_input("Tanggal Persalinan", value=datetime.date.today())
            jam_lahir = st.time_input("Jam Kelahiran", value=datetime.time(8, 30))
        with c2:
            jenis_persalinan = st.selectbox("Jenis Persalinan", ["Spontan Bidan", "Spontan Dokter", "Tindakan / Rujukan"])
            jenis_kelamin = st.selectbox("Jenis Kelamin Bayi", ["Laki-laki", "Perempuan"])
        with c3:
            apgar_1 = st.number_input("APGAR Score (1 Menit)", 0, 10, 8)
            apgar_5 = st.number_input("APGAR Score (5 Menit)", 0, 10, 9)

        st.markdown("### C. Manajemen Aktif Kala III & Observasi Kala IV")
        c1, c2, c3 = st.columns(3)
        with c1:
            oksitosin = st.checkbox("Suntik Oksitosin 10 IU (IM dalam 1 mnt)", value=True)
            ptt = st.checkbox("Peregangan Tali Pusat Terkendali (PTT)", value=True)
            masase = st.checkbox("Masase Fundus Uteri", value=True)
        with c2:
            plasenta_lahir = st.text_input("Jam Plasenta Lahir", value="08:42 WIB")
            kelengkapan_plasenta = st.selectbox("Kelengkapan Plasenta", ["Lengkap", "Tidak Lengkap / Sisa Plasenta"])
        with c3:
            laserasi = st.selectbox("Laserasi Perineum", ["Derajat 1 (Tanpa Hacting)", "Derajat 2 (Hacting Perineum)", "Derajat 3/4 (Rujuk)"])
            perdarahan_kala4 = st.number_input("Estimasi Perdarahan Kala IV (ml)", value=150)

        catatan_persalinan = st.text_area("Catatan Tambahan Bidan / SOAP Persalinan")

        btn_persalinan = st.form_submit_button("💾 Simpan Pendokumentasian Persalinan")

        if btn_persalinan:
            record = {
                "no_rm": no_rm,
                "nama_ibu": nama_ibu,
                "umur": umur_ibu,
                "GPA": f"G{gravida}P{partus}A{abortus}",
                "hpht": str(hpht),
                "tp": str(tp),
                "tgl_lahir": str(tgl_lahir),
                "jam_lahir": str(jam_lahir),
                "jenis_persalinan": jenis_persalinan,
                "apgar": f"{apgar_1}/{apgar_5}",
                "laserasi": laserasi,
                "perdarahan": perdarahan_kala4,
                "catatan": catatan_persalinan
            }
            db["persalinan"].append(record)
            save_data(db)
            st.success(f"Data persalinan untuk {nama_ibu} (No. RM: {no_rm}) berhasil disimpan!")

# ==========================================
# 3. PEMANTAUAN PARTOGRAF
# ==========================================
elif menu == "📈 Pemantauan Partograf":
    st.markdown("<div class='main-header'>📈 Lembar Pemantauan Partograf (Kala I Fase Aktif)</div>", unsafe_allow_html=True)
    st.caption("Pemantauan Pembukaan Serviks, Penurunan Kepala, Kontraksi, dan DJJ sesuai Standar APN/WHO")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("#### Input Hasil Observasi Berkala")
        jam_obs = st.time_input("Waktu Pemeriksaan", value=datetime.time(8, 0))
        djj = st.number_input("Denyut Jantung Janin (DJJ - x/menit)", 80, 200, 140)
        pembukaan = st.slider("Pembukaan Serviks (cm)", 0, 10, 4)
        penurunan = st.slider("Penurunan Kepala (x/5)", 0, 5, 4)
        ketuban = st.selectbox("Air Ketuban", ["U (Utuh)", "J (Jernih)", "M (Mekanium)", "D (Darah)", "K (Kering)"])
        kontraksi_freq = st.slider("Frekuensi Kontraksi / 10 menit", 1, 5, 3)
        kontraksi_dur = st.slider("Durasi Kontraksi (detik)", 10, 60, 35)
        td_sistolik = st.number_input("TD Sistolik (mmHg)", 80, 200, 120)
        td_diastolik = st.number_input("TD Diastolik (mmHg)", 50, 130, 80)
        nadi = st.number_input("Nadi Ibu (x/menit)", 50, 150, 82)

    with col2:
        st.markdown("#### Visualisasi Grafik Partograf (Pembukaan & Penurunan)")
        
        # Contoh Data Grafik
        jam_list = ["04:00", "08:00", "12:00", "14:00"]
        pembukaan_list = [4, 6, 8, pembukaan]
        penurunan_list = [4, 3, 2, penurunan]

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(jam_list, pembukaan_list, marker='o', color='red', linewidth=2, label='Pembukaan Serviks (cm)')
        ax.plot(jam_list, penurunan_list, marker='x', color='blue', linestyle='--', linewidth=2, label='Penurunan Kepala (x/5)')
        
        # Garis Waspada dan Garis Bertindak
        ax.plot(["04:00", "10:00"], [4, 10], color='orange', linestyle=':', label='Garis Waspada')
        ax.plot(["08:00", "14:00"], [4, 10], color='crimson', linestyle=':', label='Garis Bertindak')

        ax.set_ylim(0, 10)
        ax.set_ylabel("Cm / Penurunan")
        ax.set_xlabel("Jam Observasi")
        ax.set_title("Partograf - Kemajuan Persalinan")
        ax.legend(loc='upper left', fontsize=8)
        ax.grid(True, linestyle='--', alpha=0.5)

        st.pyplot(fig)

        if pembukaan >= 10:
            st.success("🎉 Pembukaan Lengkap (10 cm)! Siapkan Pertolongan Persalinan Kala II.")
        elif pembukaan_list[-1] <= pembukaan_list[-2] and len(pembukaan_list) >= 3:
            st.warning("⚠️ Waspada: Kemajuan persalinan lambat / melewati Garis Waspada. Siapkan evaluasi atau rujukan.")

# ==========================================
# 4. ASUHAN NIFAS (KF)
# ==========================================
elif menu == "🤱 Asuhan Nifas (KF)":
    st.markdown("<div class='main-header'>🤱 Asuhan Nifas / Kunjungan Nifas (KF 1 - 4)</div>", unsafe_allow_html=True)
    st.caption("Pemeriksaan Ibu Nifas Berdasarkan Permenkes No. 21 Tahun 2021")

    with st.form("form_nifas"):
        c1, c2, c3 = st.columns(3)
        with c1:
            no_rm = st.text_input("No. Rekam Medis Ibu", "RM-2026-001")
            nama_ibu = st.text_input("Nama Ibu Nifas", "Ny. Anisa")
            kunjungan_ke = st.selectbox("Jenis Kunjungan Nifas", [
                "KF 1 (6 Jam - 3 Hari Pasca Persalinan)",
                "KF 2 (Hari Ke-4 - Hari Ke-28)",
                "KF 3 (Hari Ke-29 - Hari Ke-42)",
                "KF 4 (> 42 Hari / Pasca Nifas)"
            ])
        with c2:
            tgl_kunjungan = st.date_input("Tanggal Kunjungan", datetime.date.today())
            td = st.text_input("Tekanan Darah (mmHg)", "120/80")
            suhu = st.number_input("Suhu Tubuh (°C)", value=36.6)
            nadi = st.number_input("Nadi (x/mnt)", value=80)
        with c3:
            tfu = st.text_input("Tinggi Fundus Uteri (TFU)", "2 Jari Bawah Pusat")
            kontraksi = st.selectbox("Kontraksi Uterus", ["Keras / Baik", "Lembek / Atonia Uteri"])
            lokhia = st.selectbox("Jenis Lokhia", ["Rubra", "Sanguinolenta", "Serosa", "Alba", "Purulenta (Abnormal)"])

        st.markdown("### Evaluasi Klinis & Tindakan Nifas")
        c1, c2, c3 = st.columns(3)
        with c1:
            luka_perineum = st.selectbox("Kondisi Luka Perineum", ["Bersih & Menyatu", "Bengkak/Kemerahan", "Terinfeksi / Pus", "Tanpa Luka"])
            asi_eksklusif = st.selectbox("Konseling & Praktik ASI", ["ASI Eksklusif Lancar", "ASI Sedikit / Kendala", "Tidak Memberi ASI"])
        with c2:
            vit_a = st.checkbox("Pemberian Vitamin A (2 Kapsul 200.000 IU)", value=True)
            fe_tablet = st.checkbox("Pemberian Tablet Tambah Darah (TTD)", value=True)
        with c3:
            kb_pasca = st.selectbox("Konseling KB Pascapersalinan", ["Setuju (MOW/IUD/Implan/Suntik)", "Belum Memutuskan", "Menolak"])

        catatan_nifas = st.text_area("Catatan SOAP / Keluhan Ibu Nifas")
        btn_nifas = st.form_submit_button("💾 Simpan Data Kunjungan Nifas")

        if btn_nifas:
            record = {
                "no_rm": no_rm,
                "nama_ibu": nama_ibu,
                "kunjungan": kunjungan_ke,
                "tgl_kunjungan": str(tgl_kunjungan),
                "td": td,
                "tfu": tfu,
                "kontraksi": kontraksi,
                "lokhia": lokhia,
                "vit_a": vit_a,
                "asi": asi_eksklusif,
                "kb_pasca": kb_pasca,
                "catatan": catatan_nifas
            }
            db["nifas"].append(record)
            save_data(db)
            st.success(f"Pencatatan {kunjungan_ke} untuk {nama_ibu} berhasil disimpan!")

# ==========================================
# 5. PELAYANAN NEONATUS (KN)
# ==========================================
elif menu == "👶 Pelayanan Neonatus (KN)":
    st.markdown("<div class='main-header'>👶 Pelayanan Bayi Baru Lahir & Neonatus (KN 1 - 3)</div>", unsafe_allow_html=True)
    st.caption("Pemeriksaan Kunjungan Neonatus Esensial & Skrining Hipotiroid Kongenital (SHK)")

    with st.form("form_neonatus"):
        c1, c2, c3 = st.columns(3)
        with c1:
            no_rm_bayi = st.text_input("No. RM Bayi / Ibu", "RM-2026-001-B")
            nama_bayi = st.text_input("Nama Bayi", "By. Ny. Anisa")
            kn_type = st.selectbox("Kategori Kunjungan Neonatus", [
                "KN 1 (6 Jam - 48 Jam)",
                "KN 2 (Hari Ke-3 - Hari Ke-7)",
                "KN 3 (Hari Ke-8 - Hari Ke-28)"
            ])
        with c2:
            tgl_pemeriksaan = st.date_input("Tanggal Pemeriksaan", datetime.date.today())
            bb = st.number_input("Berat Badan (gram)", value=3100)
            pb = st.number_input("Panjang Badan (cm)", value=49)
            lk = st.number_input("Lingkar Kepala (cm)", value=34)
        with c3:
            suhu = st.number_input("Suhu Tubuh (°C)", value=36.8)
            frek_napas = st.number_input("Frekuensi Napas (x/mnt)", value=44)
            djj_bayi = st.number_input("Frekuensi Jantung (x/mnt)", value=136)

        st.markdown("### Checklist Pelayanan Kesehatan Neonatus Esensial")
        c1, c2, c3 = st.columns(3)
        with c1:
            salep_mata = st.checkbox("Salep Mata Antibiotik Profilaksis", value=True)
            vit_k1 = st.checkbox("Injeksi Vitamin K1 (1 mg IM)", value=True)
            hb0 = st.checkbox("Imunisasi Hepatitis B0 (<24 Jam)", value=True)
        with c2:
            perawatan_tali_pusat = st.selectbox("Perawatan Tali Pusat", ["Kering & Bersih", "Basah / Bau (Inveksi)", "Tali Pusat Lepas"])
            shk = st.selectbox("Skrining Hipotiroid Kongenital (SHK)", ["Sudah Diambil Sampel (Usia 48-72 jam)", "Belum Diambil", "Ditolak Orang Tua"])
        with c3:
            tanda_bahaya = st.multiselect("Tanda Bahaya Neonatus (JIKA ADA)", [
                "Tidak Mau Menyusu", "Kejang", "Lemah / Letargis", "Napas Cepat (>60x)", "Kuning (Ikterus)", "Demam / Hipotermi"
            ])

        catatan_bayi = st.text_area("Catatan Perkembangan Bayi / SOAP")
        btn_neonatus = st.form_submit_button("💾 Simpan Data Pelayanan Neonatus")

        if btn_neonatus:
            record = {
                "no_rm": no_rm_bayi,
                "nama_bayi": nama_bayi,
                "kunjungan": kn_type,
                "tgl_pemeriksaan": str(tgl_pemeriksaan),
                "bb": bb,
                "pb": pb,
                "shk": shk,
                "vit_k1": vit_k1,
                "hb0": hb0,
                "tanda_bahaya": ", ".join(tanda_bahaya) if tanda_bahaya else "Tidak Ada",
                "catatan": catatan_bayi
            }
            db["neonatus"].append(record)
            save_data(db)
            st.success(f"Pencatatan {kn_type} untuk {nama_bayi} berhasil disimpan!")

# ==========================================
# 6. KUNJUNGAN RUMAH (HOME CARE)
# ==========================================
elif menu == "🏡 Kunjungan Rumah (Home Care)":
    st.markdown("<div class='main-header'>🏡 Form Kunjungan Rumah (Home Care) TPMB</div>", unsafe_allow_html=True)
    st.caption("Pendokumentasian Pemantauan Kesehatan Ibu & Bayi di Lingkungan Rumah")

    with st.form("form_homecare"):
        c1, c2 = st.columns(2)
        with c1:
            tgl_homecare = st.date_input("Tanggal Kunjungan Rumah", datetime.date.today())
            nama_klien = st.text_input("Nama Ibu / Bayi", "Ny. Anisa & Bayi")
            alamat_klien = st.text_area("Alamat Rumah", "Jl. Mawar No. 5, RT 02/03")
        with c2:
            alasan_kunjungan = st.selectbox("Alasan Home Care", [
                "Pemantauan Pasca Persalinan / Nifas di Rumah",
                "Pemantauan Bayi Baru Lahir / BBLR",
                "Drop Out Kunjungan / Lupa Jadwal",
                "Pendampingan Tanda Bahaya & Edukasi Keluarga"
            ])
            petugas_bidan = st.text_input("Nama Bidan Pelaksana", "Bidan Rahma, S.Tr.Keb")

        st.markdown("### Temuan Lapangan & Kondisi Rumah")
        c1, c2 = st.columns(2)
        with c1:
            kondisi_ibu_bayi = st.text_area("Kondisi Fisik Ibu & Bayi saat Dikunjungi", "Ibu tampak sehat, ASI lancar, TFU sesuai. Bayi aktif, tidak ikterus.")
            sanitasi_rumah = st.selectbox("Sanitasi & Lingkungan Rumah", ["Bersih & Ventilasi Baik", "Cukup", "Kurang Bersih / Lembab"])
        with c2:
            edukasi_diberikan = st.text_area("Edukasi & Konseling yang Diberikan", "Edukasi tanda bahaya nifas, perawatan tali pusat steril, konseling ASI eksklusif.")
            rtl = st.text_input("Rencana Tindak Lanjut (RTL)", "Kunjungan ulang ke TPMB tanggal 15 Oktober 2026")

        btn_homecare = st.form_submit_button("💾 Simpan Laporan Kunjungan Rumah")

        if btn_homecare:
            record = {
                "tgl": str(tgl_homecare),
                "klien": nama_klien,
                "alamat": alamat_klien,
                "alasan": alasan_kunjungan,
                "bidan": petugas_bidan,
                "kondisi": kondisi_ibu_bayi,
                "rtl": rtl
            }
            db["homecare"].append(record)
            save_data(db)
            st.success(f"Laporan Home Care untuk {nama_klien} berhasil disimpan!")

# ==========================================
# 7. RUJUKAN MATERNAL & NEONATAL
# ==========================================
elif menu == "🚑 Rujukan Maternal & Neonatal":
    st.markdown("<div class='main-header'>🚑 Sistem Rujukan Maternal & Neonatal (BAKSOKU & SBAR)</div>", unsafe_allow_html=True)
    st.caption("Standardisasi Penanganan Komplikasi & Pembuatan Resume Rujukan Tepat Sasar")

    with st.form("form_rujukan"):
        st.markdown("### A. Identitas & Kasus Rujukan")
        c1, c2, c3 = st.columns(3)
        with c1:
            no_rm = st.text_input("No. RM Pasien", "RM-2026-005")
            nama_pasien = st.text_input("Nama Pasien / Ibu", "Ny. Fitri")
            umur_pasien = st.number_input("Umur (Tahun)", value=31)
        with c2:
            kategori_rujukan = st.selectbox("Kategori Rujukan", ["Maternal (Ibu Hamil/Bersalin/Nifas)", "Neonatal (Bayi Baru Lahir)"])
            diagnosis_pra = st.text_input("Diagnosis Pra-Rujukan", "G2P1A0 39 Mgg Inpartu Kala I Fase Aktif + PEB")
        with c3:
            faskes_tujuan = st.text_input("Faskes Tujuan Rujukan", "RSUD DR. Soetomo")
            transportasi = st.selectbox("Transportasi Rujukan", ["Ambulans TPMB", "Ambulans Desa/Puskesmas", "Kendaraan Pribadi Siaga"])

        st.markdown("### B. Checklist Keselamatan Rujukan Prinsip 'BAKSOKU'")
        c1, c2 = st.columns(2)
        with c1:
            b_bidan = st.checkbox("B - Bidan (Pendampingan Bidan Kompeten)", value=True)
            a_alat = st.checkbox("A - Alat (Resusitator, Set Partus, Oksigen Siaga)", value=True)
            k_keluarga = st.checkbox("K - Keluarga (Informed Consent & Pendamping Keluarga)", value=True)
            s_surat = st.checkbox("S - Surat (Surat Rujukan & Resume Medis SBAR)", value=True)
        with c2:
            o_obat = st.checkbox("O - Obat (Oksitosin / MgSO4 / Cairan IV Diberikan)", value=True)
            k_kendaraan = st.checkbox("K - Kendaraan (Ambulans Layak & Pengemudi Siaga)", value=True)
            u_uang = st.checkbox("U - Uang (Penjamin BPJS / Jamkesda / Dana Siaga)", value=True)

        st.markdown("### C. Resume Medis Komunikasi SBAR (Situation, Background, Assessment, Recommendation)")
        c1, c2 = st.columns(2)
        with c1:
            sbar_s = st.text_area("S (Situation)", "Ny. Fitri 31th G2P1A0 rujukan dari TPMB dengan TD 160/110 mmHg, pusing, proteinuria +2.")
            sbar_b = st.text_area("B (Background)", "Usia kehamilan 39 minggu, mules sejak 6 jam lalu, belum keluar air-air.")
        with c2:
            sbar_a = st.text_area("A (Assessment)", "Inpartu Kala I Fase Aktif dengan Preeklampsia Berat (PEB). Pembukaan 5 cm.")
            sbar_r = st.text_area("R (Recommendation)", "Mohon penanganan komplikasi PEB, penatalaksanaan MgSO4 lanjutan, dan persiapan persalinan di RS.")

        btn_rujukan = st.form_submit_button("💾 Simpan & Cetak Lembar Rujukan SBAR")

        if btn_rujukan:
            record = {
                "no_rm": no_rm,
                "nama": nama_pasien,
                "kategori": kategori_rujukan,
                "diagnosis": diagnosis_pra,
                "faskes": faskes_tujuan,
                "baksoku_lengkap": all([b_bidan, a_alat, k_keluarga, s_surat, o_obat, k_kendaraan, u_uang]),
                "sbar_s": sbar_s,
                "sbar_a": sbar_a,
                "sbar_r": sbar_r
            }
            db["rujukan"].append(record)
            save_data(db)
            st.success(f"Dokumen Rujukan SBAR untuk {nama_pasien} ke {faskes_tujuan} berhasil dibuat dan disimpan!")

