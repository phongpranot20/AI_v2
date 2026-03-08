import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="KU AI Assistant", page_icon="🌿")

# --- UI Customization (ทำให้ดูทันสมัยขึ้น) ---
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stChatFloatingInputContainer { background-color: rgba(0,0,0,0); }
    h1 { color: #006633; }
    </style>
    """, unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Missing API Key")
    st.stop()

genai.configure(api_key=api_key)

# --- ส่วนของการตรวจสอบ Model (แก้ Error 404) ---
@st.cache_resource
def get_available_models():
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    return models

available_models = get_available_models()

# เลือก Model ที่ปลอดภัยที่สุด (ถ้ามี 1.5-flash ให้ใช้ ถ้าไม่มีให้เอาตัวแรกที่เจอ)
selected_model = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in available_models else available_models[0]

# --- เริ่มต้น Session ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    try:
        model = genai.GenerativeModel(
            model_name=selected_model,
            system_instruction="คุณคือ AI ของมหาวิทยาลัยเกษตรศาสตร์ ตอบเป็นภาษาไทยสุภาพ"
        )
        # ลองปิด tools ก่อนถ้ายัง Error 404 อยู่
        st.session_state.chat = model.start_chat(history=[])
    except Exception as e:
        st.error(f"Model Setup Error: {e}")

st.title("🌿 KU AI Assistant")
st.info(f"กำลังใช้งานโมเดล: {selected_model}")

# แสดงข้อความ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("สอบถามข้อมูล KU..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")
