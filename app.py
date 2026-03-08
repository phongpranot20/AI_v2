import streamlit as st
import google.generativeai as genai
import os

# 1. ตั้งค่าหน้าจอ (ซ่อน Sidebar และจัดวางกึ่งกลาง)
st.set_page_config(
    page_title="KU AI Assistant", 
    page_icon="🌿", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# 2. CSS แบบคลีน (เน้นแต่งสีและฟอนต์ ไม่ฝืน Layout)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* ฟอนต์หลัก */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ซ่อน Sidebar และปุ่มเมนู */
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stHeader"] {display: none;}
    .stAppDeployButton {display: none;}
    
    /* ส่วนหัว (Header) */
    .custom-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid #eee;
        margin-bottom: 2rem;
    }
    
    /* ปรับแต่งกล่องแชทให้ดูพรีเมียมขึ้น */
    .stChatMessage {
        border-radius: 20px !important;
        margin-bottom: 1rem !important;
    }
    
    /* ปุ่ม Quick Action ให้ดูเหมือน Card */
    .stButton>button {
        width: 100%;
        height: 100px;
        border-radius: 15px;
        border: 1px solid #f0f2f6;
        background-color: white;
        color: #555;
        font-size: 0.8rem;
        font-weight: 600;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 10px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        border-color: #006633;
        color: #006633;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    /* ปรับสีข้อความในแชท */
    [data-testid="stChatMessageContent"] p {
        font-size: 0.95rem;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. แสดง Header แบบเรียบหรู
st.markdown("""
    <div class="custom-header">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="background: #006633; color: white; padding: 5px 8px; border-radius: 8px; font-weight: bold;">🌿</div>
            <span style="font-weight: 700; font-size: 1.2rem;">KU AI Assistant</span>
            <span style="background: #f0f7f4; color: #006633; font-size: 0.6rem; font-weight: 700; padding: 2px 8px; border-radius: 10px;">BETA</span>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 0.7rem; font-weight: 700; color: #006633;">KASETSART UNIVERSITY</div>
            <div style="font-size: 0.6rem; color: #94a3b8;">Knowledge of the Land</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 4. การทำงานของ AI
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("กรุณาตั้งค่า GEMINI_API_KEY ใน Secrets")
    st.stop()

genai.configure(api_key=api_key)

SYSTEM_INSTRUCTION = "คุณคือ AI Chatbot ของมหาวิทยาลัยเกษตรศาสตร์ ตอบคำถามด้วยภาษาไทยที่สุภาพและเป็นกันเอง ใช้ Google Search ค้นหาข้อมูลล่าสุดจากเว็บ ku.ac.th เสมอ"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "สวัสดีครับ! ผมคือ **KU AI Assistant** ยินดีที่ได้รู้จักครับ 🌿\n\nผมพร้อมช่วยเหลือคุณในทุกเรื่องเกี่ยวกับมหาวิทยาลัยเกษตรศาสตร์ มีอะไรให้ผมช่วยไหมครับ?"}]
    st.session_state.chat = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[{"google_search_retrieval": {}}]
    ).start_chat(history=[])

# แสดงแชท (ฝั่งเดียวกันตามมาตรฐาน Streamlit)
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

# 5. Quick Action Cards (แสดงเฉพาะตอนเริ่มแชท)
if len(st.session_state.messages) <= 1:
    st.write("") # เว้นระยะ
    cols = st.columns(4)
    with cols[0]:
        if st.button("📅\nปฏิทินการศึกษา"): send_msg("ขอปฏิทินการศึกษาปีล่าสุด")
    with cols[1]:
        if st.button("📖\nการลงทะเบียน"): send_msg("ขั้นตอนการลงทะเบียนเรียน")
    with cols[2]:
        if st.button("📍\nแผนที่วิทยาเขต"): send_msg("ขอแผนที่ ม.เกษตร บางเขน")
    with cols[3]:
        if st.button("💬\nรถตะลัย"): send_msg("ตารางรถตะลัย")

# 6. ช่องรับข้อความ
if prompt := st.chat_input("พิมพ์คำถามของคุณที่นี่..."):
    send_msg(prompt)
