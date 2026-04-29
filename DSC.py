import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Pile Group – Eccentric Load", page_icon="🏗️", layout="wide")

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
body {background:#0d1117;color:#e6edf3;font-family:sans-serif;}
.card{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:1rem;margin-bottom:1rem;}
</style>
""", unsafe_allow_html=True)

# ── SESSION ──────────────────────────────────────────────────────────────────
if "n_piles" not in st.session_state:
    st.session_state.n_piles = 4
if "result" not in st.session_state:
    st.session_state.result = None

left, right = st.columns([1,1.2])

# ═════════ LEFT ═════════
with left:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📐 สูตร")

    st.markdown("""
Pᵢ = (Q/n) + (Mᵧ·xᵢ / Σx²) + (Mₓ·yᵢ / Σy²)
""")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("⚡ Loads")

    Q = st.number_input("Q (kN)", value=1200.0)
    Mx = st.number_input("Mx (kN·m)", value=150.0)
    My = st.number_input("My (kN·m)", value=100.0)
    Qc = st.number_input("Pile capacity (kN)", value=400.0)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📍 Coordinates")

    n = st.number_input("Number of piles", min_value=2, max_value=20, value=st.session_state.n_piles)
    st.session_state.n_piles = n

    pile_data = []
    for i in range(n):
        x = st.number_input(f"x{i+1}", key=f"x{i}")
        y = st.number_input(f"y{i+1}", key=f"y{i}")
        pile_data.append((f"P{i+1}", x, y))

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Calculate"):
        sum_x2 = sum(x**2 for _, x, _ in pile_data)
        sum_y2 = sum(y**2 for _, _, y in pile_data)

        rows = []
        for name, x, y in pile_data:
            Pi = (Q/n) + (My*x/sum_x2 if sum_x2 else 0) + (Mx*y/sum_y2 if sum_y2 else 0)
            rows.append([name, x, y, Pi])

        df = pd.DataFrame(rows, columns=["Pile","x","y","P (kN)"])
        st.session_state.result = df

# ═════════ RIGHT ═════════
with right:

    res = st.session_state.result

    if res is None:
        st.markdown("""
<div class="card" style="text-align:center;padding:3rem;">
    <h3>⬅️ กรอกข้อมูลแล้วกด Calculate</h3>
</div>
""", unsafe_allow_html=True)

    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Results")

        st.dataframe(res)

        max_load = res["P (kN)"].max()
        min_load = res["P (kN)"].min()

        st.write(f"Max Load = {max_load:.2f} kN")
        st.write(f"Min Load = {min_load:.2f} kN")

        if max_load > Qc:
            st.error("❌ เกินกำลังรับน้ำหนักเสาเข็ม")
        else:
            st.success("✅ ปลอดภัย")

        st.markdown('</div>', unsafe_allow_html=True)
