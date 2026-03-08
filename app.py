import streamlit as st
import google.generativeai as genai
import os

# 1. การตั้งค่าเบื้องต้น
st.set_page_config(page_title="KU AI Assistant", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

# 2. CSS ขั้นสูงเพื่อเลียนแบบ React UI เป๊ะๆ
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* พื้นฐาน */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #f8fafc !important;
    }

    /* ซ่อนส่วนประกอบที่ไม่จำเป็นของ Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid #e2e8f0 !important;
        width: 300px !important;
    }
    
    .sidebar-content {
        padding: 1.5rem;
    }
    
    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 2rem;
    }
    
    .logo-box {
        background-color: #006633;
        padding: 8px;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 12px rgba(0, 102, 51, 0.2);
    }

    .section-title {
        font-size: 0.75rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 1.5rem 0 1rem 0;
    }

    /* Chat Header */
    .chat-header {
        position: fixed;
        top: 0;
        right: 0;
        left: 300px;
        height: 70px;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(12px);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 2rem;
        border-bottom: 1px solid rgba(0, 102, 51, 0.1);
        z-index: 1000;
    }

    /* Chat Bubbles */
    .stChatMessage {
        background-color: transparent !important;
        padding: 1rem 0 !important;
    }
    
    /* Model Bubble (White) */
    [data-testid="stChatMessage"]:nth-child(even) .stChatMessageContent {
        background-color: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 0 24px 24px 24px !important;
        color: #1e293b !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
    }
    
    /* User Bubble (Green Gradient) */
    [data-testid="stChatMessage"]:nth-child(odd) .stChatMessageContent {
        background: linear-gradient(135deg, #006633 0%, #008542 100%) !important;
        border-radius: 24px 0 24px 24px !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(0, 102, 51, 0.2) !important;
    }

    /* Quick Action Cards */
    .action-card {
        background: white;
        border: 1px solid #f1f5f9;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s;
        cursor: pointer;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
    }
    .action-card:hover {
        border-color: #006633;
        box-shadow: 0 10px 15px -3px rgba(0, 102, 51, 0.1);
    }
    
    /* Input Area */
    .stChatInputContainer {
        padding-bottom: 2rem !important;
        background-color: transparent !important;
    }
    .stChatInput {
        border-radius: 30px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    }

    /* Mobile Adjustments */
    @media (max-width: 768px) {
        .chat-header { left: 0; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ส่วนประกอบ Header (HTML)
st.markdown("""
    <div class="chat-header">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-weight: 700; color: #1e293b; font-size: 1.1rem;">KU AI Assistant</span>
            <span style="background: #f0f7f4; color: #006633; font-size: 0.6rem; font-weight: 700; padding: 2px 8px; border-radius: 10px; border: 1px solid rgba(0,102,51,0.1);">BETA</span>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 0.65rem; font-weight: 700; color: #006633; letter-spacing: 0.1em;">KASETSART UNIVERSITY</div>
            <div style="font-size: 0.55rem; color: #94a3b8;">Knowledge of the Land</div>
        </div>
    </div>
    <div style="height: 80px;"></div>
    """, unsafe_allow_html=True)

# 4. Sidebar (เลียนแบบ React Sidebar)
with st.sidebar:
    st.markdown("""
        <div class="sidebar-logo">
            <div class="logo-box">🌿</div>
            <span style="font-weight: 700; font-size: 1.2rem; color: #1e293b;">KU Assistant</span>
        </div>
        <div class="section-title">คำถามที่พบบ่อย</div>
    """, unsafe_allow_html=True)
    
    # ปุ่มคำถามที่พบบ่อย (ใช้ st.button แต่แต่ง CSS ให้เหมือน)
    q1 = st.button("📅  ปฏิทินการศึกษา", key="q1")
    q2 = st.button("📖  การลงทะเบียน", key="q2")
    q3 = st.button("📍  แผนที่วิทยาเขต", key="q3")
    q4 = st.button("💬  รถตะลัย", key="q4")
    
    st.markdown("""
        <div class="section-title">ลิงก์สำคัญ</div>
        <div style="display: flex; flex-direction: column; gap: 12px; padding: 0 8px;">
            <a href="https://www.ku.ac.th" target="_blank" style="text-decoration: none; color: #64748b; font-size: 0.85rem; display: flex; justify-content: space-between;">เว็บไซต์หลัก KU <span>↗</span></a>
            <a href="https://registrar.ku.ac.th" target="_blank" style="text-decoration: none; color: #64748b; font-size: 0.85rem; display: flex; justify-content: space-between;">สำนักทะเบียน <span>↗</span></a>
            <a href="https://ocs.ku.ac.th" target="_blank" style="text-decoration: none; color: #64748b; font-size: 0.85rem; display: flex; justify-content: space-between;">สำนักคอมพิวเตอร์ <span>↗</span></a>
        </div>
        <div style="margin-top: 4rem; padding: 1rem; background: #f8fafc; border-radius: 12px; font-size: 0.65rem; color: #94a3b8;">
            พัฒนาขึ้นเพื่อเป็นตัวช่วยสำหรับนิสิตและบุคลากร มหาวิทยาลัยเกษตรศาสตร์
        </div>
    """, unsafe_allow_html=True)

# 5. การทำงานของ AI
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("กรุณาตั้งค่า GEMINI_API_KEY ใน Secrets")
    st.stop()

genai.configure(api_key=api_key)

SYSTEM_INSTRUCTION = """คุณคือ AI Chatbot ของมหาวิทยาลัยเกษตรศาสตร์ (KU) 
ตอบคำถามด้วยภาษาไทยที่สุภาพและเป็นกันเอง (เหมือนพี่ตอบน้อง) 
ใช้ Google Search ค้นหาข้อมูลล่าสุดจากเว็บ ku.ac.th เสมอ"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "สวัสดีครับ! ผมคือ **KU AI Assistant** ยินดีที่ได้รู้จักครับ 🌿\n\nผมพร้อมช่วยเหลือคุณในทุกเรื่องเกี่ยวกับมหาวิทยาลัยเกษตรศาสตร์ ไม่ว่าจะเป็นเรื่องการเรียน กิจกรรม หรือการใช้ชีวิตในรั้วนนทรี มีอะไรให้ผมช่วยไหมครับ?"}]
    st.session_state.chat = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[{"google_search_retrieval": {}}]
    ).start_chat(history=[])

# แสดงแชท
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ฟังก์ชันส่งข้อความ
def send_msg(text):
    st.session_state.messages.append({"role": "user", "content": text})
    with st.chat_message("user"):
        st.markdown(text)
    
    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(text)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

# 6. Quick Action Cards (แสดงเฉพาะตอนเริ่มแชท)
if len(st.session_state.messages) <= 1:
    cols = st.columns(4)
    with cols[0]:
        if st.button("📅\nปฏิทินการศึกษา", key="btn1"): send_msg("ขอปฏิทินการศึกษาปีล่าสุด")
    with cols[1]:
        if st.button("📖\nการลงทะเบียน", key="btn2"): send_msg("ขั้นตอนการลงทะเบียนเรียน")
    with cols[2]:
        if st.button("📍\nแผนที่วิทยาเขต", key="btn3"): send_msg("ขอแผนที่ ม.เกษตร บางเขน")
    with cols[3]:
        if st.button("💬\nรถตะลัย", key="btn4"): send_msg("ตารางรถตะลัย")

# 7. ช่องรับข้อความ
if prompt := st.chat_input("พิมพ์คำถามของคุณที่นี่..."):
    send_msg(prompt)

# ปุ่ม Sidebar Actions
if q1: send_msg("ขอปฏิทินการศึกษาปีล่าสุด")
if q2: send_msg("ขั้นตอนการลงทะเบียนเรียน")
if q3: send_msg("ขอแผนที่ ม.เกษตร บางเขน")
if q4: send_msg("ตารางรถตะลัย")
