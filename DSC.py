import streamlit as st
import numpy as np

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Pile Group Centroid Tool",
    page_icon="🏗️",
    layout="wide"
)

# -------------------------
# CSS
# -------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: #eef3f8;
}
[data-testid="stAppViewContainer"] * {
    color: #1a1a1a !important;
    font-family: 'Segoe UI', sans-serif;
}
.card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.stButton>button {
    background: #1565c0;
    color: white !important;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
.result {
    background: #f1f6ff;
    padding: 20px;
    border-radius: 12px;
    border-left: 6px solid #1565c0;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Title
# -------------------------
st.title("🏗️ Pile Group Centroid Calculator")
st.caption("Centroid + Eccentric Load Effect")

col1, col2 = st.columns(2)

# -------------------------
# INPUT
# -------------------------
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📥 Input")

    n = st.number_input("Number of piles", min_value=1, value=4)

    st.write("📍 ใส่ตำแหน่งเสาเข็ม (x, y)")

    x = []
    y = []

    for i in range(int(n)):
        c1, c2 = st.columns(2)
        xi = c1.number_input(f"x{i+1} (m)", value=0.0, key=f"x{i}")
        yi = c2.number_input(f"y{i+1} (m)", value=0.0, key=f"y{i}")
        x.append(xi)
        y.append(yi)

    P = st.number_input("Load P (kN)", value=1000.0)
    ex = st.number_input("Eccentricity ex (m)", value=0.0)
    ey = st.number_input("Eccentricity ey (m)", value=0.0)

    run = st.button("🚀 Calculate")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# CALCULATION
# -------------------------
with col2:
    if run:

        x = np.array(x)
        y = np.array(y)

        # -------------------------
        # Original Centroid
        # -------------------------
        x_bar = np.mean(x)
        y_bar = np.mean(y)

        # -------------------------
        # Moment
        # -------------------------
        Mx = P * ey   # moment about x
        My = P * ex   # moment about y

        # -------------------------
        # Distribution
        # -------------------------
        Ix = np.sum((y - y_bar)**2)
        Iy = np.sum((x - x_bar)**2)

        Qi = (P / n) + (Mx * (y - y_bar) / Ix) + (My * (x - x_bar) / Iy)

        # -------------------------
        # New centroid (weighted)
        # -------------------------
        x_new = np.sum(Qi * x) / np.sum(Qi)
        y_new = np.sum(Qi * y) / np.sum(Qi)

        # -------------------------
        # OUTPUT
        # -------------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Centroid")

        st.markdown(f"""
        <div class="result">
        <b>Original Centroid</b><br>
        x̄ = {x_bar:.2f} m <br>
        ȳ = {y_bar:.2f} m <br><br>

        <b>New Centroid (after load)</b><br>
        x = {x_new:.2f} m <br>
        y = {y_new:.2f} m
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # -------------------------
        # Load Table
        # -------------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📋 Load per Pile")

        for i in range(len(Qi)):
            st.write(f"Pile {i+1} → {Qi[i]:,.2f} kN")

        st.markdown('</div>', unsafe_allow_html=True)

        # -------------------------
        # Check
        # -------------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("⚠️ Check")

        if np.min(Qi) < 0:
            st.error("❌ มีแรงดึง (Uplift)")
        else:
            st.success("✅ ปลอดภัย")

        st.markdown('</div>', unsafe_allow_html=True)
