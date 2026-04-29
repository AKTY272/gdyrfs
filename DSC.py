import streamlit as st
import numpy as np

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Foundation Calculator",
    page_icon="🏗️",
    layout="centered"
)

# -------------------------
# CSS (สวย)
# -------------------------
st.markdown("""
<style>
.stApp {background-color: #f4f7fb;}
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    color: #1f2a44;
}
h1 {color: #0d47a1;}
h2, h3 {color: #1565c0;}

.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

label {
    font-weight: 600;
    color: #0d47a1 !important;
}

.stButton>button {
    background: linear-gradient(90deg, #1565c0, #42a5f5);
    color: white;
    border-radius: 12px;
    height: 3em;
    border: none;
    font-weight: 600;
}

.result-box {
    background: linear-gradient(135deg, #e3f2fd, #ffffff);
    padding: 20px;
    border-radius: 15px;
    font-size: 18px;
    border-left: 6px solid #1565c0;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Title
# -------------------------
st.title("🏗️ Foundation Calculator")
st.subheader("Terzaghi + Eccentric Load")

# -------------------------
# INPUT
# -------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📥 Input Parameters")

col1, col2 = st.columns(2)

with col1:
    B = st.number_input("Width B (m)", min_value=0.0)
    L = st.number_input("Length L (m)", min_value=0.0)
    D = st.number_input("Depth D (m)", min_value=0.0)

with col2:
    c = st.number_input("Cohesion c (kPa)", min_value=0.0)
    phi = st.number_input("Friction angle φ (deg)", min_value=0.0)
    gamma = st.number_input("Unit weight γ (kN/m³)", min_value=0.0)
    FS = st.number_input("Factor of Safety", min_value=1.0, value=3.0)

st.markdown("### ⚖️ Eccentric Load")
P = st.number_input("Load P (kN)", min_value=0.0)
e = st.number_input("Eccentricity e (m)", min_value=0.0)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# BUTTON
# -------------------------
colb1, colb2 = st.columns(2)
run = colb1.button("🚀 Calculate")
clear = colb2.button("🧹 Clear")

if clear:
    st.experimental_rerun()

# -------------------------
# CALCULATION
# -------------------------
if run:

    if B == 0 or D == 0 or FS == 0:
        st.warning("⚠️ กรุณากรอกข้อมูลให้ครบ")
    else:
        phi_r = np.radians(phi)

        # Terzaghi factors
        Nq = np.exp(np.pi * np.tan(phi_r)) * (np.tan(np.radians(45)+phi_r/2))**2
        Nc = 5.7 if phi == 0 else (Nq-1)/np.tan(phi_r)
        Ng = 2*(Nq+1)*np.tan(phi_r)

        # Bearing capacity
        qult = c*Nc + gamma*D*Nq + 0.5*gamma*B*Ng
        qall = qult / FS

        # -------------------------
        # Result: Bearing
        # -------------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Bearing Capacity")

        st.markdown(f"""
        <div class="result-box">
        <b>q_ult</b> = {qult:,.2f} kPa <br><br>
        <b>q_all</b> = {qall:,.2f} kPa
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # -------------------------
        # Eccentric Load
        # -------------------------
        if P > 0 and e > 0 and L > 0:

            A = B * L
            M = P * e

            # section modulus (assume bending along L)
            Z = (B * L**2) / 6

            q_max = (P / A) + (M / Z)
            q_min = (P / A) - (M / Z)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("⚖️ Eccentric Load Result")

            st.markdown(f"""
            <div class="result-box">
            <b>q_max</b> = {q_max:,.2f} kPa <br><br>
            <b>q_min</b> = {q_min:,.2f} kPa
            </div>
            """, unsafe_allow_html=True)

            # Check condition
            if q_min < 0:
                st.error("❌ เกิด Uplift (ฐานยก)")
            else:
                st.success("✅ Safe (ไม่มี uplift)")

            # eccentricity check
            if e > B/6:
                st.warning("⚠️ e > B/6 → เสี่ยง overturning")

            st.markdown('</div>', unsafe_allow_html=True)
