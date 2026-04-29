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
# CSS (UI PRO)
# -------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef3f8, #ffffff);
    font-family: 'Segoe UI', sans-serif;
}

/* Header */
h1 {
    color: #0d47a1;
    font-weight: 800;
}
h3 {
    color: #1565c0;
}

/* Card */
.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* Input */
label {
    color: #0d47a1 !important;
    font-weight: 600;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #1565c0, #42a5f5);
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-weight: 600;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.03);
}

/* Result box */
.result-box {
    background: linear-gradient(135deg, #e3f2fd, #ffffff);
    padding: 20px;
    border-radius: 15px;
    border-left: 6px solid #1565c0;
    font-size: 18px;
}

/* Table */
table {
    border-collapse: collapse;
    width: 100%;
}
td, th {
    padding: 10px;
    text-align: center;
}
th {
    background-color: #1565c0;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Title
# -------------------------
st.title("🏗️ Pile Foundation Designer")
st.caption("Eccentric Load Distribution on Pile Group")

# -------------------------
# Layout
# -------------------------
col_input, col_output = st.columns([1, 1])

# -------------------------
# INPUT
# -------------------------
with col_input:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📥 Input")

    P = st.number_input("Axial Load P (kN)", min_value=0.0, value=1000.0)
    e = st.number_input("Eccentricity e (m)", min_value=0.0, value=0.5)

    n = st.selectbox("Number of Piles", [2, 4, 6])
    spacing = st.number_input("Pile spacing (m)", min_value=0.1, value=2.0)

    run = st.button("🚀 Calculate")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# OUTPUT
# -------------------------
with col_output:

    if run:

        M = P * e

        # pile layout
        if n == 2:
            x = np.array([-spacing/2, spacing/2])

        elif n == 4:
            x = np.array([-spacing/2, spacing/2, -spacing/2, spacing/2])

        else:
            x = np.array([-spacing, 0, spacing, -spacing, 0, spacing])

        sum_x2 = np.sum(x**2)

        Qi = (P / n) + (M * x / sum_x2)

        # -------------------------
        # RESULT BOX
        # -------------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Result Summary")

        st.markdown(f"""
        <div class="result-box">
        <b>Total Load (P)</b> = {P:,.2f} kN <br>
        <b>Moment (M)</b> = {M:,.2f} kN·m <br><br>
        <b>Max Pile Load</b> = {np.max(Qi):,.2f} kN <br>
        <b>Min Pile Load</b> = {np.min(Qi):,.2f} kN
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # -------------------------
        # TABLE
        # -------------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📋 Load per Pile")

        table_html = "<table><tr><th>Pile</th><th>Load (kN)</th></tr>"
        for i, q in enumerate(Qi):
            table_html += f"<tr><td>{i+1}</td><td>{q:,.2f}</td></tr>"
        table_html += "</table>"

        st.markdown(table_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # -------------------------
        # CHECK
        # -------------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("⚠️ Design Check")

        if np.min(Qi) < 0:
            st.error("❌ มีแรงดึงในเสาเข็ม (Uplift)")
        else:
            st.success("✅ ทุกเสาเข็มรับแรงอัด")

        st.markdown('</div>', unsafe_allow_html=True)
