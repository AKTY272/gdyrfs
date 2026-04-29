import streamlit as st
import numpy as np

st.set_page_config(layout="wide")

# -------------------------
# CSS (อ่านง่าย)
# -------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: #eef3f8;
}
* { color: #000000 !important; }

input {
    background: white !important;
    color: black !important;
}
div[data-baseweb="select"] > div {
    background: white !important;
    color: black !important;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏗️ Pile Load + Eccentricity Tool")

col1, col2 = st.columns(2)

# -------------------------
# INPUT
# -------------------------
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    layout = st.selectbox("Layout", ["2x2", "3x3", "2x3"])

    sx = st.number_input("Spacing X (m)", value=2.0)
    sy = st.number_input("Spacing Y (m)", value=2.0)

    P = st.number_input("Load P (kN)", value=1000.0)
    ex = st.number_input("Eccentricity ex (m)", value=0.2)
    ey = st.number_input("Eccentricity ey (m)", value=0.0)

    run = st.button("🚀 Calculate")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# LAYOUT GENERATOR
# -------------------------
def generate(layout, sx, sy):
    if layout == "2x2":
        x = [-sx/2, sx/2, -sx/2, sx/2]
        y = [-sy/2, -sy/2, sy/2, sy/2]

    elif layout == "3x3":
        x, y = [], []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                x.append(i*sx)
                y.append(j*sy)

    else:  # 2x3
        x, y = [], []
        for i in [-1,0,1]:
            for j in [-0.5,0.5]:
                x.append(i*sx)
                y.append(j*sy)

    return np.array(x), np.array(y)

# -------------------------
# CALCULATION
# -------------------------
with col2:
    if run:

        x, y = generate(layout, sx, sy)
        n = len(x)

        # centroid
        x_bar = np.mean(x)
        y_bar = np.mean(y)

        # eccentricity ของแต่ละเสา
        ex_i = x - x_bar
        ey_i = y - y_bar

        # moment
        Mx = P * ey
        My = P * ex

        # inertia
        Ix = np.sum(ey_i**2)
        Iy = np.sum(ex_i**2)

        # load per pile
        Pi = (P / n) + (Mx * ey_i / Ix) + (My * ex_i / Iy)

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("📍 Centroid")
        st.write(f"x̄ = {x_bar:.2f} m")
        st.write(f"ȳ = {y_bar:.2f} m")

        st.subheader("📊 Result per Pile")

        for i in range(n):
            st.write(
                f"Pile {i+1}:  Pi = {Pi[i]:.2f} kN | "
                f"ex = {ex_i[i]:.2f} m | ey = {ey_i[i]:.2f} m"
            )

        if np.min(Pi) < 0:
            st.error("❌ มีแรงดึง (uplift)")
        else:
            st.success("✅ Safe")

        st.markdown('</div>', unsafe_allow_html=True)
