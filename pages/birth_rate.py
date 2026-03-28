import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import base64
import os

st.set_page_config(
    page_title="Birth Rate Forecast",
    layout="wide",
    initial_sidebar_state="expanded",
)

def img_to_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
before_b64 = img_to_b64(os.path.join(BASE_DIR, "before_clean.jpg"))
after_b64  = img_to_b64(os.path.join(BASE_DIR, "after_clean.png"))

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=DM+Mono&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: #090b0f; color: #f1f5f9; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #07090f !important;
        border-right: none !important;
    }

    [data-testid="stSidebarNav"] {
        display: none;
    }

    [data-testid="stSidebarCollapseButton"], 
    [data-testid="collapsedControl"] {
        color: white !important;
    }

    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapseButton"] svg path,
    [data-testid="collapsedControl"] svg path {
        fill: white !important;
        stroke: white !important; 
        color: white !important;
    }

    [data-testid="stSidebarCollapseButton"]:hover svg,
    [data-testid="stSidebarCollapseButton"]:hover svg path,
    [data-testid="collapsedControl"]:hover svg,
    [data-testid="collapsedControl"]:hover svg path {
        fill: #cbd5e1 !important;
        stroke: #cbd5e1 !important;
    }
                
    div[data-testid="stPageLink"] a {
        background: #1e293b !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        padding: 1.1rem !important;
        border-radius: 12px !important;
        display: block !important;
        text-align: center !important;
        margin-top: 1rem;
    }

    div[data-testid="stPageLink"] a p {
        color: white !important;
        font-size: 1.35rem !important;
        font-weight: 700 !important;
    }

    div[data-testid="stPageLink"] a:hover {
        background: #334155 !important;
    }

    :root { --acc: #7dd3fc; --acc-dim: rgba(125,211,252,0.8); --acc-faint: rgba(125,211,252,0.15); }

    /* Layout */
    .hero { padding: 4.5rem 0 3rem; max-width: 640px; }
    .hero-eyebrow { font-size: 0.8rem; font-weight: 700; letter-spacing: 0.28em; text-transform: uppercase; color: #94a3b8; margin-bottom: 1rem; }
    .hero-title { font-family: 'DM Serif Display', serif; font-size: 3.2rem; font-weight: 400; color: #ffffff; line-height: 1.1; letter-spacing: -0.02em; margin: 0 0 1rem; }
    .hero-title em { font-style: italic; color: #cbd5e1; }
    .hero-body { font-size: 1.1rem; color: #cbd5e1; line-height: 1.8; font-weight: 300; }

    .divider { border: none; border-top: 1px solid rgba(255,255,255,0.05); margin: 2.5rem 0; }
    .sec-label { font-size: 0.8rem; font-weight: 700; letter-spacing: 0.25em; text-transform: uppercase; color: #94a3b8; margin-bottom: 1rem; }
    .sec-title { font-family: 'DM Serif Display', serif; font-size: 1.7rem; color: #ffffff; font-weight: 400; margin-bottom: 1.2rem; }

    /* Selectbox */
    div[data-testid="stSelectbox"] label,
    div[data-testid="stSelectbox"] p { color: #cbd5e1 !important; font-size: 1rem !important; font-weight: 500 !important; letter-spacing: 0.05em !important; }
    div[data-baseweb="select"] { background: #0b0e14 !important; border-color: rgba(125,211,252,0.3) !important; border-radius: 8px !important; }
    div[data-baseweb="select"] * { background: #0b0e14 !important; color: #ffffff !important; font-size: 1rem !important; }

    /* Button */
    .stButton button {
        background: rgba(125,211,252,0.15) !important;
        color: var(--acc) !important; border: 1px solid rgba(125,211,252,0.4) !important;
        border-radius: 8px !important; padding: 0.55rem 1.8rem !important;
        font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important;
        font-size: 1rem !important; letter-spacing: 0.06em !important;
        width: 100%; margin-top: 0.5rem; transition: background 0.2s !important;
    }
    .stButton button:hover { background: rgba(125,211,252,0.25) !important; color: #ffffff !important; }

    /* Result cards */
    .result-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 1px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; overflow: hidden; margin-top: 1.5rem; }
    .result-cell { background: #0b0e14; padding: 1.6rem 1.2rem; text-align: center; }
    .result-cell-label { font-size: 0.8rem; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 0.5rem; }
    .result-cell-label.male   { color: rgba(125,211,252,0.9); }
    .result-cell-label.female { color: rgba(240,128,167,0.9); }
    .result-cell-label.total  { color: rgba(154,205,130,0.9); }
    .result-cell-value { font-family: 'DM Serif Display', serif; font-size: 2.2rem; color: #ffffff; line-height: 1; }
    .result-cell-unit  { font-size: 0.85rem; color: #94a3b8; margin-top: 0.3rem; font-family: 'DM Mono', monospace; }
    .result-footnote { font-size: 0.85rem; color: #94a3b8; text-align: right; margin-top: 0.8rem; font-family: 'DM Mono', monospace; }

    /* Doc cards */
    .doc-card { background: #0b0e14; border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 1.8rem 1.8rem; margin-bottom: 1rem; }
    .doc-card-title { font-family: 'DM Serif Display', serif; font-size: 1.25rem; color: #ffffff; margin-bottom: 0.8rem; font-weight: 400; }
    .doc-card p { color: #cbd5e1; font-size: 1rem; line-height: 1.75; margin: 0 0 0.5rem; }
    .doc-card a { color: var(--acc); text-decoration: none; word-break: break-all; font-weight: 500; }
    .doc-card a:hover { color: #ffffff; }

    /* Step list */
    .step-list { margin: 0.5rem 0 0; padding: 0; list-style: none; }
    .step-list li { display: flex; gap: 0.75rem; align-items: flex-start; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 1rem; color: #cbd5e1; line-height: 1.6; }
    .step-list li:last-child { border-bottom: none; }
    .step-num { flex-shrink: 0; width: 24px; height: 24px; background: rgba(125,211,252,0.15); border-radius: 4px; color: var(--acc); font-size: 0.8rem; font-weight: 700; display: flex; align-items: center; justify-content: center; margin-top: 0.15rem; font-family: 'DM Mono', monospace; }

    /* Compare grid */
    .compare-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; overflow: hidden; margin-top: 1.2rem; }
    .compare-label { padding: 0.4rem 0.8rem; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; }
    .compare-label.before { background: rgba(240,100,80,0.15); color: rgba(240,100,80,0.9); border-bottom: 1px solid rgba(240,100,80,0.2); }
    .compare-label.after  { background: rgba(110,231,183,0.15); color: rgba(110,231,183,0.9); border-bottom: 1px solid rgba(110,231,183,0.2); }
    
    .compare-panel { background: #0b0e14; }
    .compare-panel img { 
        width: 100%; 
        height: 220px; 
        object-fit: contain; 
        display: block; 
        background: #090b0f; 
        padding: 0.5rem;
        cursor: zoom-in; /* เพิ่มลูกศรแว่นขยายให้รู้ว่ากดได้ */
        transition: opacity 0.2s ease;
    }
    .compare-panel img:hover {
        opacity: 0.7; /* เวลาชี้เมาส์ให้รูปจางลงนิดนึง */
    }

    /* 🔴 จุดที่เพิ่ม: ระบบ Lightbox ซูมรูป */
    .lightbox {
        display: none;
        position: fixed;
        z-index: 99999;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        background-color: rgba(9, 11, 15, 0.95);
        backdrop-filter: blur(5px);
        align-items: center;
        justify-content: center;
    }
    .lightbox:target {
        display: flex; /* แสดงขึ้นมาเมื่อถูกคลิกอ้างอิง ID */
    }
    .lightbox img {
        max-width: 90vw;
        max-height: 90vh;
        object-fit: contain;
        border-radius: 8px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .lightbox-close {
        position: absolute;
        top: 2rem; right: 3rem;
        color: #94a3b8;
        font-size: 3rem;
        text-decoration: none;
        transition: color 0.2s;
    }
    .lightbox-close:hover {
        color: #ffffff;
    }

    /* Feature table */
    .feat-table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; }
    .feat-table th { text-align: left; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: #94a3b8; padding: 0.45rem 0.7rem; border-bottom: 1px solid rgba(255,255,255,0.08); }
    .feat-table td { font-size: 1rem; color: #cbd5e1; padding: 0.5rem 0.7rem; border-bottom: 1px solid rgba(255,255,255,0.05); vertical-align: top; }
    .feat-table tr:last-child td { border-bottom: none; }
    .feat-table td:first-child { color: #94a3b8; font-family: 'DM Mono', monospace; font-size: 0.95rem; white-space: nowrap; }
    .feat-badge { display: inline-block; padding: 0.12rem 0.5rem; border-radius: 3px; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.05em; border: 1px solid; }
    .badge-lag    { border-color: rgba(125,211,252,0.4); color: rgba(125,211,252,0.9); }
    .badge-time   { border-color: rgba(240,180,100,0.4); color: rgba(240,180,100,0.9); }
    .badge-target { border-color: rgba(154,205,130,0.4); color: rgba(154,205,130,0.9); }

    /* Algo grid */
    .algo-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 1px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; overflow: hidden; margin-top: 0.8rem; }
    .algo-cell { background: #0b0e14; padding: 1.4rem 1.2rem; }
    .algo-name   { font-family: 'DM Serif Display', serif; font-size: 1.15rem; color: #ffffff; margin-bottom: 0.25rem; }
    .algo-weight { font-size: 0.8rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 0.75rem; }
    .algo-weight.xgb { color: rgba(240,180,100,0.9); }
    .algo-weight.rf  { color: rgba(125,211,252,0.9); }
    .algo-weight.lr  { color: rgba(192,132,252,0.9); }
    .algo-desc   { font-size: 1rem; color: #cbd5e1; line-height: 1.65; }

    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.page_link("app.py", label="Home")
    st.page_link("pages/butterfly.py", label="Butterfly Classifier")
    st.page_link("pages/birth_rate.py", label="Birth Rate Forecast")

# ── Hero ─────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">Thailand — National Statistics</div>
  <div class="hero-title">Birth Rate<br><em>Analytics</em></div>
  <div class="hero-body">
    วิเคราะห์แนวโน้มและคาดคะเนอัตราการเกิดด้วย Ensemble Machine Learning
    จากข้อมูลรายเดือน กรมการปกครอง ย้อนหลังกว่า 20 ปี
  </div>
</div>
""", unsafe_allow_html=True)

# ── Data ─────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("birth_data.csv")
    df["month"] = pd.to_datetime(df["month"])
    for c in ["male", "female", "total"]:
        df[c] = df[c].astype(str).str.replace(",", "").astype(float)
    return df

try:
    df = load_data()
except FileNotFoundError:
    df = pd.DataFrame({"month": pd.date_range("2000-01-01", periods=12, freq="M"), "male": [30000]*12, "female": [29000]*12, "total": [59000]*12})

PLOT_BG  = "#090b0f"
GRID_CLR = "rgba(255,255,255,0.08)"
TICK_CLR = "#94a3b8" 
AXIS_LBL = dict(font=dict(color=TICK_CLR, size=12))
HOVER_LBL = dict(bgcolor="#0d1220", bordercolor="rgba(125,211,252,0.4)", font=dict(family="DM Sans", color="#ffffff"))

def base_layout(h=320):
    return dict(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
        font=dict(family="DM Sans", color=TICK_CLR, size=13),
        xaxis=dict(gridcolor=GRID_CLR, tickfont=dict(color=TICK_CLR), title=dict(text="Year", **AXIS_LBL), showline=False),
        yaxis=dict(gridcolor=GRID_CLR, tickfont=dict(color=TICK_CLR), title=dict(text="Births", **AXIS_LBL), tickformat=","),
        hovermode="x unified", hoverlabel=HOVER_LBL,
        margin=dict(l=10, r=10, t=16, b=10), height=h,
    )

# Chart 1 — Male vs Female
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="sec-label">Historical Data</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-title">Births by Gender Over Time</div>', unsafe_allow_html=True)

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df["month"], y=df["male"],   name="Male",   mode="lines", line=dict(color="#63b3ed", width=1.8), fill="tozeroy", fillcolor="rgba(99,179,237,0.1)", hovertemplate="<b>Male</b><br>%{x|%b %Y}<br>%{y:,.0f}<extra></extra>"))
fig1.add_trace(go.Scatter(x=df["month"], y=df["female"], name="Female", mode="lines", line=dict(color="#f080a7", width=1.8), fill="tozeroy", fillcolor="rgba(240,128,167,0.1)", hovertemplate="<b>Female</b><br>%{x|%b %Y}<br>%{y:,.0f}<extra></extra>"))
fig1.update_layout(**base_layout(300), legend=dict(bgcolor="rgba(11,14,20,0.8)", bordercolor="rgba(255,255,255,0.15)", borderwidth=1, font=dict(color="#cbd5e1")))
st.plotly_chart(fig1, use_container_width=True)

# Chart 2 — Total
st.markdown('<div class="sec-label" style="margin-top:1.5rem">Overview</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-title">Total Births</div>', unsafe_allow_html=True)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df["month"], y=df["total"], name="Total", mode="lines", line=dict(color="#9acd82", width=2), fill="tozeroy", fillcolor="rgba(154,205,130,0.1)", hovertemplate="<b>Total</b><br>%{x|%b %Y}<br>%{y:,.0f}<extra></extra>"))
fig2.update_layout(**base_layout(260))
st.plotly_chart(fig2, use_container_width=True)

# ── Forecast ─────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="sec-label">Forecast</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-title">Predict Future Birth Rate</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([2, 2, 1])
with c1:
    year = st.selectbox("Year", options=list(range(2026, 2036)), index=0)
with c2:
    month_names = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    month_name  = st.selectbox("Month", options=month_names, index=0)
    month_num   = month_names.index(month_name) + 1
with c3:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    run = st.button("Run Forecast")

if run:
    try:
        rf_m  = joblib.load("rf_m.pkl");  xgb_m = joblib.load("xgb_m.pkl"); lr_m = joblib.load("lr_m.pkl")
        rf_f  = joblib.load("rf_f.pkl");  xgb_f = joblib.load("xgb_f.pkl"); lr_f = joblib.load("lr_f.pkl")
        sample = [[34000,33500,33000,35000,32000,31500,31000,32500,month_num,year]]
        male   = 0.4*xgb_m.predict(sample) + 0.3*rf_m.predict(sample) + 0.3*lr_m.predict(sample)
        female = 0.4*xgb_f.predict(sample) + 0.3*rf_f.predict(sample) + 0.3*lr_f.predict(sample)
        total  = male + female
        st.markdown(f"""
        <div class="result-grid">
          <div class="result-cell">
            <div class="result-cell-label male">Male</div>
            <div class="result-cell-value">{int(male[0]):,}</div>
            <div class="result-cell-unit">estimated births</div>
          </div>
          <div class="result-cell">
            <div class="result-cell-label female">Female</div>
            <div class="result-cell-value">{int(female[0]):,}</div>
            <div class="result-cell-unit">estimated births</div>
          </div>
          <div class="result-cell">
            <div class="result-cell-label total">Total</div>
            <div class="result-cell-value">{int(total[0]):,}</div>
            <div class="result-cell-unit">combined births</div>
          </div>
        </div>
        <div class="result-footnote">Ensemble: XGBoost 40% · Random Forest 30% · Linear Regression 30%</div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Model files not found. Ensure .pkl files are in the working directory.")

# ── Documentation ────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="sec-label">Documentation</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-title">About This Project</div>', unsafe_allow_html=True)

# Data Source
st.markdown("""
<div class="doc-card">
  <div class="doc-card-title">Data Source</div>
  <p>ข้อมูลจำนวนการเกิดรายเดือนจำแนกตามเพศทั่วประเทศไทย รวบรวมโดย <strong style="color:#94a3b8">กรมการปกครอง กระทรวงมหาดไทย</strong> ผ่านระบบสถิติทางการทะเบียน</p>
  <p>Source: <a href="https://stat.bora.dopa.go.th/stat/statnew/statMONTH/statmonth/#/displayData" target="_blank">stat.bora.dopa.go.th</a> &nbsp;·&nbsp; ช่วงข้อมูล: <strong style="color:#94a3b8">มกราคม 2545 – กุมภาพันธ์ 2569</strong></p>
</div>
""", unsafe_allow_html=True)

# 🔴 จุดที่แก้ไข HTML: ห่อรูปภาพด้วย Tag <a> และเพิ่มโครงสร้าง Lightbox ด้านล่าง
st.markdown(f"""
<div class="doc-card">
  <div class="doc-card-title">Data Cleaning Process</div>
  <p>ข้อมูลดิบจาก กรมการปกครอง ต้องผ่านการ clean ก่อนนำไปวิเคราะห์ (คลิกที่รูปเพื่อขยาย)</p>
  <ul class="step-list">
    <li><span class="step-num">1</span><span>นำ header หลายแถว (ชื่อรายงาน, ช่วงเวลา) ออก เหลือเฉพาะแถวข้อมูลจริง</span></li>
    <li><span class="step-num">2</span><span>เปลี่ยนชื่อคอลัมน์จากภาษาไทยเป็นภาษาอังกฤษ: <code style="font-family:'DM Mono',monospace;color:#000000;background-color:#ffffff;padding:0.1rem 0.3rem;border-radius:3px;font-size:0.85rem;">month, male, female, total</code></span></li>
    <li><span class="step-num">3</span><span>แปลงชื่อเดือนภาษาไทย เช่น <em>มกราคม 2545</em> ให้เป็น ISO format <code style="font-family:'DM Mono',monospace;color:#000000;background-color:#ffffff;padding:0.1rem 0.3rem;border-radius:3px;font-size:0.85rem;">YYYY-MM</code> โดยแปลง พ.ศ. เป็น ค.ศ. (ลบ 543)</span></li>
    <li><span class="step-num">4</span><span>ลบ comma ในตัวเลข แล้วแปลงเป็น <code style="font-family:'DM Mono',monospace;color:#000000;background-color:#ffffff;padding:0.1rem 0.3rem;border-radius:3px;font-size:0.85rem;">float</code></span></li>
    <li><span class="step-num">5</span><span>ลบแถว "ยอดรวมทั้งหมด" เก็บเฉพาะข้อมูลรายเดือน แล้ว sort ตาม month จากเก่าไปใหม่</span></li>
    <li><span class="step-num">6</span><span>ตรวจสอบ missing values และ outliers ด้วย IQR method ไม่พบค่าผิดปกติอย่างมีนัยสำคัญ</span></li>
  </ul>
  <div class="compare-grid">
    <div class="compare-panel">
      <div class="compare-label before">Before — Raw Data</div>
      <a href="#img-before">
        <img src="data:image/jpeg;base64,{before_b64}" alt="before" />
      </a>
    </div>
    <div class="compare-panel">
      <div class="compare-label after">After — Cleaned</div>
      <a href="#img-after">
        <img src="data:image/png;base64,{after_b64}" alt="after" />
      </a>
    </div>
  </div>
</div>

<a href="#_" class="lightbox" id="img-before">
  <span class="lightbox-close">&times;</span>
  <img src="data:image/jpeg;base64,{before_b64}" alt="before full" />
</a>
<a href="#_" class="lightbox" id="img-after">
  <span class="lightbox-close">&times;</span>
  <img src="data:image/png;base64,{after_b64}" alt="after full" />
</a>
""", unsafe_allow_html=True)

# Features
st.markdown("""
<div class="doc-card">
  <div class="doc-card-title">Dataset Features</div>
  <table class="feat-table">
    <thead><tr><th>Feature</th><th>Type</th><th>Description</th></tr></thead>
    <tbody>
      <tr><td>male_lag1–lag4</td><td><span class="feat-badge badge-lag">Lag</span></td><td>จำนวนเกิดชาย ย้อนหลัง 1–4 เดือน</td></tr>
      <tr><td>female_lag1–lag4</td><td><span class="feat-badge badge-lag">Lag</span></td><td>จำนวนเกิดหญิง ย้อนหลัง 1–4 เดือน</td></tr>
      <tr><td>month</td><td><span class="feat-badge badge-time">Temporal</span></td><td>เลขเดือน (1–12) แทน seasonal cycle</td></tr>
      <tr><td>year</td><td><span class="feat-badge badge-time">Temporal</span></td><td>ปี ค.ศ. แทน long-term trend</td></tr>
      <tr><td>male</td><td><span class="feat-badge badge-target">Target</span></td><td>จำนวนเกิดชายที่ต้องการทำนาย</td></tr>
      <tr><td>female</td><td><span class="feat-badge badge-target">Target</span></td><td>จำนวนเกิดหญิงที่ต้องการทำนาย</td></tr>
    </tbody>
  </table>
</div>
""", unsafe_allow_html=True)

# Algorithms
st.markdown("""
<div class="doc-card">
  <div class="doc-card-title">Model Algorithms & Theory</div>
  <p>ใช้ <strong style="color:#94a3b8">Weighted Ensemble</strong> รวมผลจาก 3 อัลกอริทึม</p>
  <div class="algo-grid">
    <div class="algo-cell">
      <div class="algo-name">XGBoost</div>
      <div class="algo-weight xgb">Weight: 40%</div>
      <div class="algo-desc">Gradient Boosting ที่สร้าง tree ใหม่แต่ละรอบเพื่อแก้ residual error พร้อม L1/L2 regularization</div>
    </div>
    <div class="algo-cell">
      <div class="algo-name">Random Forest</div>
      <div class="algo-weight rf">Weight: 30%</div>
      <div class="algo-desc">Bagging ensemble ของ decision trees หลายต้น แต่ละต้นใช้ bootstrap sample และ random feature subset</div>
    </div>
    <div class="algo-cell">
      <div class="algo-name">Linear Regression</div>
      <div class="algo-weight lr">Weight: 30%</div>
      <div class="algo-desc">Baseline model จับ linear trend ระยะยาว ช่วย stabilize การทำนายในช่วงเวลาที่ห่างจากข้อมูล</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="doc-card">
  <div class="doc-card-title">References & Credits</div>
  <p><strong>Training Data:</strong> ชุดข้อมูลที่ใช้ในการ Train Model นำมาจากระบบสถิติทางการทะเบียน กรมการปกครอง<br>
  🔗 <a href="https://stat.bora.dopa.go.th/stat/statnew/statMONTH/statmonth/#/mainpage" target="_blank">https://stat.bora.dopa.go.th/stat/statnew/statMONTH/statmonth/#/mainpage</a></p>
  <p style="margin-top:0.8rem;"><strong>Libraries & Tools:</strong> <a href="https://streamlit.io/" target="_blank">Streamlit</a> (Web Framework), <a href="https://scikit-learn.org/" target="_blank">Scikit-Learn</a> & <a href="https://xgboost.ai/" target="_blank">XGBoost</a> (Machine Learning), <a href="https://plotly.com/" target="_blank">Plotly</a> (Data Visualization)</p>
  <p style="margin-top:0.8rem;"><strong>Development:</strong> หน้าเว็บแอปพลิเคชันนี้ได้รับการช่วยเหลือในการพัฒนาและออกแบบโค้ดบางส่วนโดย <strong>Claude (Anthropic)</strong></p>
</div>
""", unsafe_allow_html=True)