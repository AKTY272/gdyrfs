import streamlit as st
import numpy as np

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Shallow Foundation Tool",
    page_icon="🏗️",
    layout="centered"
)

# -------------------------
# CSS (UI ให้ดูโปร)
# -------------------------
st.markdown("""
<style>
.block-container {padding-top: 2rem;}
.card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.title {font-size: 28px; font-weight: 700;}
.subtitle {color: gray;}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.markdown('<div class="title">🏗️ Shallow Foundation Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Terzaghi Bearing Capacity</div>', unsafe_allow_html=True)

# -------------------------
# Input
# -------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📥 Input")

c1, c2 = st.columns(2)

with c1:
    B = st.slider("Width B (m)", 0.5, 10.0, 2.0)
    D = st.slider("Depth D (m)", 0.5, 10.0, 1.0)

with c2:
    c = st.slider("Cohesion c (kPa)", 0.0, 100.0, 10.0)
    phi = st.slider("φ (deg)", 0.0, 45.0, 30.0)
    gamma = st.slider("γ (kN/m³)", 10.0, 25.0, 18.0)
    FS = st.slider("FS", 1.0, 5.0, 3.0)

run = st.button("🚀 Calculate")
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Calculation
# -------------------------
if run:
    phi_r = np.radians(phi)

    Nq = np.exp(np.pi * np.tan(phi_r)) * (np.tan(np.radians(45)+phi_r/2))**2
    Nc = 5.7 if phi == 0 else (Nq-1)/np.tan(phi_r)
    Ng = 2*(Nq+1)*np.tan(phi_r)

    qult = c*Nc + gamma*D*Nq + 0.5*gamma*B*Ng
    qall = qult / FS

    # -------------------------
    # Result
    # -------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Result")

    r1, r2, r3 = st.columns(3)
    r1.metric("q_ult", f"{qult:,.2f} kPa")
    r2.metric("q_all", f"{qall:,.2f} kPa")
    r3.metric("q_safe", f"{qall:,.2f} kPa")

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------
    # Graph (no lib)
    # -------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📈 Behavior")

    mode = st.selectbox("เลือกกราฟ", ["q vs B", "q vs φ"])

    if mode == "q vs B":
        Bv = np.linspace(0.5, 10, 50)
        qv = []

        for b in Bv:
            qu = c*Nc + gamma*D*Nq + 0.5*gamma*b*Ng
            qv.append(qu/FS)

        st.line_chart(qv)

    else:
        pv = np.linspace(0, 45, 50)
        qv = []

        for p in pv:
            pr = np.radians(p)
            Nq2 = np.exp(np.pi*np.tan(pr))*(np.tan(np.radians(45)+pr/2))**2
            Nc2 = 5.7 if p == 0 else (Nq2-1)/np.tan(pr)
            Ng2 = 2*(Nq2+1)*np.tan(pr)

            qu = c*Nc2 + gamma*D*Nq2 + 0.5*gamma*B*Ng2
            qv.append(qu/FS)

        st.line_chart(qv)

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------
    # Professional Diagram (SVG)
    # -------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏗️ Foundation Diagram")

    scale = 50
    w = B*scale
    d = D*scale

    svg = f"""
    <svg width="420" height="300">

    <!-- Ground -->
    <line x1="50" y1="120" x2="370" y2="120" stroke="black" stroke-width="2"/>

    <!-- Footing -->
    <rect x="{210-w/2}" y="120" width="{w}" height="35"
          fill="#4da6ff" stroke="black"/>

    <!-- Load -->
    <line x1="210" y1="60" x2="210" y2="120"
          stroke="red" stroke-width="2"/>
    <text x="215" y="80" fill="red">P</text>

    <!-- Width -->
    <line x1="{210-w/2}" y1="180" x2="{210+w/2}" y2="180"
          stroke="black" marker-start="url(#a)" marker-end="url(#a)"/>
    <text x="210" y="200" text-anchor="middle">B = {B:.2f} m</text>

    <!-- Depth -->
    <line x1="60" y1="120" x2="60" y2="{120+d}"
          stroke="black" marker-start="url(#a)" marker-end="url(#a)"/>
    <text x="65" y="{120+d/2}">D = {D:.2f} m</text>

    <defs>
    <marker id="a" markerWidth="10" markerHeight="10"
        refX="5" refY="5" orient="auto">
        <path d="M0,0 L10,5 L0,10 z" fill="black"/>
    </marker>
    </defs>

    </svg>
    """

    st.markdown(svg, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
