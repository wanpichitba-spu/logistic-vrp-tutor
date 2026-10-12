import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ตั้งค่าหน้าตาเว็บแอป
st.set_page_config(page_title="Logistics Chat Tutor & Dashboard", page_icon="📊", layout="centered")

# ชื่อไฟล์ฐานข้อมูลสำหรับบันทึกคำถามนักศึกษา
DATA_FILE = "student_logs.csv"

# ฟังก์ชันสำหรับโหลดและบันทึกข้อมูล
def load_logs():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Timestamp", "Student_Name", "Chapter", "Question"])

def save_log(student_name, chapter, question):
    df = load_logs()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame([[now, student_name, chapter, question]], 
                            columns=["Timestamp", "Student_Name", "Chapter", "Question"])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# ==========================================
# 🛠️ แถบเมนูด้านข้าง (Sidebar)
# ==========================================
st.sidebar.title("📚 ระบบติวเตอร์ & Dashboard")
mode = st.sidebar.radio("เลือกโหมดการใช้งาน:", ["🎓 สำหรับนักศึกษา (ถามคำถาม)", "📊 สำหรับอาจารย์ (Dashboard)"])

# ==========================================
# 🎓 โหมดที่ 1: สำหรับนักศึกษาพิมพ์ถาม + บันทึกข้อมูล
# ==========================================
if mode == "🎓 สำหรับนักศึกษา (ถามคำถาม)":
    st.title("🚛 Logistics Tutor 24 ชม.")
    st.markdown("ยินดีต้อนรับนักศึกษา! กรุณาพิมพ์ชื่อ/รหัสนักศึกษา และพิมพ์คำถามที่สงสัยลงในช่องด้านล่างได้เลยครับ")
    
    # ช่องกรอกชื่อ/รหัสนักศึกษา (เพื่อ Record ว่าใครถาม)
    student_name = st.text_input("👤 ชื่อ-นามสกุล หรือ รหัสนักศึกษา :", placeholder="เช่น นายสมชาย ใจดี (65012345)")
    
    chapter = st.selectbox("📖 เลือกบทเรียนที่ต้องการถาม :", 
                           ["บทที่ 9-10: การจัดเส้นทาง (VRP)", "บทที่ 6: แบบจำลองการขนส่ง (Transport Model)"])
    
    user_query = st.text_input("💬 พิมพ์คำถามที่ต้องการให้ AI ช่วยตอบ :", placeholder="เช่น VRP คืออะไร? / S15 คิดยังไง? / ขอวิธีทำ Least Cost")

    if st.button("🚀 ส่งคำถาม"):
        if not student_name:
            st.warning("⚠️ กรุณากรอกชื่อหรือรหัสนักศึกษาก่อนส่งคำถามนะครับ")
        elif not user_query:
            st.warning("⚠️ กรุณาพิมพ์คำถามด้วยนะครับ")
        else:
            # บันทึกข้อมูลเข้าระบบ (Record คนถาม, บทเรียน, คำถาม, เวลา)
            save_log(student_name, chapter, user_query)
            st.success("✅ บันทึกคำถามเรียบร้อยแล้ว!")
            
            # ส่วนการตอบของ AI ตามบทเรียน
            st.write("---")
            st.markdown("### 🤖 คำตอบจาก AI Tutor:")
            q = user_query.lower()
            
            if chapter == "บทที่ 9-10: การจัดเส้นทาง (VRP)":
                if "vrp" in q or "คืออะไร" in q:
                    st.markdown("**VRP** คือ ปัญหาการจัดเส้นทางเดินรถเพื่อส่งสินค้าให้ลูกค้าครบทุกจุดโดยใช้ระยะทางรวมน้อยที่สุด ภายใต้พิกัดความจุรถ (โจทย์ข้อนี้คือไม่เกิน **150 ลัง** ครับ)")
                elif "s15" in q:
                    st.markdown("สูตร $S_{15} = d_{01} + d_{05} - d_{15}$ ➡️ แทนค่า $37 + 59 - 16 = $ **80** ครับผม!")
                else:
                    st.markdown(f"ขอบคุณสำหรับคำถาม **{user_query}** พี่ AI จะเก็บข้อมูลไว้ให้นักศึกษานะครับ (คำตอบเฉลย VRP: ใช้รถ 3 คัน)")
            
            elif chapter == "บทที่ 6: แบบจำลองการขนส่ง (Transport Model)":
                if "northwest" in q:
                    st.markdown("**วิธี Northwest Corner Rule** 🧭 จัดของจากช่องบนซ้ายสุดก่อนเสมอ 📊 ต้นทุนรวม = **4,200 บาท**")
                elif "least cost" in q:
                    st.markdown("**วิธี Least Cost Method** 💰 เลือกจัดของลงช่องที่ค่าขนส่งถูกที่สุดก่อน 📊 ต้นทุนรวม = **4,100 บาท**")
                else:
                    st.markdown(f"ขอบคุณสำหรับคำถาม **{user_query}** พี่ AI ได้บันทึกข้อสงสัยเรียบร้อยแล้วครับ")

# ==========================================
# 📊 โหมดที่ 2: สำหรับอาจารย์ (Dashboard วิเคราะห์ข้อมูล)
# ==========================================
elif mode == "📊 สำหรับอาจารย์ (Dashboard)":
    st.title("📊 Dashboard สรุปการเข้าใช้งานของนักศึกษา")
    
    # ระบบล็อกรหัสผ่านเข้า Dashboard สำหรับอาจารย์ (ตั้งรหัสได้ตามต้องการ)
    password = st.text_input("🔒 กรุณากรอกรหัสผ่านสำหรับอาจารย์ :", type="password")
    
    if password == "1234":  # <--- อาจารย์สามารถเปลี่ยนรหัสผ่านตรงนี้ได้ครับ
        st.success("🔓 เข้าสู่ระบบสำเร็จ")
        
        df_logs = load_logs()
        
        if df_logs.empty:
            st.info("ยังไม่มีข้อมูลการพิมพ์ถามของนักศึกษาในขณะนี้")
        else:
            # 1. ตัวเลขสรุปภาพรวม (Metrics)
            col1, col2, col3 = st.columns(3)
            col1.metric("จำนวนคำถามทั้งหมด", f"{len(df_logs)} ครั้ง")
            col2.metric("จำนวนนักศึกษาที่เข้ามาถาม", f"{df_logs['Student_Name'].nunique()} คน")
            col3.metric("บทเรียนที่ถามมากที่สุด", df_logs['Chapter'].mode()[0] if not df_logs.empty else "-")
            
            st.write("---")
            
            # 2. กราฟวิเคราะห์
            st.subheader("📈 จำนวนคำถามแบ่งตามบทเรียน")
            chapter_counts = df_logs['Chapter'].value_counts()
            st.bar_chart(chapter_counts)
            
            st.write("---")
            
            # 3. ตารางตารางแสดงรายชื่อและคำถามทั้งหมด (History Log)
            st.subheader("📋 ประวัติการถามคำถามของนักศึกษาทั้งหมด")
            st.dataframe(df_logs.sort_values(by="Timestamp", ascending=False), use_container_width=True)
            
            # ปุ่มดาวน์โหลดไฟล์รายงานเป็น Excel/CSV
            csv_data = df_logs.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 ดาวน์โหลดรายงาน (CSV File)",
                data=csv_data,
                file_name="student_questions_report.csv",
                mime="text/csv"
            )
    elif password:
        st.error("❌ รหัสผ่านไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง")
