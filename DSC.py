import streamlit as st
import numpy as np

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Pile Foundation Designer",
    page_icon="🏗️",
    layout="wide"
)

# -------------------------
# CSS (สวย + ตัวหนังสือดำทั้งหมด)
# -------------------------
st.markdown("""
<style>

/* พื้นหลัง */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #eef3f8, #ffffff);
}

/* ตัวหนังสือทั้งหมด */
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] * {
    color: #000000 !important;
    font-family: 'Segoe UI', sans-serif;
}

/* หัวข้อ */
h1 {
    font-weight: 800;
}

/* Card */
.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* ปุ่ม */
.stButton>button {
    background: linear-gradient(90deg, #1565c0, #42a5f5);
    color: white !important;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-weight: 600;
}

/* Result box */
.result-box {
    background: #f1f6ff;
    padding: 20px;
    border-radius: 12px;
    border-left: 6px solid #1565c0;
    font-size: 18px;
}

/* Table */
table {
    width: 100%;
    border-collapse: collapse;
}
th {
    background: #1565c0;
    color: white;
    padding: 10px;
}
td {
    padding: 10px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Title
# -------------------------
st.title("🏗️ Pile Foundation Designer")
st.caption("Eccentric Load Distribution (Pile Group)")

# -------------------------
# Layout
# -------------------------
col1, col2 = st.columns([1,1])

# -------------------------
# INPUT
# -------------------------
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📥 Input")

    P = st.number_input("Axial Load P (kN)", value=1000.0)
    e = st.number_input("Eccentricity e (m)", value=0.5)

    n = st.selectbox("Number of Piles", [2, 4, 6])
    spacing = st.number_input("Pile spacing (m)", value=2.0)

    run = st.button("🚀 Calculate")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# OUTPUT
# -------------------------
with col2:

    if run:

        M = P * e

        # pile position (1D simplification)
        if n == 2:
            x = np.array([-spacing/2, spacing/2])

        elif n == 4:
            x = np.array([-spacing/2, spacing/2, -spacing/2, spacing/2])

        else:
            x = np.array([-spacing, 0, spacing, -spacing, 0, spacing])

        sum_x2 = np.sum(x**2)

        Qi = (P / n) + (M * x / sum_x2)

        # -------------------------
        # Summary
        # -------------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Summary")

        st.markdown(f"""
        <div class="result-box">
        <b>Total Load</b> = {P:,.2f} kN <br>
        <b>Moment</b> = {M:,.2f} kN·m <br><br>
        <b>Max Load</b> = {np.max(Qi):,.2f} kN <br>
        <b>Min Load</b> = {np.min(Qi):,.2f} kN
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # -------------------------
        # Table
        # -------------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📋 Load per Pile")

        table = "<table><tr><th>Pile</th><th>Load (kN)</th></tr>"
        for i, q in enumerate(Qi):
            table += f"<tr><td>{i+1}</td><td>{q:,.2f}</td></tr>"
        table += "</table>"

        st.markdown(table, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # -------------------------
        # Check
        # -------------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("⚠️ Design Check")

        if np.min(Qi) < 0:
            st.error("❌ มีแรงดึง (Pile Uplift)")
        else:
            st.success("✅ ทุกต้นรับแรงอัด")

        st.markdown('</div>', unsafe_allow_html=True)
