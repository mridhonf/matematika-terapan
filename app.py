import streamlit as st
import numpy as np
from scipy.optimize import linprog
from scipy.stats import expon
import math

st.set_page_config(page_title="Aplikasi Model Matematika Industri", layout="wide")

# Sidebar instruksi
st.sidebar.title("📌 Petunjuk Penggunaan")
st.sidebar.markdown("""
Pilih salah satu model matematika dari daftar menu di bawah:

1. **Optimasi Produksi**: Menyelesaikan masalah Linear Programming.
2. **Model Persediaan (EOQ)**: Menghitung Economic Order Quantity.
3. **Model Antrian (M/M/1)**: Menghitung performa sistem antrian tunggal.
4. **Model Lainnya**: Simulasi decay/exponential untuk sistem industri.

Masukkan parameter yang diminta, lalu lihat grafik dan hasilnya.
""")

menu = st.sidebar.radio("📂 Pilih Menu", ["Optimasi Produksi", "Model Persediaan (EOQ)", "Model Antrian (M/M/1)", "Model Matematika Lainnya"])

# ========== 1. OPTIMASI PRODUKSI ==========
if menu == "Optimasi Produksi":
    st.title("📈 Optimasi Produksi (Linear Programming)")

    st.markdown("Contoh: Maksimalkan keuntungan dari 2 produk dengan batasan waktu kerja dan bahan baku.")

    c = [-20, -30]  # koefisien fungsi objektif (negatif untuk maksimasi)
    A = [[1, 2], [2, 1]]  # koefisien kendala
    b = [40, 50]  # sisi kanan kendala

    res = linprog(c, A_ub=A, b_ub=b, method='highs')

    if res.success:
        x = np.linspace(0, 50, 100)
        y1 = (40 - x) / 2
        y2 = (50 - 2 * x) / 1

        fig, ax = plt.subplots()
        ax.plot(x, y1, label='x + 2y ≤ 40')
        ax.plot(x, y2, label='2x + y ≤ 50')
        ax.fill_between(x, np.minimum(y1, y2), color='gray', alpha=0.3)
        ax.plot(res.x[0], res.x[1], 'ro', label='Solusi Optimal')
        ax.set_xlim(0, 30)
        ax.set_ylim(0, 30)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        st.success(f"Solusi Optimal: x = {res.x[0]:.2f}, y = {res.x[1]:.2f}")
        st.info(f"Maksimum Profit = {-res.fun:.2f}")
    else:
        st.error("Optimasi gagal ditemukan.")

# ========== 2. EOQ ==========
elif menu == "Model Persediaan (EOQ)":
    st.title("📦 Model Persediaan EOQ")

    D = st.number_input("Permintaan tahunan (D)", min_value=1, value=1000)
    S = st.number_input("Biaya pemesanan per pesanan (S)", min_value=1.0, value=50.0)
    H = st.number_input("Biaya penyimpanan per unit per tahun (H)", min_value=0.1, value=5.0)

    if D and S and H:
        EOQ = math.sqrt((2 * D * S) / H)
        st.success(f"EOQ (Jumlah Pemesanan Ekonomis): {EOQ:.2f} unit")

        Q = np.linspace(1, 2*EOQ, 100)
        TC = (D/Q)*S + (Q/2)*H

        fig, ax = plt.subplots()
        ax.plot(Q, TC, label="Total Biaya")
        ax.axvline(EOQ, color='r', linestyle='--', label='EOQ')
        ax.set_xlabel("Jumlah Pesanan")
        ax.set_ylabel("Total Biaya")
        ax.set_title("Kurva EOQ")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

# ========== 3. MODEL ANTRIAN ==========
elif menu == "Model Antrian (M/M/1)":
    st.title("⏳ Model Antrian (M/M/1)")

    λ = st.number_input("Tingkat kedatangan (λ)", min_value=0.1, value=5.0)
    μ = st.number_input("Tingkat pelayanan (μ)", min_value=0.1, value=8.0)

    if λ < μ:
        ρ = λ / μ
        L = ρ / (1 - ρ)
        Lq = ρ**2 / (1 - ρ)
        W = 1 / (μ - λ)
        Wq = λ / (μ * (μ - λ))

        st.success(f"Utilisasi (ρ): {ρ:.2f}")
        st.info(f"Rata-rata dalam sistem (L): {L:.2f}")
        st.info(f"Rata-rata dalam antrian (Lq): {Lq:.2f}")
        st.info(f"Waktu dalam sistem (W): {W:.2f}")
        st.info(f"Waktu tunggu dalam antrian (Wq): {Wq:.2f}")

        t = np.linspace(0, 5, 100)
        P0 = 1 - ρ
        Pn = [(1 - ρ) * ρ**n for n in range(20)]

        fig, ax = plt.subplots()
        ax.bar(range(20), Pn)
        ax.set_xlabel("Jumlah pelanggan dalam sistem")
        ax.set_ylabel("Probabilitas")
        ax.set_title("Distribusi Pelanggan dalam Sistem (M/M/1)")
        st.pyplot(fig)
    else:
        st.error("λ harus lebih kecil dari μ agar sistem stabil.")

# ========== 4. MODEL LAINNYA ==========
elif menu == "Model Matematika Lainnya":
    st.title("🧮 Model Matematika Industri Lainnya")
    st.markdown("Contoh: Model **Exponential Decay** untuk pengurangan jumlah barang karena rusak/usang.")

    N0 = st.number_input("Jumlah awal (N₀)", value=1000)
    decay_rate = st.number_input("Laju kerusakan (λ)", value=0.1)
    time_end = st.slider("Waktu (tahun)", 1, 20, 10)

    t = np.linspace(0, time_end, 100)
    N = N0 * np.exp(-decay_rate * t)

    fig, ax = plt.subplots()
    ax.plot(t, N, label="Jumlah Barang")
    ax.set_xlabel("Waktu (tahun)")
    ax.set_ylabel("Jumlah Barang")
    ax.set_title("Model Eksponensial Decay")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    st.success(f"Sisa barang setelah {time_end} tahun: {N[-1]:.2f}")
