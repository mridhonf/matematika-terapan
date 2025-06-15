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
st.title("Optimasi Produksi Motor")
    st.write("Model Linear Programming untuk memaksimalkan keuntungan produksi dua jenis motor: Sport dan Bebek.")

    # -----------------------------
    # Input dari pengguna
    # -----------------------------
    # Input keuntungan per unit untuk masing-masing motor
    profit_sport = st.number_input("Keuntungan per unit Motor Sport (juta)", value=5.0)
    profit_bebek = st.number_input("Keuntungan per unit Motor Bebek (juta)", value=3.0)

    # Waktu produksi (konstanta) untuk masing-masing jenis motor
    waktu_perakitan = [3, 2]  # 3 jam untuk Sport, 2 jam untuk Bebek
    waktu_mesin = [2, 1]      # 2 jam untuk Sport, 1 jam untuk Bebek

    # Input batas waktu total yang tersedia
    total_perakitan = st.slider("Total waktu perakitan tersedia per minggu (jam)", 0, 500, 240)
    total_mesin = st.slider("Total waktu mesin tersedia per minggu (jam)", 0, 300, 180)

    # -----------------------------
    # Menyusun model matematis LP
    # -----------------------------
    c = [-profit_sport, -profit_bebek]  # Fungsi tujuan (dikalikan -1 karena linprog meminimalkan)
    A = [waktu_perakitan, waktu_mesin]  # Matriks kendala (koefisien)
    b = [total_perakitan, total_mesin]  # Batasan kendala
    x_bounds = (0, None)                # x ≥ 0

    # -----------------------------
    # Menyelesaikan model LP
    # -----------------------------
    res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, x_bounds])

    # -----------------------------
    # Menampilkan hasil
    # -----------------------------
    if res.success:
        x1, x2 = res.x  # x1 = jumlah Motor Sport, x2 = jumlah Motor Bebek
        st.success(f"Produksi optimal: {x1:.2f} unit Sport dan {x2:.2f} unit Bebek")
        st.write(f"Total keuntungan maksimum: Rp {(res.fun * -1):,.2f} juta")

        # -----------------------------
        # Visualisasi grafik kendala dan solusi
        # -----------------------------
        fig, ax = plt.subplots()

        x = np.linspace(0, 100, 100)  # Range nilai Motor Sport
        # Menggambar garis kendala perakitan dan mesin
        y1 = (total_perakitan - waktu_perakitan[0] * x) / waktu_perakitan[1]
        y2 = (total_mesin - waktu_mesin[0] * x) / waktu_mesin[1]

        # Plot garis kendala
        ax.plot(x, y1, label='Kendala Perakitan')
        ax.plot(x, y2, label='Kendala Mesin')

        # Plot titik solusi optimal
        ax.scatter(x1, x2, color='red', label='Solusi Optimal')

        # Atur batas tampilan grafik agar muat
        ax.set_xlim(0, max(x1, x2) * 1.5)
        ax.set_ylim(0, max(x1, x2) * 1.5)

        # Label sumbu dan legenda
        ax.set_xlabel("Motor Sport")
        ax.set_ylabel("Motor Bebek")
        ax.legend()

        # Tampilkan grafik di Streamlit
        st.pyplot(fig)

    else:
        # Jika tidak ditemukan solusi yang feasible
        st.error("Tidak ditemukan solusi optimal. Periksa kembali input kendala.")

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
elif menu == "Model Matematika Lainnya":
    # Menampilkan judul halaman menu
    st.title("Model Proyeksi Permintaan Motor")

    # Deskripsi singkat model
    st.write("Memprediksi permintaan motor di masa depan menggunakan regresi linear sederhana.")

    # Formulir input data historis penjualan
    st.markdown("Masukkan data historis penjualan:")

    # Input tahun-tahun historis, dipisahkan koma
    years = st.text_input("Tahun-tahun (pisahkan dengan koma)", "2019,2020,2021,2022,2023")

    # Input data penjualan per tahun yang sesuai
    sales = st.text_input("Jumlah terjual per tahun (unit)", "2000,2200,2500,2700,3000")

    try:
        # Mengubah string input tahun menjadi array integer
        X = np.array([int(x) for x in years.split(",")])

        # Mengubah string input penjualan menjadi array integer
        Y = np.array([int(y) for y in sales.split(",")])

        # Mengecek apakah panjang data tahun dan penjualan cocok
        if len(X) != len(Y):
            st.error("Jumlah tahun dan data penjualan harus sama.")
        else:
            # ==========================
            # Proses Regresi Linear
            # ==========================

            # Menggunakan numpy.polyfit untuk mencari garis regresi linear: y = b*x + a
            coef = np.polyfit(X, Y, 1)  # coef[0] = b (slope), coef[1] = a (intercept)
            a, b = coef[1], coef[0]     # assign agar lebih mudah dibaca

            # Input tahun yang ingin diprediksi
            tahun_pred = st.number_input("Prediksi permintaan untuk tahun:", value=2025)

            # Menghitung hasil prediksi menggunakan rumus regresi: y = a + b*x
            prediksi = a + b * tahun_pred

            # Menampilkan hasil prediksi ke user
            st.success(f"Prediksi permintaan untuk tahun {tahun_pred}: {prediksi:.0f} unit")

            # ==========================
            # Visualisasi Garis Regresi
            # ==========================

            # Membuat array tahun untuk digambar di grafik (lebih rapat agar garis halus)
            x_plot = np.linspace(min(X)-1, max(X)+2, 100)

            # Menghitung nilai y (penjualan) berdasarkan garis regresi
            y_plot = a + b * x_plot

            # Membuat grafik
            fig, ax = plt.subplots()

            # Menampilkan titik data aktual (tahun vs penjualan)
            ax.plot(X, Y, 'o-', label='Data Aktual')

            # Menampilkan garis regresi (garis prediksi)
            ax.plot(x_plot, y_plot, 'r--', label='Regresi Linear')

            # Menandai tahun prediksi dengan garis vertikal
            ax.axvline(tahun_pred, color='gray', linestyle='--', label='Tahun Prediksi')

            # Menandai hasil prediksi dengan garis horizontal
            ax.axhline(prediksi, color='green', linestyle=':', label='Prediksi')

            # Memberi label sumbu dan legend
            ax.set_xlabel("Tahun")
            ax.set_ylabel("Jumlah Terjual (unit)")
            ax.legend()

            # Menampilkan grafik di Streamlit
            st.pyplot(fig)

    except:
        # Menangani kesalahan input jika user salah format angka/koma
        st.error("Pastikan input berupa angka dan dipisahkan dengan koma.")
