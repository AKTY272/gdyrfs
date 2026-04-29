import streamlit as st
import numpy as np

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Shallow Foundation Calculator",
                   page_icon="🏗️",
                   layout="centered")

# -------------------------
# Custom CSS (UI สวย)
# -------------------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.stButton>button {
    background-color: #1f77b4;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
.result-box {
    background-color: #e8f0fe;
    padding: 15px;
    border-radius: 10px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Title
# -------------------------
st.title("🏗️ Shallow Foundation Bearing Capacity")
st.subheader("Terzaghi Method")

# -------------------------
# Input Section
# -------------------------
st.markdown("### 🔢 Input Parameters")

col1, col2 = st.columns(2)

with col1:
    B = st.number_input("Width B (m)", min_value=0.0)
    L = st.number_input("Length L (m)", min_value=0.0)
    D = st.number_input("Depth D (m)", min_value=0.0)

with col2:
    c = st.number_input("Cohesion c (kPa)", min_value=0.0)
    phi = st.number_input("Friction angle φ (deg)", min_value=0.0)
    gamma = st.number_input("Unit weight γ (kN/m³)", min_value=0.0)
    FS = st.number_input("Factor of Safety (FS)", min_value=1.0, value=3.0)

# -------------------------
# Buttons
# -------------------------
col_btn1, col_btn2 = st.columns(2)

calculate = col_btn1.button("🔍 Calculate")
clear = col_btn2.button("🧹 Clear")

# -------------------------
# Clear Logic
# -------------------------
if clear:
    st.experimental_rerun()

# -------------------------
# Calculation
# -------------------------
if calculate:

    if B == 0 or D == 0 or FS == 0:
        st.warning("⚠️ กรุณากรอกข้อมูลให้ครบถ้วน")
    else:
        phi_rad = np.radians(phi)

        # Bearing capacity factors
        Nq = np.exp(np.pi * np.tan(phi_rad)) * (np.tan(np.radians(45) + phi_rad/2))**2
        
        if phi == 0:
            Nc = 5.7   # special case
        else:
            Nc = (Nq - 1) / np.tan(phi_rad)

        Ngamma = 2 * (Nq + 1) * np.tan(phi_rad)

        # Terzaghi equation
        qult = c * Nc + gamma * D * Nq + 0.5 * gamma * B * Ngamma

        qall = qult / FS
        qf = qall

        # -------------------------
        # Output
        # -------------------------
        st.markdown("### 📊 Results")

        st.markdown(f"""
        <div class="result-box">
        <b>Ultimate Bearing Capacity (q<sub>ult</sub>)</b> = {qult:,.2f} kPa <br><br>
        <b>Allowable Bearing Capacity (q<sub>all</sub>)</b> = {qall:,.2f} kPa <br><br>
        <b>Safe Bearing Capacity (q<sub>f</sub>)</b> = {qf:,.2f} kPa
        </div>
        """, unsafe_allow_html=True)
