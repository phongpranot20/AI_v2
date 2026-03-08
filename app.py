import streamlit as st
import google.generativeai as genai
import os

# 1. ตั้งค่าหน้าจอและธีม
st.set_page_config(page_title="KU AI Assistant", page_icon="🌿", layout="wide")

# Custom CSS เพื่อให้หน้าตาเหมือนเวอร์ชัน React
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Header Style */
    .main-header {
        background-color: #006633;
        padding: 2rem;
        border-radius: 0 0 2rem 2rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Chat Bubble Styles */
    .stChatMessage {
        border-radius: 1.5rem !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Sidebar Style */
    [data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #e2e8f0;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        background-color: white;
        color: #1e293b;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        border-color: #006633;
        color: #006633;
        background-color: #f0f7f4;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ตรวจสอบ API Key
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("❌ กรุณาใส่ GEMINI_API_KEY ใน Streamlit Secrets")
    st.stop()

# 3. ตั้งค่า AI (ตัวตนและเครื่องมือค้นหา)
SYSTEM_INSTRUCTION = """คุณคือ AI Chatbot ของมหาวิทยาลัยเกษตรศาสตร์ (KU) 
หน้าที่ของคุณคือตอบคำถามและช่วยเหลือเกี่ยวกับเรื่องต่างๆ ภายในมหาวิทยาลัย เช่น:
- ข้อมูลการรับสมัคร (TCAS), การลงทะเบียนเรียน, สถานที่ต่างๆ, รถตะลัย, กิจกรรมนิสิต
ตอบเป็นภาษาไทยที่สุภาพและเป็นกันเอง (เหมือนพี่ตอบน้อง) 
ใช้ Google Search ค้นหาข้อมูลล่าสุดจากเว็บ ku.ac.th เสมอ และบอกแหล่งที่มาด้วย"""

genai.configure(api_key=api_key)

# 4. Sidebar และปุ่มทางลัด (Quick Actions)
with st.sidebar:
    st.image("https://www.ku.ac.th/assets/images/logo-ku.png", width=100)
    st.title("KU Assistant")
    st.markdown("---")
    st.subheader("คำถามที่พบบ่อย")
    
    # สร้างปุ่มทางลัด
    q1 = st.button("📅 ปฏิทินการศึกษา")
    q2 = st.button("📚 ขั้นตอนลงทะเบียน")
    q3 = st.button("🚌 เส้นทางรถตะลัย")
    q4 = st.button("📍 แผนที่บางเขน")

# 5. หน้าจอหลัก
st.markdown('<div class="main-header"><h1>🌿 KU AI Assistant</h1><p>ศาสตร์แห่งแผ่นดิน เพื่อความกินดีอยู่ดีของชาติ</p></div>', unsafe_allow_html=True)

# เริ่มต้นประวัติการสนทนา
if "messages" not in st.session_state:
    st.session_state.messages = []
    # สร้าง Chat Session พร้อมเครื่องมือค้นหา
    st.session_state.chat = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[{"google_search_retrieval": {}}]
    ).start_chat(history=[])

# แสดงข้อความเก่า
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ฟังก์ชันส่งข้อความ
def send_msg(text):
    st.session_state.messages.append({"role": "user", "content": text})
    with st.chat_message("user"):
        st.markdown(text)
    
    with st.chat_message("assistant"):
        with st.spinner("กำลังค้นหาข้อมูลจาก KU..."):
            response = st.session_state.chat.send_message(text)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

# ตรวจสอบว่ามีการกดปุ่มทางลัดไหม
if q1: send_msg("ขอปฏิทินการศึกษาปีล่าสุดของ KU หน่อย")
elif q2: send_msg("ขั้นตอนการลงทะเบียนเรียนต้องทำยังไงบ้าง")
elif q3: send_msg("ขอข้อมูลเส้นทางเดินรถตะลัยหน่อย")
elif q4: send_msg("ขอแผนที่มหาวิทยาลัยเกษตรศาสตร์ บางเขน")

# ช่องพิมพ์คำถามปกติ
if prompt := st.chat_input("พิมพ์คำถามของคุณที่นี่..."):
    send_msg(prompt)
