import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Integrated CD Planner", layout="wide")

# --- ส่วนของการเก็บข้อมูล (Session State) ---
if 'ip_data' not in st.session_state:
    st.session_state.ip_data = pd.DataFrame(columns=['ประเด็น', 'Importance', 'Performance'])
if 'opps' not in st.session_state:
    st.session_state.opps = ""
if 'threats' not in st.session_state:
    st.session_state.threats = ""
if 'so_strat' not in st.session_state:
    st.session_state.so_strat = ""
if 'wo_strat' not in st.session_state:
    st.session_state.wo_strat = ""
if 'st_strat' not in st.session_state:
    st.session_state.st_strat = ""
if 'wt_strat' not in st.session_state:
    st.session_state.wt_strat = ""

# --- Sidebar: Navigation ---
st.sidebar.title("ระบบแผนพัฒนาชุมชน")
step = st.sidebar.radio("เลือกขั้นตอนการทำงาน", [
    "Step 1: IP Matrix (ปัจจัยภายใน)",
    "Step 2: Policy Alignment",
    "Step 3: SWOT Analysis",
    "Step 4: TOWS Matrix & Strategy",
    "Step 7: สรุปและ Export PDF"
])

# --- STEP 1: IP MATRIX ---
if step == "Step 1: IP Matrix (ปัจจัยภายใน)":
    st.header("📍 ขั้นตอนที่ 1: วิเคราะห์งานพัฒนาชุมชน (IP Matrix)")
    with st.form("ip_form"):
        col1, col2, col3 = st.columns([3, 1, 1])
        topic = col1.text_input("ประเด็นการพัฒนา")
        imp = col2.slider("Importance (ความสำคัญ)", 1, 5, 3)
        perf = col3.slider("Performance (ผลงานที่ทำได้)", 1, 5, 3)
        submit = st.form_submit_button("เพิ่มข้อมูล")
        if submit and topic:
            new_data = pd.DataFrame({'ประเด็น': [topic], 'Importance': [imp], 'Performance': [perf]})
            st.session_state.ip_data = pd.concat([st.session_state.ip_data, new_data], ignore_index=True)

    if not st.session_state.ip_data.empty:
        fig = px.scatter(st.session_state.ip_data, x="Performance", y="Importance", text="ประเด็น",
                         range_x=[0, 6], range_y=[0, 6])
        fig.add_hline(y=3.0, line_dash="dash", line_color="red")
        fig.add_vline(x=3.0, line_dash="dash", line_color="red")
        fig.update_traces(marker=dict(size=15, color='#1f77b4'), textposition='top center')
        st.plotly_chart(fig, use_container_width=True)

# --- STEP 2: POLICY ALIGNMENT ---
elif step == "Step 2: Policy Alignment":
    st.header("🔗 ขั้นตอนที่ 2: ความเชื่อมโยงกับแผนระดับต่างๆ")
    if not st.session_state.ip_data.empty:
        for index, row in st.session_state.ip_data.iterrows():
            with st.expander(f"ประเด็น: {row['ประเด็น']}"):
                st.write(f"✅ ระดับอำเภอ: สอดคล้องกับแผนพัฒนาอำเภอ")
                st.write(f"🏢 ระดับจังหวัด: สนับสนุนตัวชี้วัดจังหวัดแม่ฮ่องสอน")
    else:
        st.warning("กรุณากรอกข้อมูลใน Step 1 ก่อน")

# --- STEP 3: SWOT ANALYSIS ---
elif step == "Step 3: SWOT Analysis":
    st.header("🔍 ขั้นตอนที่ 3: วิเคราะห์สภาพแวดล้อม (SWOT Analysis)")
    
    strengths, weaknesses = [], []
    if not st.session_state.ip_data.empty:
        for index, row in st.session_state.ip_data.iterrows():
            if row['Importance'] >= 3 and row['Performance'] >= 3:
                strengths.append(row['ประเด็น'])
            elif row['Importance'] >= 3 and row['Performance'] < 3:
                weaknesses.append(row['ประเด็น'])

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💪 จุดแข็ง (Strengths)")
        for s in strengths: st.success(f"✔️ {s}")
    with col2:
        st.subheader("⚠️ จุดอ่อน (Weaknesses)")
        for w in weaknesses: st.error(f"❌ {w}")

    col3, col4 = st.columns(2)
    with col3:
        st.session_state.opps = st.text_area("🌟 โอกาส (Opportunities)", value=st.session_state.opps)
    with col4:
        st.session_state.threats = st.text_area("🔥 อุปสรรค (Threats)", value=st.session_state.threats)

# --- STEP 4: TOWS MATRIX ---
elif step == "Step 4: TOWS Matrix & Strategy":
    st.header("🧠 ขั้นตอนที่ 4: การจัดทำแผนกลยุทธ์ (TOWS Matrix)")
    col1, col2 = st.columns(2)
    with col1:
        st.success("🎯 SO Strategy")
        st.session_state.so_strat = st.text_area("รุก (S+O)", value=st.session_state.so_strat)
    with col2:
        st.info("🛠️ WO Strategy")
        st.session_state.wo_strat = st.text_area("แก้ไข (W+O)", value=st.session_state.wo_strat)
    with col1:
        st.warning("🛡️ ST Strategy")
        st.session_state.st_strat = st.text_area("ป้องกัน (S+T)", value=st.session_state.st_strat)
    with col2:
        st.error("⚠️ WT Strategy")
        st.session_state.wt_strat = st.text_area("รับ (W+T)", value=st.session_state.wt_strat)

# --- STEP 7: EXPORT PDF ---
elif step == "Step 7: สรุปและ Export PDF":
    st.header("📄 สร้างและดาวน์โหลดเอกสาร (PDF Export)")
    st.write("ระบบจะรวบรวมข้อมูลที่คุณวิเคราะห์ทั้งหมดจัดทำเป็นรูปเล่ม PDF")

    # ฟังก์ชันสร้าง PDF
    def generate_pdf():
        pdf = FPDF()
        pdf.add_page()
        
        # ตรวจสอบว่ามีไฟล์ฟอนต์ภาษาไทยหรือไม่
        if os.path.exists("THSarabunNew.ttf"):
            pdf.add_font('THSarabunNew', '', 'THSarabunNew.ttf', uni=True)
            pdf.set_font('THSarabunNew', '', 18)
        else:
            pdf.set_font('Arial', 'B', 16)
            st.warning("⚠️ ไม่พบไฟล์ THSarabunNew.ttf - ภาษาไทยอาจไม่แสดงผล")

        # พิมพ์หัวข้อ
        pdf.cell(200, 10, txt="รายงานการวิเคราะห์แผนพัฒนาชุมชนเชิงพื้นที่แบบบูรณาการ", ln=True, align='C')
        pdf.cell(200, 10, txt="(Integrated Community Development Plan)", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font('THSarabunNew', '', 16) if os.path.exists("THSarabunNew.ttf") else pdf.set_font('Arial', '', 12)
        
        # เพิ่มข้อมูลปัจจัยภายนอก
        pdf.cell(200, 10, txt="1. ปัจจัยภายนอก (Opportunities & Threats):", ln=True)
        pdf.multi_cell(0, 10, txt=f"โอกาส (O): {st.session_state.opps}")
        pdf.multi_cell(0, 10, txt=f"อุปสรรค (T): {st.session_state.threats}")
        pdf.ln(5)

        # เพิ่มข้อมูลกลยุทธ์ TOWS
        pdf.cell(200, 10, txt="2. กลยุทธ์การพัฒนา (TOWS Strategy):", ln=True)
        pdf.multi_cell(0, 10, txt=f"- เชิงรุก (SO): {st.session_state.so_strat}")
        pdf.multi_cell(0, 10, txt=f"- เชิงแก้ไข (WO): {st.session_state.wo_strat}")
        pdf.multi_cell(0, 10, txt=f"- เชิงป้องกัน (ST): {st.session_state.st_strat}")
        pdf.multi_cell(0, 10, txt=f"- เชิงรับ (WT): {st.session_state.wt_strat}")
        
        # บันทึกเป็นไฟล์ชั่วคราว
        pdf.output("plan_report.pdf")

    # ปุ่มกดสร้างและดาวน์โหลด
    if st.button("ประมวลผลข้อมูลสร้างไฟล์ PDF"):
        generate_pdf()
        with open("plan_report.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.success("✅ สร้างไฟล์สำเร็จ! กดปุ่มด้านล่างเพื่อดาวน์โหลดได้เลยครับ")
        st.download_button(
            label="📥 ดาวน์โหลดไฟล์แผนพัฒนา (PDF)",
            data=PDFbyte,
            file_name="Integrated_CD_Plan.pdf",
            mime='application/octet-stream'
        )
