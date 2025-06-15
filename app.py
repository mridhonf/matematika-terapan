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
import streamlit as st
from scipy.optimize import linprog

st.title("Optimasi Produksi Motor (Linear Programming)")

st.markdown("## Soal:")
st.write("""
Perusahaan memproduksi Motor Sport dan Motor Bebek.
- Keuntungan: Sport = Rp 5 juta, Bebek = Rp 3 juta
- Batasan: 180 jam perakitan, 300 unit bahan baku per minggu
- Sport butuh: 3 jam & 5 bahan per unit
- Bebek butuh: 2 jam & 4 bahan per unit
""")

# Koefisien fungsi objektif (dikali -1 karena linprog meminimalkan)
c = [-5, -3]  # Z = 5x + 3y → minimisasi -Z

# Koefisien dan batasan dari constraint
A = [
    [3, 2],  # waktu perakitan: 3x + 2y ≤ 180
    [5, 4]   # bahan baku:      5x + 4y ≤ 300
]
b = [180, 300]

# Batas bawah x dan y adalah 0 (tidak negatif)
x_bounds = (0, None)
y_bounds = (0, None)

# Solusi
res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

if res.success:
    st.success("Solusi optimal ditemukan!")
    x_opt, y_opt = res.x
    st.write(f"Produksi Motor Sport: {x_opt:.0f} unit")
    st.write(f"Produksi Motor Bebek: {y_opt:.0f} unit")
    st.write(f"Keuntungan maksimum: Rp {(-res.fun):.2f} juta")
else:
    st.error("Tidak ditemukan solusi optimal.")

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
