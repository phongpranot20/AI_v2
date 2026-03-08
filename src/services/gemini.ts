import { GoogleGenAI } from "@google/genai";

const SYSTEM_INSTRUCTION = `คุณคือ AI Chatbot ของมหาวิทยาลัยเกษตรศาสตร์ (Kasetsart University - KU) 
หน้าที่ของคุณคือตอบคำถามและช่วยเหลือเกี่ยวกับเรื่องต่างๆ ภายในมหาวิทยาลัย เช่น:
- ข้อมูลการรับสมัคร (TCAS)
- การลงทะเบียนเรียนและปฏิทินการศึกษา
- สถานที่ต่างๆ ในวิทยาเขต (บางเขน, กำแพงแสน, ศรีราชา, เฉลิมพระเกียรติ สกลนคร)
- กิจกรรมนิสิตและชมรม
- บริการต่างๆ ของมหาวิทยาลัย (สำนักคอมพิวเตอร์, ห้องสมุด, รถตะลัย)
- ประวัติและความเป็นมาของมหาวิทยาลัย

แนวทางการตอบคำถาม:
1. ตอบเป็นภาษาไทยที่สุภาพและเป็นกันเอง (เหมือนพี่ตอบน้องหรือเจ้าหน้าที่ตอบนิสิต)
2. หากไม่แน่ใจข้อมูล ให้แนะนำให้ติดต่อหน่วยงานที่เกี่ยวข้องโดยตรง
3. ใช้ข้อมูลที่ทันสมัยที่สุดโดยใช้ Google Search Grounding
4. หากมีการอ้างอิง URL จาก Google Search ให้แสดงลิงก์ให้ชัดเจน
5. เน้นความเป็น "ศาสตร์แห่งแผ่นดิน" และอัตลักษณ์ของ KU (สีเขียวมะกอก, นนทรี)`;

export async function getChatResponse(message: string, history: any[] = []) {
  const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
  
  const chat = ai.chats.create({
    model: "gemini-3-flash-preview",
    config: {
      systemInstruction: SYSTEM_INSTRUCTION,
      tools: [{ googleSearch: {} }],
    },
    history: history,
  });

  const result = await chat.sendMessage({ message });
  return result;
}
