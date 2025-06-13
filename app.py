import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

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
if menu == "Optimasi Produksi (Linear Programming)":
    st.title("Optimasi Produksi Motor")
    st.write("Model Linear Programming untuk memaksimalkan keuntungan produksi dua jenis motor: Sport dan Bebek.")

    profit_sport = st.number_input("Keuntungan per unit Motor Sport (juta)", value=5.0)
    profit_bebek = st.number_input("Keuntungan per unit Motor Bebek (juta)", value=3.0)
    waktu_perakitan = [3, 2]  # jam/unit
    waktu_mesin = [2, 1]      # jam/unit
    total_perakitan = st.slider("Total waktu perakitan tersedia (jam)", 0, 500, 240)
    total_mesin = st.slider("Total waktu mesin tersedia (jam)", 0, 300, 180)

    c = [-profit_sport, -profit_bebek]
    A = [waktu_perakitan, waktu_mesin]
    b = [total_perakitan, total_mesin]
    x_bounds = (0, None)
    
    res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, x_bounds])

    if res.success:
        x1, x2 = res.x
        st.success(f"Produksi optimal: {x1:.2f} unit Sport dan {x2:.2f} unit Bebek")
        st.write(f"Total keuntungan maksimum: Rp {(res.fun * -1):,.2f} juta")

        # Visualisasi
        fig, ax = plt.subplots()
        x = np.linspace(0, 100, 100)
        y1 = (total_perakitan - waktu_perakitan[0] * x) / waktu_perakitan[1]
        y2 = (total_mesin - waktu_mesin[0] * x) / waktu_mesin[1]
        ax.plot(x, y1, label='Kendala Perakitan')
        ax.plot(x, y2, label='Kendala Mesin')
        ax.scatter(x1, x2, color='red', label='Solusi Optimal')
        ax.set_xlim(0, max(x1, x2) * 1.5)
        ax.set_ylim(0, max(x1, x2) * 1.5)
        ax.set_xlabel("Motor Sport")
        ax.set_ylabel("Motor Bebek")
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("Tidak ditemukan solusi optimal.")

# ========== MENU 2: EOQ ==========
elif menu == "Model Persediaan (EOQ)":
    st.title("Model Persediaan EOQ")
    st.write("Menghitung Economic Order Quantity untuk komponen motor.")

    D = st.number_input("Permintaan tahunan (unit)", value=1000)
    S = st.number_input("Biaya pemesanan per pesanan (Rp)", value=500000.0)
    H = st.number_input("Biaya penyimpanan per unit per tahun (Rp)", value=10000.0)

    EOQ = np.sqrt((2 * D * S) / H)
    st.success(f"EOQ: {EOQ:.2f} unit per pesanan")

    # Visualisasi
    Q = np.linspace(1, 2 * EOQ, 100)
    TC = (D / Q) * S + (Q / 2) * H

    fig, ax = plt.subplots()
    ax.plot(Q, TC, label='Total Cost')
    ax.axvline(EOQ, color='red', linestyle='--', label='EOQ')
    ax.set_xlabel("Jumlah Pesan (Q)")
    ax.set_ylabel("Total Biaya (Rp)")
    ax.legend()
    st.pyplot(fig)


# ========== MENU 2: EOQ ==========
elif menu == "Model Persediaan (EOQ)":
    st.title("Model Persediaan (EOQ) - Economic Order Quantity")

    st.sidebar.subheader("📦 Petunjuk Penggunaan")
    st.sidebar.markdown(
        "- Masukkan nilai permintaan tahunan (D)\n"
        "- Masukkan biaya pemesanan per pesanan (S)\n"
        "- Masukkan biaya penyimpanan per unit per tahun (H)"
    )

    # Input
    D = st.number_input("Permintaan Tahunan (unit)", value=1000)
    S = st.number_input("Biaya Pemesanan per Pesanan (Rp)", value=50000)
    H = st.number_input("Biaya Penyimpanan per Unit per Tahun (Rp)", value=2000)

    if D > 0 and S > 0 and H > 0:
        # Hitung EOQ
        EOQ = np.sqrt((2 * D * S) / H)
        st.success(f"EOQ Optimal: {EOQ:.2f} unit per pesanan")

        # Visualisasi Total Biaya
        Q = np.arange(1, int(2 * EOQ))
        total_biaya = (D / Q) * S + (Q / 2) * H

        fig, ax = plt.subplots()
        ax.plot(Q, total_biaya, label='Total Biaya', color='blue')
        ax.axvline(EOQ, color='red', linestyle='--', label='EOQ Optimal')
        ax.set_xlabel("Jumlah Pesanan (Q)")
        ax.set_ylabel("Total Biaya (Rp)")
        ax.set_title("Grafik Total Biaya vs Jumlah Pesanan")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("Masukkan semua nilai input dengan benar.")

# ========== MENU 3: ANTRIAN M/M/1 ==========
elif menu == "Model Antrian (M/M/1)":
    st.title("Model Antrian M/M/1")
    st.write("Estimasi performa sistem antrian untuk proses pengecekan kualitas motor.")

    lambd = st.number_input("Laju kedatangan pelanggan (motor/jam)", value=10.0)
    mu = st.number_input("Laju pelayanan (motor/jam)", value=15.0)

    if mu > lambd:
        rho = lambd / mu
        L = rho / (1 - rho)
        Lq = rho**2 / (1 - rho)
        W = 1 / (mu - lambd)
        Wq = rho / (mu - lambd)

        st.success(f"Utilisasi server: {rho:.2f}")
        st.write(f"Rata-rata jumlah motor dalam sistem: {L:.2f}")
        st.write(f"Rata-rata jumlah dalam antrian: {Lq:.2f}")
        st.write(f"Waktu rata-rata dalam sistem: {W:.2f} jam")
        st.write(f"Waktu rata-rata dalam antrian: {Wq:.2f} jam")

        # Visualisasi
        fig, ax = plt.subplots()
        rho_range = np.linspace(0.01, 0.99, 100)
        Lq_range = rho_range**2 / (1 - rho_range)
        ax.plot(rho_range, Lq_range)
        ax.axvline(rho, color='red', linestyle='--', label='Utilisasi Sekarang')
        ax.set_xlabel("Utilisasi (ρ)")
        ax.set_ylabel("Rata-rata Jumlah dalam Antrian (Lq)")
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("Laju pelayanan harus lebih tinggi dari laju kedatangan (μ > λ)")

# ========== MENU 4: MODEL LAINNYA ==========
elif menu == "Model Matematika Lainnya":
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

            tahun_pred = st.number_input("Prediksi permintaan untuk tahun:", value=2025)
            prediksi = a + b * tahun_pred

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

