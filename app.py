import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="KU AI Assistant", page_icon="🌿")

# ดึง API Key
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ ไม่พบ API Key ใน Secrets! กรุณาไปที่ Settings > Secrets")
    st.stop()

# ตั้งค่าโมเดล
try:
    genai.configure(api_key=api_key)
    # ใช้โมเดลเวอร์ชันที่เสถียรที่สุด
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"❌ การตั้งค่า API ผิดพลาด: {str(e)}")
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
            # ลองส่งคำถาม
            response = model.generate_content(prompt)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("⚠️ AI ไม่สามารถตอบคำถามนี้ได้ (อาจติดตัวกรองความปลอดภัย)")
        except Exception as e:
            # แสดง Error แบบละเอียด
            st.error(f"❌ เกิดข้อผิดพลาดจาก Google API: {str(e)}")
            if "API_KEY_INVALID" in str(e):
                st.info("💡 คำแนะนำ: API Key ของคุณอาจจะไม่ถูกต้อง ลองสร้างคีย์ใหม่ที่ aistudio.google.com")
            elif "quota" in str(e).lower():
                st.info("💡 คำแนะนำ: คุณใช้งานเกินโควตาฟรีของ Gemini แล้ว กรุณารอสักครู่แล้วลองใหม่")
