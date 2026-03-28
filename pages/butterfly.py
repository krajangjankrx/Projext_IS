import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
import os
import base64

st.set_page_config(
    page_title="Butterfly Classifier",
    layout="wide",
    initial_sidebar_state="expanded",
)

def img_to_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=DM+Mono&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    
    /* ปรับพื้นหลังหลักให้กลืนกับ App เดิมเล็กน้อย */
    .stApp { background: #050608 !important; color: white; }

    /* ── Sidebar (สไตล์เดียวกับหน้า Home) ── */
    [data-testid="stSidebar"] {
        background: #07090f !important;
        border-right: none !important;
    }

    /* ซ่อน navigation ด้านบน */
    [data-testid="stSidebarNav"] {
        display: none;
    }

    /* ปุ่มเปิดปิด sidebar */
    [data-testid="stSidebarCollapseButton"], 
    [data-testid="collapsedControl"] {
        color: white !important;
    }

    /* บังคับทั้งสีพื้นและสีเส้นให้เป็นสีขาว */
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
                
    /* ปุ่มเมนู */
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
        font-size: 1.25rem !important;
        font-weight: 700 !important;
    }

    div[data-testid="stPageLink"] a:hover {
        background: #334155 !important;
    }

    #MainMenu, footer, header { visibility: hidden; }

    /* ── Accent ── */
    :root { --acc: #6ee7b7; --acc-dim: rgba(110,231,183,0.7); --acc-faint: rgba(110,231,183,0.09); }

    /* ── Hero ── */
    .hero { padding: 4.5rem 0 3rem; max-width: 680px; }
    .hero-title {
        font-family: 'DM Serif Display', serif;
        font-size: 3.6rem; font-weight: 400;
        color: white; line-height: 1.08;
        letter-spacing: -0.02em; margin: 0 0 1.1rem;
    }
    .hero-title em { font-style: italic; color: #cbd5e1; }
    .hero-body {
        font-size: 1.05rem; color: #94a3b8;
        line-height: 1.8; font-weight: 300;
    }

    /* ── Dividers & Labels ── */
    .divider { border: none; border-top: 1px solid rgba(255,255,255,0.07); margin: 2.8rem 0; }
    .sec-label {
        font-size: 0.72rem; font-weight: 700;
        letter-spacing: 0.22em; text-transform: uppercase;
        color: #94a3b8; margin-bottom: 1.2rem;
    }

    /* ── Gallery ── */
    .gallery-grid {
        display: grid; grid-template-columns: repeat(5,1fr);
        gap: 1px; background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 10px; overflow: hidden;
    }
    .gallery-cell { background: #11131c; overflow: hidden; }
    .gallery-cell img { width: 100%; display: block; aspect-ratio: 1; object-fit: cover; opacity: 0.88; transition: opacity 0.2s; }
    .gallery-cell img:hover { opacity: 1; }

    /* caption override */
    [data-testid="stImage"] p,
    .stCaption, [data-testid="stCaptionContainer"] p {
        font-size: 0.78rem !important;
        color: #94a3b8 !important;
        text-align: center !important;
        margin-top: 0.3rem !important;
    }

    /* ── Upload ── */
    [data-testid="stFileUploader"] {
        background: #11131c !important;
        border: 1px dashed rgba(110,231,183,0.25) !important;
        border-radius: 10px !important;
    }
    [data-testid="stFileUploader"] label { color: #94a3b8 !important; font-size: 0.95rem !important; }
    [data-testid="stFileUploader"] * { color: #94a3b8 !important; }
    [data-testid="stFileUploader"] button { color: var(--acc-dim) !important; border-color: rgba(110,231,183,0.25) !important; }

    /* Section label above upload */
    .upload-label {
        font-size: 0.72rem; font-weight: 700;
        letter-spacing: 0.22em; text-transform: uppercase;
        color: #94a3b8; margin-bottom: 0.8rem;
    }

    /* ── Result panel ── */
    .result-panel {
        background: #11131c;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px; padding: 2.2rem 2rem;
    }
    .result-tag {
        font-size: 0.72rem; font-weight: 700;
        letter-spacing: 0.2em; text-transform: uppercase;
        color: var(--acc-dim); margin-bottom: 0.5rem;
    }
    .result-name {
        font-family: 'DM Serif Display', serif;
        font-size: 2.5rem; color: white; line-height: 1.15; margin-bottom: 1.6rem;
    }

    .conf-wrap { margin-bottom: 1.8rem; }
    .conf-header {
        display: flex; justify-content: space-between;
        font-size: 0.85rem; color: #94a3b8; margin-bottom: 0.5rem;
    }
    .conf-header span:last-child { color: white; font-weight: 600; font-family: 'DM Mono', monospace; }
    .conf-track { height: 7px; background: rgba(110,231,183,0.1); border-radius: 99px; overflow: hidden; }
    .conf-fill  { height: 100%; border-radius: 99px; background: linear-gradient(90deg, rgba(110,231,183,0.4), rgba(110,231,183,0.85)); }

    .top3-head {
        font-size: 0.72rem; font-weight: 700;
        letter-spacing: 0.2em; text-transform: uppercase;
        color: #cbd5e1; margin-bottom: 0.7rem;
    }
    .top3-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 0.6rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);
        font-size: 0.95rem;
    }
    .top3-row:last-child { border-bottom: none; }
    .top3-row .name { color: #94a3b8; }
    .top3-row .pct  { color: #94a3b8; font-family: 'DM Mono', monospace; font-size: 0.88rem; }
    .top3-row.first .name { color: white; font-weight: 600; }
    .top3-row.first .pct  { color: var(--acc-dim); font-size: 0.95rem; font-weight: 600; }

    /* ── Documentation Styles ── */
    .doc-card { background: #11131c; border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 1.8rem 1.8rem; margin-bottom: 1rem; }
    .doc-card-title { font-family: 'DM Serif Display', serif; font-size: 1.25rem; color: #ffffff; margin-bottom: 0.8rem; font-weight: 400; }
    .doc-card p { color: #cbd5e1; font-size: 1rem; line-height: 1.75; margin: 0 0 0.5rem; }
    .doc-card a { color: var(--acc); text-decoration: none; word-break: break-all; font-weight: 500; }
    .doc-card a:hover { color: #ffffff; }

    .step-list { margin: 0.5rem 0 0; padding: 0; list-style: none; }
    .step-list li { display: flex; gap: 0.75rem; align-items: flex-start; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 1rem; color: #cbd5e1; line-height: 1.6; }
    .step-list li:last-child { border-bottom: none; }
    .step-num { flex-shrink: 0; width: 24px; height: 24px; background: rgba(110,231,183,0.15); border-radius: 4px; color: var(--acc); font-size: 0.8rem; font-weight: 700; display: flex; align-items: center; justify-content: center; margin-top: 0.15rem; font-family: 'DM Mono', monospace; }

    .compare-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; overflow: hidden; margin-top: 1.2rem; }
    .compare-label { padding: 0.4rem 0.8rem; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; }
    .compare-label.before { background: rgba(240,100,80,0.15); color: rgba(240,100,80,0.9); border-bottom: 1px solid rgba(240,100,80,0.2); }
    .compare-label.after  { background: rgba(110,231,183,0.15); color: rgba(110,231,183,0.9); border-bottom: 1px solid rgba(110,231,183,0.2); }
    
    .compare-panel { background: #11131c; }
    .compare-panel img { 
        width: 100%; 
        height: 220px; 
        object-fit: contain; 
        display: block; 
        background: #050608; 
        padding: 0.5rem;
        cursor: zoom-in;
        transition: opacity 0.2s ease;
    }
    .compare-panel img:hover {
        opacity: 0.7;
    }

    /* Lightbox ซูมรูป */
    .lightbox {
        display: none;
        position: fixed;
        z-index: 99999;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        background-color: rgba(5, 6, 8, 0.95);
        backdrop-filter: blur(5px);
        align-items: center;
        justify-content: center;
    }
    .lightbox:target {
        display: flex;
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

    .algo-grid { display: grid; grid-template-columns: 1fr; gap: 1px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; overflow: hidden; margin-top: 0.8rem; }
    .algo-cell { background: #11131c; padding: 1.4rem 1.2rem; }
    .algo-name   { font-family: 'DM Serif Display', serif; font-size: 1.15rem; color: #ffffff; margin-bottom: 0.25rem; }
    .algo-desc   { font-size: 1rem; color: #cbd5e1; line-height: 1.65; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.page_link("app.py", label="Home")
    st.page_link("pages/butterfly.py", label="Butterfly Classifier")
    st.page_link("pages/birth_rate.py", label="Birth Rate Forecast")

# ── Model ────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    return tf.keras.models.load_model(os.path.join(BASE_DIR, "..", "butterfly_model.keras"))

try:
    model = load_model()
except Exception as e:
    st.warning(f"Model loading error: {e}")
    model = None

CLASS_NAMES = [
    'Cabbage White', 'Common Buckeye', 'Giant Swallowtail',
    'Monarch', 'Mourning Cloak', 'Painted Lady',
    'Postman', 'Red Admiral', 'Small Copper', 'Zebra'
]

# ── Hero ─────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">Butterfly<br><em>Species Classifier</em></div>
  <div class="hero-body">
    อัปโหลดรูปภาพผีเสื้อเพื่อให้ AI วิเคราะห์และจำแนกสายพันธุ์
    จากทั้งหมด 10 ชนิดด้วยโมเดล Convolutional Neural Network
  </div>
</div>
""", unsafe_allow_html=True)

# ── Gallery ──────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="sec-label">Reference — 10 Species</div>', unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

cols = st.columns(5)
for i, name in enumerate(CLASS_NAMES):
    img_path = os.path.join(BASE_DIR, "..", "examples", f"{name}.jpg")
    with cols[i % 5]:
        try:
            img = Image.open(img_path)
            st.image(img, use_container_width=True, caption=name)
        except FileNotFoundError:
            st.markdown(
                f'<div style="aspect-ratio:1;background:#11131c;display:flex;align-items:center;'
                f'justify-content:center;font-size:0.82rem;color:#94a3b8;text-align:center;padding:0.5rem; border-radius:10px;">{name}</div>',
                unsafe_allow_html=True
            )
            st.caption(name)

# ── Classify ─────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="sec-label">Classify</div>', unsafe_allow_html=True)

uploaded = st.file_uploader(
    "Upload an image (.jpg / .jpeg / .png)",
    type=["jpg", "jpeg", "png"],
    label_visibility="visible",
)

if uploaded and model is not None:
    c1, c2 = st.columns([1, 1], gap="large")

    with c1:
        st.markdown('<div class="upload-label">Uploaded Image</div>', unsafe_allow_html=True)
        image = Image.open(uploaded).convert("RGB")
        st.image(image, use_container_width=True)

    with c2:
        # ให้ AI ประมวลผลให้เสร็จก่อน
        with st.spinner("Analysing..."):
            arr   = tf.keras.preprocessing.image.img_to_array(image.resize((224, 224)))
            arr   = np.expand_dims(arr, 0)
            preds = model.predict(arr)[0]

        top_i = int(np.argmax(preds))
        conf  = float(preds[top_i]) * 100
        top3  = np.argsort(preds)[::-1][:3]

        rows_html = "".join(
            f'<div class="top3-row {"first" if r == 0 else ""}">'
            f'<span class="name">{CLASS_NAMES[idx]}</span>'
            f'<span class="pct">{preds[idx]*100:.1f}%</span></div>'
            for r, idx in enumerate(top3)
        )

        st.markdown(f"""
        <div class="result-panel">
            <div class="result-tag">Predicted Species</div>
            <div class="result-name">{CLASS_NAMES[top_i]}</div>
            <div class="conf-wrap">
              <div class="conf-header">
                <span>Confidence</span>
                <span>{conf:.1f}%</span>
              </div>
              <div class="conf-track">
                <div class="conf-fill" style="width:{conf:.1f}%"></div>
              </div>
            </div>
            <div class="top3-head">Top 3 Candidates</div>
            {rows_html}
        </div>
        """, unsafe_allow_html=True)

# ── Documentation ────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="sec-label">Documentation</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-title">About This Project</div>', unsafe_allow_html=True)

# แปลงรูปเป็น base64 โดยอ้างอิงจากไฟล์ใหม่ที่คุณอัปโหลด
before_bf_b64 = img_to_b64(os.path.join(BASE_DIR, "before_clean_butterfly.png"))
after_bf_b64  = img_to_b64(os.path.join(BASE_DIR, "after_clean_butterfly.png"))

# Data Source & Preparation (พร้อมระบบคลิกซูมภาพแบบ Lightbox)
st.markdown(f"""
<div class="doc-card">
  <div class="doc-card-title">Data Source & Preparation</div>
  <p>ข้อมูลชุดนี้ได้มาจาก Kaggle โดยเป็นรูปภาพผีเสื้อ 10 สายพันธุ์ อย่างไรก็ตาม ข้อมูลดิบที่ได้มามีการเก็บรูปภาพทั้งหมดรวมกันอยู่ในโฟลเดอร์เดียว ทำให้ไม่สะดวกต่อการนำไปฝึกสอนโมเดลด้วย Keras (คลิกที่รูปเพื่อขยาย)</p>
  <p>จึงได้ทำการ <strong>Data Cleaning</strong> โดยการเขียนโค้ดเพื่อดึงภาพแยกประเภท และสร้างโฟลเดอร์ย่อยตามชื่อสายพันธุ์ทั้ง 10 ชนิด เพื่อให้สอดคล้องกับโครงสร้างการอ่านข้อมูลของ <code>image_dataset_from_directory</code></p>
  <div class="compare-grid">
    <div class="compare-panel">
      <div class="compare-label before">Before — Raw Images in One Folder</div>
      <a href="#img-bf-before">
        <img src="data:image/png;base64,{before_bf_b64}" alt="before" />
      </a>
    </div>
    <div class="compare-panel">
      <div class="compare-label after">After — Categorized into Folders</div>
      <a href="#img-bf-after">
        <img src="data:image/png;base64,{after_bf_b64}" alt="after" />
      </a>
    </div>
  </div>
</div>

<a href="#_" class="lightbox" id="img-bf-before">
  <span class="lightbox-close">&times;</span>
  <img src="data:image/png;base64,{before_bf_b64}" alt="before full" />
</a>
<a href="#_" class="lightbox" id="img-bf-after">
  <span class="lightbox-close">&times;</span>
  <img src="data:image/png;base64,{after_bf_b64}" alt="after full" />
</a>
""", unsafe_allow_html=True)

# Algorithms & Theory
st.markdown("""
<div class="doc-card">
  <div class="doc-card-title">Model Algorithms & Theory</div>
  <div class="algo-grid">
    <div class="algo-cell">
      <div class="algo-name">Convolutional Neural Network (CNN)</div>
      <div class="algo-desc">
        ใช้สถาปัตยกรรม Deep Learning ที่ชื่อว่า CNN ซึ่งมีประสิทธิภาพสูงในการวิเคราะห์และจำแนกข้อมูลภาพ โดยอาศัย <strong>Convolutional Layer</strong> ในการสกัดลักษณะเด่น (Features) ของผีเสื้อ เช่น ลวดลายของปีก สี และรูปทรง ทำงานร่วมกับ <strong>MaxPooling Layer</strong> เพื่อลดขนาดของข้อมูลและดึงเฉพาะข้อมูลที่สำคัญ ก่อนจะแปลงข้อมูลเป็นเส้นตรง (Flatten) แล้วส่งต่อไปยัง <strong>Dense Layer</strong> เพื่อคำนวณความน่าจะเป็นและจำแนกสายพันธุ์
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Model Development Process
st.markdown("""
<div class="doc-card">
  <div class="doc-card-title">Model Development Steps</div>
  <ul class="step-list">
    <li><span class="step-num">1</span><span><strong>Load & Preprocess:</strong> โหลดข้อมูลภาพทั้งหมดและปรับขนาด (Resize) รูปภาพให้เท่ากันที่ 224x224 พิกเซล และทำการ Scaling ค่าสีให้อยู่ในช่วง 0-1</span></li>
    <li><span class="step-num">2</span><span><strong>Data Augmentation:</strong> เพิ่มความหลากหลายให้ข้อมูลภาพ เช่น การพลิกภาพ การหมุน หรือซูม เพื่อลดโอกาสการเกิด Overfitting</span></li>
    <li><span class="step-num">3</span><span><strong>Build Architecture:</strong> สร้างโครงสร้างโมเดล CNN ตามลำดับชั้น (Sequential) ประกอบด้วย Conv2D, MaxPooling2D, Flatten และจบด้วย Dense Layer ที่มี 10 โหนด (ตามจำนวนสายพันธุ์)</span></li>
    <li><span class="step-num">4</span><span><strong>Compile & Train:</strong> กำหนด Loss function เป็น <code>categorical_crossentropy</code> สำหรับคลาสหลายกลุ่ม และให้โมเดลเริ่มฝึกสอนเรียนรู้ (Training) จากชุดข้อมูลภาพ</span></li>
    <li><span class="step-num">5</span><span><strong>Export:</strong> บันทึกโมเดลเป็นไฟล์ <code>.keras</code> เพื่อนำมาโหลดใช้งานทำนายผลลัพธ์ในเว็บแอปพลิเคชัน (Streamlit) นี้</span></li>
  </ul>
</div>
""", unsafe_allow_html=True)

# References
st.markdown("""
<div class="doc-card">
  <div class="doc-card-title">References & Credits</div>
  <p><strong>Training Data:</strong> ชุดข้อมูลภาพผีเสื้อ 10 สายพันธุ์ นำมาจาก Kaggle<br>
  🔗 <a href="https://www.kaggle.com/datasets/veeralakrishna/butterfly-dataset" target="_blank">https://www.kaggle.com/datasets/veeralakrishna/butterfly-dataset</a></p>
  <p style="margin-top:0.8rem;"><strong>Libraries & Tools:</strong> <a href="https://streamlit.io/" target="_blank">Streamlit</a> (Web Framework), <a href="https://www.tensorflow.org/" target="_blank">TensorFlow / Keras</a> (Deep Learning), <a href="https://pillow.readthedocs.io/" target="_blank">Pillow</a> (Image Processing)</p>
  <p style="margin-top:0.8rem;"><strong>Development:</strong> หน้าเว็บแอปพลิเคชันนี้ได้รับการช่วยเหลือในการพัฒนาและออกแบบโค้ดบางส่วนโดย <strong>Claude (Anthropic)</strong> และ <strong>Gemini (Google)</strong></p>
</div>
""", unsafe_allow_html=True)