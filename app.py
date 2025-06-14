import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog
from pulp import LpMaximize, LpProblem, LpVariable

st.set_page_config(page_title="Aplikasi Model Industri Motor", layout="wide")

# Sidebar - Menu
menu = st.sidebar.selectbox(
    "Pilih Model:",
    ["Optimasi Produksi (Linear Programming)", "Model Persediaan (EOQ)", "Model Antrian (M/M/1)", "Model Matematika Lainnya"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Petunjuk Umum:**")
st.sidebar.markdown(
    """
    Aplikasi ini dirancang untuk membantu analisis model matematika pada perusahaan produksi motor:
    - Optimasi jumlah produksi
    - Efisiensi persediaan
    - Estimasi waktu dan panjang antrian
    - Model matematika lainnya seperti break-even
    """
)

# ========== MENU 1: LINEAR PROGRAMMING ==========
# Dokumentasi / instruksi di sidebar
if menu == "Optimasi Produksi (Linear Programming)":
    st.sidebar.subheader("📌 Petunjuk Penggunaan")
    st.sidebar.markdown(
        "- Masukkan keuntungan per unit motor\n"
        "- Masukkan total jam kerja dan jam mesin\n"
        "- Sistem akan menghitung jumlah produksi optimal"
    )

# Input user
    profit_sport = st.number_input("💰 Keuntungan per Unit Motor Sport (Rp)", value=3000000)
    profit_bebek = st.number_input("💰 Keuntungan per Unit Motor Bebek (Rp)", value=2000000)
    waktu_kerja = st.number_input("⏱️ Total Waktu Kerja (jam)", value=120)
    waktu_mesin = st.number_input("⚙️ Total Waktu Mesin (jam)", value=100)

# ------------------------
# Pemodelan Linear Programming
# ------------------------

# 1. Membuat model optimasi dengan tujuan maksimisasi keuntungan
    model = LpProblem("Optimasi_Produksi_Motor", LpMaximize)

# 2. Mendefinisikan variabel keputusan: jumlah motor sport (X) dan motor bebek (Y)
    X = LpVariable("Motor_Sport", lowBound=0, cat="Continuous")
    Y = LpVariable("Motor_Bebek", lowBound=0, cat="Continuous")

# 3. Menentukan fungsi objektif (maximize profit)
    model += profit_sport * X + profit_bebek * Y

# 4. Menambahkan kendala waktu kerja: 3X + 2Y ≤ waktu kerja tersedia
    model += 3 * X + 2 * Y <= waktu_kerja

# 5. Menambahkan kendala waktu mesin: 2X + 1Y ≤ waktu mesin tersedia
    model += 2 * X + 1 * Y <= waktu_mesin

# 6. Menyelesaikan model
    model.solve()

# 7. Mengambil hasil solusi
    x_val = X.varValue  # jumlah motor sport
    y_val = Y.varValue  # jumlah motor bebek
    total_profit = model.objective.value()

# ------------------------
# Output hasil
# ------------------------
    st.subheader("📈 Hasil Optimasi Produksi")
    st.write(f"✅ Produksi Motor Sport: **{x_val:.2f} unit**")
    st.write(f"✅ Produksi Motor Bebek: **{y_val:.2f} unit**")
    st.success(f"💵 Total Keuntungan Maksimum: **Rp {int(total_profit):,}**")

# ------------------------
# Visualisasi Wilayah Solusi
# ------------------------

# Membuat titik X untuk menggambar kendala
    x_vals = np.linspace(0, waktu_kerja, 200)

# Menghitung batas Y dari masing-masing kendala
    y_kerja = (waktu_kerja - 3 * x_vals) / 2
    y_mesin = (waktu_mesin - 2 * x_vals) / 1

# Plot wilayah solusi
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_kerja, label="Kendala Waktu Kerja", color='blue')
    ax.plot(x_vals, y_mesin, label="Kendala Waktu Mesin", color='green')

# Arsiran solusi
    ax.fill_between(x_vals, np.minimum(y_kerja, y_mesin), 0, where=(np.minimum(y_kerja, y_mesin) > 0), alpha=0.2)

# Titik solusi optimal
    ax.plot(x_val, y_val, 'ro', label="Solusi Optimal")

# Label grafik
    ax.set_xlabel("Motor Sport (unit)")
    ax.set_ylabel("Motor Bebek (unit)")
    ax.set_title("Wilayah Solusi dan Titik Optimal")
    ax.legend()
    st.pyplot(fig)
# ========== MENU 2: EOQ ==========
elif menu == "Model Persediaan (EOQ)":
    st.title("Model Persediaan (EOQ)")

    st.sidebar.subheader("📌 Petunjuk")
    st.sidebar.markdown(
        "- Masukkan data permintaan tahunan (D)\n"
        "- Biaya pesan tiap kali order (S)\n"
        "- Biaya simpan per unit per tahun (H)"
    )

    # Input dari user
    D = st.number_input("Permintaan Tahunan (unit)", value=1000)
    S = st.number_input("Biaya Pemesanan per Order (Rp)", value=50000)
    H = st.number_input("Biaya Penyimpanan per Unit per Tahun (Rp)", value=2000)

    if D > 0 and S > 0 and H > 0:
        # Hitung EOQ menggunakan rumus klasik
        EOQ = (2 * D * S / H) ** 0.5

        # Tampilkan hasil EOQ
        st.subheader("📦 Hasil Perhitungan EOQ")
        st.write(f"Jumlah Pembelian Optimal (EOQ): **{EOQ:.2f} unit**")

        # Visualisasi: grafik total biaya terhadap jumlah pesanan
        import numpy as np
        import matplotlib.pyplot as plt

        Q = np.arange(1, int(2 * EOQ))  # rentang jumlah pemesanan
        total_biaya = (D / Q) * S + (Q / 2) * H  # total biaya tahunan

        fig, ax = plt.subplots()
        ax.plot(Q, total_biaya, label='Total Biaya', color='blue')
        ax.axvline(EOQ, color='red', linestyle='--', label='EOQ Optimal')
        ax.set_xlabel("Jumlah Pesan per Order (Q)")
        ax.set_ylabel("Total Biaya Tahunan (Rp)")
        ax.set_title("Grafik EOQ - Total Biaya vs Jumlah Order")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("Isi semua input dengan benar.")
# ========== MENU 3: ANTRIAN M/M/1 ==========
elif menu == "Model Antrian (M/M/1)":
    st.title("Model Antrian (M/M/1) - Produksi Motor")

    st.sidebar.subheader("📌 Petunjuk")
    st.sidebar.markdown(
        "- Masukkan laju kedatangan pelanggan (λ)\n"
        "- Masukkan laju pelayanan per pelanggan (μ)\n"
        "- Sistem akan menghitung kinerja antrian M/M/1"
        "- RPS = Rata Rata Jumlah Pelanggan Dalam Sistem"
        "- RPA = Rata Rata Jumlah Pelanggan Dalam Antrean"
        "- WRS = Waktu Rata Rata dalam Sistem"
        "- WPA = Waktu Rata Rata dalam Antrean"
    )

    # Input dari pengguna
    lambd = st.number_input("Berapa banyak motor pelanggan yang datang per jam nya (λ)", value=5.0)
    mu = st.number_input("Laju Pelayanan pelanggan per jam nya (μ)", value=8.0)

    if lambd > 0 and mu > 0 and lambd < mu:
        # Rumus dasar model antrian M/M/1
        rho = lambd / mu                  # Tingkat utilisasi server
        RPS = rho / (1 - rho)               # Rata-rata jumlah pelanggan dalam sistem
        RPA = rho**2 / (1 - rho)           # Rata-rata jumlah pelanggan dalam antrean
        WRS = 1 / (mu - lambd)              # Waktu rata-rata dalam sistem
        WRA = lambd / (mu * (mu - lambd))  # Waktu rata-rata dalam antrean

        # Output hasil perhitungan
        st.subheader("📊 Hasil Analisis Antrian M/M/1")
        st.write(f"Tingkat Utilisasi Server (ρ): **{rho:.2f}**")
        st.write(f"Rata-rata Pelanggan dalam Sistem (RPS): **{RPS:.2f}**")
        st.write(f"Rata-rata Pelanggan dalam Antrian (RPA): **{RPA:.2f}**")
        st.write(f"Waktu Rata-rata dalam Sistem (WRS): **{WRS:.2f} jam**")
        st.write(f"Waktu Rata-rata dalam Antrian (WRA): **{WRA:.2f} jam**")

        # Visualisasi batang
        st.subheader("📉 Visualisasi Antrian")
        labels = ["RPS", "RPA", "WRS", "Wq"]
        values = [RPS, RPA, WRS, WRA]

        fig, ax = plt.subplots()
        ax.bar(labels, values, color=["blue", "orange", "green", "red"])
        ax.set_ylabel("Nilai")
        ax.set_title("Grafik Parameter Antrian")
        st.pyplot(fig)

    elif lambd >= mu:
        st.error("⛔ Laju kedatangan harus lebih kecil dari laju pelayanan (λ < μ) agar sistem stabil.")
    else:
        st.info("Masukkan nilai λ dan μ yang valid untuk memulai perhitungan.")

# ========== MENU 4: MODEL LAINNYA ==========
elif menu == "Model Planning Permintaan Motor":
    st.title("Model Proyeksi Permintaan Motor")
    st.write("Memprediksi permintaan motor di masa depan menggunakan regresi linear sederhana.")

    st.markdown("Masukkan data historis penjualan:")
    years = st.text_input("Tahun-tahun (pisahkan dengan koma)", "2019,2020,2021,2022,2023")
    sales = st.text_input("Jumlah terjual per tahun (unit)", "2000,2200,2500,2700,3000")

    try:
        X = np.array([int(x) for x in years.split(",")])
        Y = np.array([int(y) for y in sales.split(",")])

        if len(X) != len(Y):
            st.error("Jumlah tahun dan data penjualan harus sama.")
        else:
            # Regresi Linear Sederhana
            coef = np.polyfit(X, Y, 1)  # slope, intercept
            a, b = coef[1], coef[0]
            #fungsi
            tahun_pred = st.number_input("Prediksi permintaan untuk tahun:", value=0)
            prediksi = a + b * tahun_pred
            #output dari perhitungan
            st.success(f"Prediksi permintaan untuk tahun {tahun_pred}: {prediksi:.0f} unit")

            # Visualisasi
            x_plot = np.linspace(min(X)-1, max(X)+2, 100)
            y_plot = a + b * x_plot

            fig, ax = plt.subplots()
            ax.plot(X, Y, 'o-', label='Data Aktual')
            ax.plot(x_plot, y_plot, 'r--', label='Regresi Linear')
            ax.axvline(tahun_pred, color='gray', linestyle='--', label='Tahun Prediksi')
            ax.axhline(prediksi, color='green', linestyle=':', label='Prediksi')
            ax.set_xlabel("Tahun")
            ax.set_ylabel("Jumlah Terjual (unit)")
            ax.legend()
            st.pyplot(fig)
    except:
        st.error("Pastikan input berupa angka dan dipisahkan dengan koma.")

        st.pyplot(fig)
    else:
        st.error("Harga jual harus lebih besar dari biaya modal.")

