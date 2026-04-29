import streamlit as st
import numpy as np

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Pile Foundation Design",
                   page_icon="🏗️",
                   layout="centered")

# -------------------------
# CSS
# -------------------------
st.markdown("""
<style>
.stApp {background-color: #f4f7fb;}
h1 {color: #0d47a1;}
.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
}
.result {
    background: #e3f2fd;
    padding: 15px;
    border-radius: 10px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Title
# -------------------------
st.title("🏗️ Pile Foundation (Eccentric Load)")
st.subheader("Load Distribution to Piles")

# -------------------------
# Input
# -------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

P = st.number_input("Axial Load P (kN)", min_value=0.0)
e = st.number_input("Eccentricity e (m)", min_value=0.0)

n = st.selectbox("Number of Piles", [2, 4, 6])

spacing = st.number_input("Pile spacing (m)", min_value=0.1, value=2.0)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Calculate
# -------------------------
if st.button("🚀 Calculate"):

    if P == 0:
        st.warning("⚠️ ใส่ค่า P ก่อน")
    else:

        M = P * e

        # pile positions (1D simplification)
        if n == 2:
            x = np.array([-spacing/2, spacing/2])

        elif n == 4:
            x = np.array([-spacing/2, spacing/2, -spacing/2, spacing/2])

        else:  # 6 piles
            x = np.array([-spacing, 0, spacing, -spacing, 0, spacing])

        sum_x2 = np.sum(x**2)

        Qi = []

        for xi in x:
            Qi.append((P / n) + (M * xi / sum_x2))

        Qi = np.array(Qi)

        # -------------------------
        # Output
        # -------------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Load per Pile")

        for i, q in enumerate(Qi):
            st.write(f"Pile {i+1} = {q:,.2f} kN")

        st.markdown('</div>', unsafe_allow_html=True)

        # -------------------------
        # Check
        # -------------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("⚠️ Check")

        if np.min(Qi) < 0:
            st.error("❌ มีแรงดึง (Pile uplift)")
        else:
            st.success("✅ ทุกต้นรับแรงอัด")

        st.write(f"Max Load = {np.max(Qi):,.2f} kN")

        st.markdown('</div>', unsafe_allow_html=True)
