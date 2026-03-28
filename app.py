import streamlit as st

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. CSS: ปรับดีไซน์
st.markdown("""
<style>

/* พื้นหลังหลัก */
.stApp {
    background: #050608 !important;
    color: white;
}

/* sidebar background */
[data-testid="stSidebar"] {
    background: #07090f !important;
}

/* ซ่อน navigation ด้านบน */
[data-testid="stSidebarNav"] {
    display: none;
}

/* ปุ่มเปิดปิด sidebar */
[data-testid="collapsedControl"], 
[data-testid="stSidebarCollapseButton"], 
button[kind="header"], 
button[title="Collapse sidebar"], 
button[title="Expand sidebar"] {
    color: white !important;
    opacity: 1 !important;
}

[data-testid="collapsedControl"] svg, 
[data-testid="stSidebarCollapseButton"] svg, 
button[kind="header"] svg, 
button[title="Collapse sidebar"] svg, 
button[title="Expand sidebar"] svg {
    fill: white !important;
    color: white !important;
}

[data-testid="collapsedControl"] svg path, 
[data-testid="stSidebarCollapseButton"] svg path, 
button[kind="header"] svg path, 
button[title="Collapse sidebar"] svg path, 
button[title="Expand sidebar"] svg path {
    fill: white !important;
}

/* hover ให้สว่างขึ้นหรือเปลี่ยนสีเล็กน้อยเมื่อเอาเมาส์ชี้ */
button[kind="header"]:hover svg,
button[title="Collapse sidebar"]:hover svg, 
button[title="Expand sidebar"]:hover svg {
    filter: brightness(1.6);
    fill: #cbd5e1 !important;
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

/* ซ่อนเมนู */
#MainMenu, footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)

# 3. Sidebar (ต้องใช้ with st.sidebar)
with st.sidebar:
    st.page_link("app.py", label="Home")
    st.page_link("pages/butterfly.py", label="Butterfly Classifier")
    st.page_link("pages/birth_rate.py", label="Birth Rate Forecast")

# 4. Hero Section
st.markdown("""
<div style="padding: 6rem 0 4rem; max-width: 850px;">
  <h1 style="font-family:'DM Serif Display'; font-size:5rem; color:white; line-height:1.05; margin-bottom:1.5rem;">
    Intelligence System<br> <em>Projects</em>
  </h1>
  <p style="font-size:1.3rem; color:#cbd5e1; line-height:1.8; font-weight:300;">
    รวบรวมผลงานด้านการพัฒนาโมเดลปัญญาประดิษฐ์และการวิเคราะห์ข้อมูลเชิงลึก 
    เพื่อสร้างโซลูชันที่มีประสิทธิภาพด้วย Python และ Deep Learning
  </p>
</div>
""", unsafe_allow_html=True)

# 5. Project Cards & Navigation
st.markdown('<div style="color:#6366f1; font-weight:700; letter-spacing:0.3em; text-transform:uppercase; margin-bottom:2rem;">Selected Projects</div>', unsafe_allow_html=True)

col_card1, col_card2 = st.columns(2)
with col_card1:
    st.markdown("""
    <div style="background:#11131c; padding:3.5rem 2.5rem; border-radius:20px; border:1px solid rgba(255,255,255,0.1); height:100%;">
        <h2 style="font-family:'DM Serif Display'; font-size:2.5rem; color:white; margin-bottom:1.2rem;">Butterfly Species Classifier</h2>
        <p style="color:#94a3b8; font-size:1.15rem;">ระบบจำแนกสายพันธุ์ผีเสื้ออัตโนมัติจากภาพถ่าย ด้วยการใช้ CNN ประสิทธิภาพสูง</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/butterfly.py", label="เปิดระบบจำแนกผีเสื้อ →")

with col_card2:
    st.markdown("""
    <div style="background:#11131c; padding:3.5rem 2.5rem; border-radius:20px; border:1px solid rgba(255,255,255,0.1); height:100%;">
        <h2 style="font-family:'DM Serif Display'; font-size:2.5rem; color:white; margin-bottom:1.2rem;">Birth Rate Forecasting</h2>
        <p style="color:#94a3b8; font-size:1.15rem;">วิเคราะห์แนวโน้มและพยากรณ์จำนวนการเกิดของประชากรไทยในอนาคต โดยใช้ Ensemble Learning</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/birth_rate.py", label="เปิดระบบพยากรณ์อัตราเกิด →")

# 6. Footer (ผู้จัดทำ)
st.markdown('<div style="border-top: 1px solid rgba(255,255,255,0.1); margin: 4rem 0 2rem;"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #cbd5e1; font-size: 1.05rem; padding: 1rem 0 3rem; font-family: 'DM Sans', sans-serif;">
    <span style="color: #6366f1; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; font-size: 0.8rem; display: block; margin-bottom: 0.5rem;">Created By</span>
    <span style="color: white; font-weight: 500;">Krajangjan Pongkittiwiboon</span> <span style="color: #64748b; margin: 0 0.5rem;">|</span> <span style="font-family: 'DM Mono', monospace; color: #94a3b8;">6704062617261</span>
</div>
""", unsafe_allow_html=True)