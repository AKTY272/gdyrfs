import streamlit as st
import numpy as np

st.set_page_config(layout="wide")

# -------------------------
# CSS (แก้ readability)
# -------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: #eef3f8;
}

/* ตัวหนังสือ */
* {
    color: #000000 !important;
}

/* input */
input {
    background-color: white !important;
    color: black !important;
}

/* dropdown */
div[data-baseweb="select"] > div {
    background-color: white !important;
    color: black !important;
}

/* card */
.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏗️ Pile Group Designer (Smart Input)")

col1, col2 = st.columns(2)

# -------------------------
# INPUT (ง่ายขึ้น)
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
# GENERATE PILES
# -------------------------
def generate_layout(layout, sx, sy):
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
# OUTPUT
# -------------------------
with col2:
    if run:

        x, y = generate_layout(layout, sx, sy)
        n = len(x)

        # centroid
        x_bar = np.mean(x)
        y_bar = np.mean(y)

        # moment
        Mx = P * ey
        My = P * ex

        Ix = np.sum((y - y_bar)**2)
        Iy = np.sum((x - x_bar)**2)

        Qi = (P / n) + (Mx * (y - y_bar)/Ix) + (My * (x - x_bar)/Iy)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Result")

        st.write(f"Centroid: ({x_bar:.2f}, {y_bar:.2f})")
        st.write(f"Max Load: {np.max(Qi):.2f} kN")
        st.write(f"Min Load: {np.min(Qi):.2f} kN")

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📋 Load per Pile")

        for i in range(n):
            st.write(f"Pile {i+1}: {Qi[i]:.2f} kN")

        st.markdown('</div>', unsafe_allow_html=True)

        if np.min(Qi) < 0:
            st.error("❌ Uplift เกิดขึ้น")
        else:
            st.success("✅ Safe")
