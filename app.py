import streamlit as st
import google.generativeai as genai
import os

# 1. ตั้งค่าหน้าจอ
st.set_page_config(page_title="KU AI Assistant", page_icon="🌿")

# 2. ดึง API Key จาก Streamlit Secrets
# (ต้องไปใส่ใน Settings -> Secrets ของ Streamlit Cloud ด้วยชื่อ GEMINI_API_KEY)
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ ไม่พบ API Key! กรุณาไปที่ Settings > Secrets แล้วใส่ GEMINI_API_KEY = 'คีย์ของคุณ'")
    st.stop()

# 3. ตั้งค่าโมเดล
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="คุณคือ AI Chatbot ของ ม.เกษตรศาสตร์ ตอบเป็นภาษาไทยที่สุภาพและเป็นกันเอง"
)

# 4. ส่วนแสดงผล UI
st.title("🌿 KU AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("ถามคำถามเกี่ยวกับ KU..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
