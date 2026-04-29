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
# UI Style
# -------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.title("🏗️ Shallow Foundation Calculator")
st.caption("Terzaghi Bearing Capacity Method")

# -------------------------
# Input
# -------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📥 Input Parameters")

col1, col2 = st.columns(2)

with col1:
    B = st.slider("Width B (m)", 0.1, 10.0, 2.0)
    L = st.slider("Length L (m)", 0.1, 10.0, 2.0)
    D = st.slider("Depth D (m)", 0.1, 10.0, 1.0)

with col2:
    c = st.slider("Cohesion c (kPa)", 0.0, 100.0, 10.0)
    phi = st.slider("Friction angle φ (deg)", 0.0, 45.0, 30.0)
    gamma = st.slider("Unit weight γ (kN/m³)", 10.0, 25.0, 18.0)
    FS = st.slider("Factor of Safety", 1.0, 5.0, 3.0)

calculate = st.button("🚀 Calculate")
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Calculation
# -------------------------
if calculate:

    phi_rad = np.radians(phi)

    Nq = np.exp(np.pi * np.tan(phi_rad)) * (np.tan(np.radians(45) + phi_rad/2))**2
    
    if phi == 0:
        Nc = 5.7
    else:
        Nc = (Nq - 1) / np.tan(phi_rad)

    Ngamma = 2 * (Nq + 1) * np.tan(phi_rad)

    qult = c * Nc + gamma * D * Nq + 0.5 * gamma * B * Ngamma
    qall = qult / FS

    # -------------------------
    # Results
    # -------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Results")

    col1, col2, col3 = st.columns(3)
    col1.metric("q_ult (kPa)", f"{qult:,.2f}")
    col2.metric("q_all (kPa)", f"{qall:,.2f}")
    col3.metric("q_safe (kPa)", f"{qall:,.2f}")

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------
    # Graph (no matplotlib)
    # -------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📈 Sensitivity Analysis")

    graph_type = st.selectbox(
        "เลือกกราฟ",
        ["q vs Width (B)", "q vs Friction angle (φ)"]
    )

    if graph_type == "q vs Width (B)":
        B_range = np.linspace(0.5, 10, 50)
        q_vals = []

        for b in B_range:
            Nq = np.exp(np.pi * np.tan(phi_rad)) * (np.tan(np.radians(45) + phi_rad/2))**2
            Nc = 5.7 if phi == 0 else (Nq - 1) / np.tan(phi_rad)
            Ngamma = 2 * (Nq + 1) * np.tan(phi_rad)

            qult_temp = c * Nc + gamma * D * Nq + 0.5 * gamma * b * Ngamma
            q_vals.append(qult_temp / FS)

        st.line_chart(q_vals)

    else:
        phi_range = np.linspace(0, 45, 50)
        q_vals = []

        for p in phi_range:
            phi_r = np.radians(p)
            Nq = np.exp(np.pi * np.tan(phi_r)) * (np.tan(np.radians(45) + phi_r/2))**2
            
            Nc = 5.7 if p == 0 else (Nq - 1) / np.tan(phi_r)
            Ngamma = 2 * (Nq + 1) * np.tan(phi_r)

            qult_temp = c * Nc + gamma * D * Nq + 0.5 * gamma * B * Ngamma
            q_vals.append(qult_temp / FS)

        st.line_chart(q_vals)

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------
    # Simple Diagram (no matplotlib)
    # -------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏗️ Footing Diagram")

    st.markdown(f"""
    ```
        Ground Level
    -----------------------
            |<-- B = {B} m -->|
            ┌───────────────┐
            │   FOOTING     │
            └───────────────┘
                ↑
                │  D = {D} m
                ↓
    ```
    """)

    st.markdown('</div>', unsafe_allow_html=True)
