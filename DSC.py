import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Pile Group – Eccentric Load", page_icon="🏗️", layout="wide")

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Sarabun:wght@300;400;600;700&display=swap');
:root{
  --bg:#0d1117;--surface:#161b22;--border:#30363d;
  --accent:#58a6ff;--accent2:#1f6feb;--gold:#f0a500;
  --text:#e6edf3;--muted:#8b949e;
  --ok:#3fb950;--warn:#d29922;--danger:#f85149;
  --r:10px;
}
html,body,[class*="css"]{font-family:'Sarabun',sans-serif;background:var(--bg)!important;color:var(--text)!important;}
.block-container{padding:1.8rem 2.5rem 4rem!important;}

/* hero */
.hero{background:linear-gradient(135deg,#0d1f38,#0d1117 60%,#0a1a0d);
  border:1px solid var(--border);border-left:5px solid var(--accent);
  border-radius:var(--r);padding:1.6rem 2rem;margin-bottom:1.8rem;position:relative;overflow:hidden;}
.hero::before{content:"";position:absolute;top:-50px;right:-50px;width:200px;height:200px;
  border:45px solid rgba(88,166,255,.05);border-radius:50%;}
.hero h1{font-size:1.7rem;font-weight:700;color:var(--accent);margin:0 0 .3rem;}
.hero p{color:var(--muted);font-size:.85rem;margin:0;}
.badge{display:inline-block;background:rgba(88,166,255,.1);color:var(--accent);
  border:1px solid rgba(88,166,255,.3);border-radius:4px;
  font-size:.68rem;font-family:'IBM Plex Mono',monospace;
  padding:.15rem .5rem;margin-bottom:.5rem;letter-spacing:.06em;}

/* cards */
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:1.2rem 1.4rem;margin-bottom:1.2rem;}
.card-title{font-size:.68rem;font-weight:700;letter-spacing:.12em;color:var(--muted);
  text-transform:uppercase;margin-bottom:.9rem;padding-bottom:.45rem;border-bottom:1px solid var(--border);}

/* formula */
.formula{background:rgba(88,166,255,.04);border:1px solid rgba(88,166,255,.2);
  border-radius:8px;padding:.9rem 1.1rem;
  font-family:'IBM Plex Mono',monospace;font-size:.85rem;color:var(--accent);line-height:2;}

/* result metric */
.res-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:.8rem;margin-top:.6rem;}
.res-card{background:var(--bg);border:1px solid var(--border);border-radius:var(--r);
  padding:.9rem .8rem;text-align:center;}
.res-label{font-size:.65rem;color:var(--muted);letter-spacing:.07em;text-transform:uppercase;margin-bottom:.3rem;}
.res-val{font-size:1.55rem;font-weight:700;font-family:'IBM Plex Mono',monospace;}
.res-unit{font-size:.68rem;color:var(--muted);margin-top:.15rem;}
.ok{border-top:3px solid var(--ok);} .ok .res-val{color:var(--ok);}
.warn{border-top:3px solid var(--warn);} .warn .res-val{color:var(--warn);}
.danger{border-top:3px solid var(--danger);} .danger .res-val{color:var(--danger);}

/* table */
.ft{width:100%;border-collapse:collapse;font-size:.82rem;}
.ft th{background:rgba(88,166,255,.08);color:var(--accent);text-transform:uppercase;
  font-size:.67rem;letter-spacing:.07em;padding:.5rem .7rem;border:1px solid var(--border);}
.ft td{padding:.45rem .7rem;border:1px solid var(--border);font-family:'IBM Plex Mono',monospace;}
.ft tr:nth-child(even) td{background:rgba(255,255,255,.02);}
.ft .sum-row td{background:rgba(88,166,255,.06);color:var(--accent);font-weight:600;}
.ft .max-row td{background:rgba(248,81,73,.06);color:var(--danger);font-weight:600;}
.ft .min-row td{background:rgba(63,185,80,.06);color:var(--ok);font-weight:600;}

/* info strip */
.istrip{border-radius:7px;padding:.65rem 1rem;font-size:.8rem;margin-top:.8rem;}
.istrip.ok{background:rgba(63,185,80,.06);border:1px solid rgba(63,185,80,.25);color:var(--ok);}
.istrip.warn{background:rgba(210,153,34,.06);border:1px solid rgba(210,153,34,.25);color:var(--warn);}
.istrip.danger{background:rgba(248,81,73,.06);border:1px solid rgba(248,81,73,.25);color:var(--danger);}

div[data-testid="stNumberInput"] input{
  background:var(--bg)!important;border:1px solid var(--border)!important;
  border-radius:6px!important;color:var(--text)!important;
  font-family:'IBM Plex Mono',monospace!important;font-size:.87rem!important;}
div[data-testid="stNumberInput"] input:focus{border-color:var(--accent)!important;box-shadow:0 0 0 3px rgba(88,166,255,.12)!important;}
label[data-testid="stWidgetLabel"] p{font-size:.82rem!important;}

div[data-testid="stButton"] button{border-radius:7px!important;font-weight:600!important;
  font-size:.87rem!important;padding:.5rem 1.4rem!important;transition:all .2s!important;width:100%;}
div[data-testid="stAppViewContainer"]{background:var(--bg)!important;}
div[data-testid="stHeader"]{background:transparent!important;}
hr{border-color:var(--border)!important;margin:1.2rem 0!important;}
</style>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="badge">GEOTECHNICAL · PILE GROUP ANALYSIS</div>
  <h1>🏗️ คำนวณแรงปฏิกิริยาเสาเข็ม – เยื้องศูนย์แบบสมมาตร</h1>
  <p>สูตร Terzaghi-Meyerhof สำหรับกลุ่มเสาเข็มรับโมเมนต์สองทิศทาง &nbsp;·&nbsp; หน่วย: kN, m</p>
</div>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "n_piles" not in st.session_state:
    st.session_state.n_piles = 4
if "result" not in st.session_state:
    st.session_state.result = None

# ── LAYOUT ───────────────────────────────────────────────────────────────────
left, right = st.columns([1, 1.2], gap="large")

# ════════════════════════════════════════════════════════════
#  LEFT – INPUTS
# ════════════════════════════════════════════════════════════
with left:
    # ── Formula card ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📐 สูตรที่ใช้คำนวณ</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="formula">
  P<sub>i</sub> = (Q/n) + (M<sub>y</sub>·x<sub>i</sub> / Σx²) + (M<sub>x</sub>·y<sub>i</sub> / Σy²)<br><br>
  โดยที่:<br>
  &nbsp; Q &nbsp;= แรงกระทำในแนวดิ่งรวม (kN)<br>
  &nbsp; n &nbsp;= จำนวนเสาเข็มทั้งหมด<br>
  &nbsp; Mₓ = โมเมนต์รอบแกน x (kN·m)<br>
  &nbsp; M_y = โมเมนต์รอบแกน y (kN·m)<br>
  &nbsp; x<sub>i</sub>, y<sub>i</sub> = ระยะจาก Centroid ถึงเสาเข็มต้นที่ i<br>
  &nbsp; Σx², Σy² = ผลรวมกำลังสองของระยะ
</div>
""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Global loads ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">⚡ แรงกระทำและโมเมนต์</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        Q = st.number_input("Q (kN)", min_value=0.0, value=1200.0, step=10.0,
                            help="แรงแนวดิ่งรวมที่กระทำบนฐานราก")
    with c2:
        Mx = st.number_input("Mₓ (kN·m)", value=150.0, step=5.0,
                             help="โมเมนต์รอบแกน x")
    with c3:
        My = st.number_input("Mᵧ (kN·m)", value=100.0, step=5.0,
                             help="โมเมนต์รอบแกน y")

    Qc = st.number_input("กำลังรับน้ำหนักของเสาเข็มแต่ละต้น P_allow (kN)",
                         min_value=1.0, value=400.0, step=10.0,
                         help="ใช้เปรียบเทียบกับ P_i ที่คำนวณได้")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Number of piles ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🔢 จำนวนและพิกัดเสาเข็ม</div>', unsafe_allow_html=True)
    n_piles = st.number_input("จำนวนเสาเข็ม n (ต้น)", min_value=2, max_value=20,
                               value=st.session_state.n_piles, step=1)
    st.session_state.n_piles = n_piles

    st.markdown("""
<div style="font-size:.78rem;color:#8b949e;margin:.4rem 0 .9rem;line-height:1.6;">
  ℹ️ ใส่พิกัด (x, y) ของแต่ละเสาเข็ม <b>วัดจาก Centroid (C.G.) ของกลุ่มเสาเข็ม</b><br>
  &nbsp;&nbsp;&nbsp; ค่าเป็น + หรือ − ขึ้นอยู่กับทิศทาง
</div>
""", unsafe_allow_html=True)

    # Dynamic pile coordinate inputs
    pile_data = []
    for i in range(n_piles):
        ca, cb = st.columns(2)
        with ca:
            xi = st.number_input(f"x_{i+1} (m)", value=0.0, step=0.1,
                                  key=f"x_{i}", format="%.2f",
                                  label_visibility="visible")
        with cb:
            yi = st.number_input(f"y_{i+1} (m)", value=0.0, step=0.1,
                                  key=f"y_{i}", format="%.2f",
                                  label_visibility="visible")
        pile_data.append((f"Pile_{i+1}", xi, yi))

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Buttons ──
    bA, bB = st.columns(2)
    with bA:
        calc = st.button("🔢 คำนวณ (Calculate)", type="primary")
    with bB:
        reset = st.button("🗑️ ล้างค่า (Reset)")

    if reset:
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    if calc:
        sum_x2 = sum(x**2 for _, x, _ in pile_data)
        sum_y2 = sum(y**2 for _, _, y in pile_data)
        rows = []
        for name, xi, yi in pile_data:
            Pi = (Q / n_piles) + (My * xi / sum_x2 if sum_x2 != 0 else 0) + (Mx * yi / sum_y2 if sum_y2 != 0 else 0)
            rows.append({"เสาเข็ม": name, "x (m)": xi, "x² (m²)": xi**2,
                         "y (m)": yi, "y² (m²)": yi**2, "Pᵢ (kN)": Pi})
        df = pd.DataFrame(rows)
        st.session_state.result = dict(
            df=df, Q=Q, Mx=Mx, My=My, n=n_piles,
            sum_x2=sum_x2, sum_y2=sum_y2, Qc=Qc
        )
        st.rerun()

# ════════════════════════════════════════════════════════════
#  RIGHT – RESULTS
# ════════════════════════════════════════════════════════════
with right:
    res = st.session_state.result

    if res is None:
        st.markdown("""
<div class="card" style="text-align:center;padding:4rem 1rem;color:#555;">
  <div style="font-size:3rem;margin-bottom:.8rem">⬅️</div>
  <div style="font-size:1rem;font-weight
