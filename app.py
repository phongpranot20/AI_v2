import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="KU AI Assistant", page_icon="🌿")

# ดึง API Key
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ ไม่พบ API Key! กรุณาใส่ใน Secrets")
    st.stop()

# ตั้งค่าโมเดล
try:
    genai.configure(api_key=api_key)
    
    # ลองหาชื่อโมเดลที่ถูกต้องจากระบบ
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # เลือกโมเดล (เรียงลำดับความสำคัญ)
    target_model = ""
    for m in ["models/gemini-1.5-flash-latest", "models/gemini-1.5-flash", "models/gemini-pro"]:
        if m in available_models:
            target_model = m
            break
    
    if not target_model:
        # ถ้าไม่เจอตัวที่ต้องการเลย ให้เอาตัวแรกที่ระบบอนุญาต
        target_model = available_models[0] if available_models else ""

    if not target_model:
        st.error("❌ ไม่พบโมเดลที่ใช้งานได้สำหรับ API Key นี้")
        st.stop()
        
    model = genai.GenerativeModel(target_model)
    st.sidebar.success(f"✅ เชื่อมต่อโมเดล: {target_model}")

except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาดในการเชื่อมต่อ: {str(e)}")
    st.stop()

st.title("🌿 KU AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("ถามคำถามที่นี่..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"❌ ไม่สามารถตอบได้: {str(e)}")
