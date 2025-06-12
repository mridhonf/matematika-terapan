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
    st.title("Break-even Point (BEP) Analisis")
    st.write("Analisis titik impas produksi motor.")

    fixed_cost = st.number_input("Biaya tetap (Rp)", value=100_000_000.0)
    variable_cost = st.number_input("Biaya variabel per unit (Rp)", value=3_000_000.0)
    selling_price = st.number_input("Harga jual per unit (Rp)", value=5_000_000.0)

    if selling_price > variable_cost:
        BEP = fixed_cost / (selling_price - variable_cost)
        st.success(f"Titik impas: {BEP:.2f} unit motor")

        # Visualisasi
        q = np.linspace(0, BEP * 2, 100)
        revenue = selling_price * q
        cost = fixed_cost + variable_cost * q

        fig, ax = plt.subplots()
        ax.plot(q, revenue, label='Pendapatan')
        ax.plot(q, cost, label='Total Biaya')
        ax.axvline(BEP, color='red', linestyle='--', label='Break-even Point')
        ax.set_xlabel("Jumlah Unit")
        ax.set_ylabel("Rp")
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("Harga jual harus lebih besar dari biaya variabel.")

