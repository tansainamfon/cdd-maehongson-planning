import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Integrated CD Planner (Mae Hong Son)", layout="wide")

# --- ส่วนของการเก็บข้อมูล (Session State) ---
if 'ip_data' not in st.session_state:
    st.session_state.ip_data = pd.DataFrame(columns=['ประเด็น', 'Importance', 'Performance'])

# กำหนดค่าเริ่มต้นของ O และ T ให้เป็นบริบทของแม่ฮ่องสอน
if 'opps' not in st.session_state:
    st.session_state.opps = "- นโยบายส่งเสริมการท่องเที่ยวเมืองรองและการท่องเที่ยวเชิงวัฒนธรรม/ธรรมชาติ\n- การขับเคลื่อนแนวคิด 'ฮ่องสอน ฮอมฮัก' เพื่อสร้างองค์กรแห่งความสุขอย่างยั่งยืน\n- นโยบายกระตุ้นเศรษฐกิจฐานรากและ OTOP"
if 'threats' not in st.session_state:
    st.session_state.threats = "- สภาพภูมิประเทศเป็นภูเขาสูงชัน ทำให้การคมนาคมขนส่งเข้าถึงยากลำบาก\n- ปัญหาหมอกควันไฟป่า (PM 2.5) ในช่วงฤดูแล้งกระทบการท่องเที่ยว\n- โครงสร้างประชากรผู้สูงอายุที่เพิ่มขึ้นในพื้นที่"
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
st.sidebar.caption("สำนักงานพัฒนาชุมชนจังหวัดแม่ฮ่องสอน")
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
        topic = col1.text_input("ประเด็นการพัฒนาพื้นที่ (เช่น กองทุนสตรี, สัมมาชีพชุมชน, OTOP)")
        imp = col2.slider("Importance (ความสำคัญ)", 1, 5, 3)
        perf = col3.slider("Performance (ผลงานที่ทำได้จริง)", 1, 5, 3)
        submit = st.form_submit_button("บันทึกข้อมูล")
        if submit and topic:
            new_data = pd.DataFrame({'ประเด็น': [topic], 'Importance': [imp], 'Performance': [perf]})
            st.session_state.ip_data = pd.concat([st.session_state.ip_data, new_data], ignore_index=True)

    if not st.session_state.ip_data.empty:
        fig = px.scatter(st.session_state.ip_data, x="Performance", y="Importance", text="ประเด็น",
                         range_x=[0, 6], range_y=[0, 6], title="การประเมินศักยภาพปัจจัยภายในพื้นที่")
        fig.add_hline(y=3.0, line_dash="dash", line_color="red")
        fig.add_vline(x=3.0, line_dash="dash", line_color="red")
        fig.update_traces(marker=dict(size=15, color='#1f77b4'), textposition='top center')
        st.plotly_chart(fig, use_container_width=True)

# --- STEP 2: POLICY ALIGNMENT ---
elif step == "Step 2: Policy Alignment":
    st.header("🔗 ขั้นตอนที่ 2: การบูรณาการยุทธศาสตร์ (Policy Alignment)")
    st.write("ระบบทำการเชื่อมโยงประเด็นจากพื้นที่ สู่แผนระดับจังหวัดและแผนระดับชาติ")
    
    if not st.session_state.ip_data.empty:
        for index, row in st.session_state.ip_data.iterrows():
            with st.expander(f"📌 ประเด็นวิเคราะห์: {row['ประเด็น']}"):
                st.markdown(f"""
                *   🏢 **แผนพัฒนาจังหวัดแม่ฮ่องสอน:** 
                    *   สอดคล้องกับยุทธศาสตร์การยกระดับคุณภาพชีวิตและส่งเสริมเศรษฐกิจชุมชน เพื่อรองรับการเป็นเมืองท่องเที่ยวเชิงนิเวศและวัฒนธรรม
                *   📊 **แผนพัฒนาเศรษฐกิจและสังคมแห่งชาติ ฉบับที่ 13:** 
                    *   สนับสนุนหมุดหมายที่ 8: ไทยมีพื้นที่และเมืองอัจฉริยะที่น่าอยู่ ปลอดภัย เติบโตได้อย่างยั่งยืน (ลดความเหลื่อมล้ำเชิงพื้นที่)
                *   🇹🇭 **แผนยุทธศาสตร์ชาติ 20 ปี:** 
                    *   ตอบโจทย์ยุทธศาสตร์ที่ 4: การสร้างโอกาสและความเสมอภาคทางสังคม (การเสริมสร้างพลังทางสังคมและการกระจายศูนย์กลางความเจริญ)
                """)
    else:
        st.warning("กรุณากรอกข้อมูลใน Step 1 เพื่อวิเคราะห์ความเชื่อมโยง")

# --- STEP 3: SWOT ANALYSIS ---
elif step == "Step 3: SWOT Analysis":
    st.header("🔍 ขั้นตอนที่ 3: วิเคราะห์สภาพแวดล้อม (SWOT Analysis - Mae Hong Son Context)")
    st.write("ผสานจุดแข็ง/จุดอ่อนจากผลการทำงาน (Step 1) เข้ากับบริบททางภูมิสังคมของจังหวัดแม่ฮ่องสอน")
    
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
        st.caption("ดึงข้อมูลอัตโนมัติจาก IP Matrix (Importance >= 3, Performance >= 3)")
        if strengths:
            for s in strengths: st.success(f"✔️ {s}")
        else:
            st.info("ยังไม่มีข้อมูลจุดแข็ง")
    with col2:
        st.subheader("⚠️ จุดอ่อน (Weaknesses)")
        st.caption("ดึงข้อมูลอัตโนมัติจาก IP Matrix (Importance >= 3, Performance < 3)")
        if weaknesses:
            for w in weaknesses: st.error(f"❌ {w}")
        else:
            st.info("ยังไม่มีข้อมูลจุดอ่อน")

    st.markdown("---")
    st.subheader("🌍 ปัจจัยภายนอก (Opportunities & Threats)")
    st.write("*ระบบกำหนดค่าเริ่มต้นจากฐานข้อมูลบริบทจังหวัดแม่ฮ่องสอน สามารถพิมพ์แก้ไขหรือเพิ่มติมได้*")
    col3, col4 = st.columns(2)
    with col3:
        st.session_state.opps = st.text_area("🌟 โอกาส (Opportunities)", value=st.session_state.opps, height=180)
    with col4:
        st.session_state.threats = st.text_area("🔥 อุปสรรค (Threats)", value=st.session_state.threats, height=180)

# --- STEP 4: TOWS MATRIX ---
elif step == "Step 4: TOWS Matrix & Strategy":
    st.header("🧠 ขั้นตอนที่ 4: การจัดทำแผนกลยุทธ์ (TOWS Matrix)")
    st.write("สร้างกลยุทธ์เชิงรุกและเชิงรับ โดยอิงข้อมูลพื้นที่และการวิเคราะห์ยุทธศาสตร์จังหวัด")
    col1, col2 = st.columns(2)
    with col1:
        st.success("🎯 SO Strategy (กลยุทธ์เชิงรุก)")
        st.session_state.so_strat = st.text_area("รุก (S+O) - ใช้ทุนชุมชนคว้าโอกาสระดับพื้นที่", value=st.session_state.so_strat)
    with col2:
        st.info("🛠️ WO Strategy (กลยุทธ์เชิงแก้ไข)")
        st.session_state.wo_strat = st.text_area("แก้ไข (W+O) - ใช้นโยบายรัฐหนุนเสริมจุดอ่อน", value=st.session_state.wo_strat)
    with col1:
        st.warning("🛡️ ST Strategy (กลยุทธ์เชิงป้องกัน)")
        st.session_state.st_strat = st.text_area("ป้องกัน (S+T) - สร้างความต้านทานต่ออุปสรรค", value=st.session_state.st_strat)
    with col2:
        st.error("⚠️ WT Strategy (กลยุทธ์เชิงรับ)")
        st.session_state.wt_strat = st.text_area("รับ (W+T) - ถอยเพื่อปรับโครงสร้างกลุ่ม", value=st.session_state.wt_strat)

# --- STEP 7: EXPORT PDF ---
elif step == "Step 7: สรุปและ Export PDF":
    st.header("📄 สร้างและดาวน์โหลดเอกสาร (PDF Export)")
    
    def generate_pdf():
        pdf = FPDF()
        pdf.add_page()
        
        if os.path.exists("THSarabunNew.ttf"):
            pdf.add_font('THSarabunNew', '', 'THSarabunNew.ttf', uni=True)
            pdf.set_font('THSarabunNew', '', 18)
        else:
            pdf.set_font('Arial', 'B', 16)
            
        pdf.cell(200, 10, txt="รายงานการวิเคราะห์แผนพัฒนาชุมชนเชิงพื้นที่แบบบูรณาการ", ln=True, align='C')
        pdf.cell(200, 10, txt="(จังหวัดแม่ฮ่องสอน)", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font('THSarabunNew', '', 16) if os.path.exists("THSarabunNew.ttf") else pdf.set_font('Arial', '', 12)
        
        pdf.cell(200, 10, txt="1. ความเชื่อมโยงยุทธศาสตร์ (Strategic Alignment):", ln=True)
        pdf.multi_cell(0, 10, txt="- สอดคล้องกับแผนพัฒนาจังหวัดแม่ฮ่องสอน, แผนพัฒนาเศรษฐกิจและสังคมแห่งชาติ ฉบับที่ 13 และยุทธศาสตร์ชาติ 20 ปี")
        pdf.ln(5)

        pdf.cell(200, 10, txt="2. ปัจจัยภายนอก (บริบทพื้นที่แม่ฮ่องสอน):", ln=True)
        pdf.multi_cell(0, 8, txt=f"โอกาส (O):\n{st.session_state.opps}")
        pdf.ln(2)
        pdf.multi_cell(0, 8, txt=f"อุปสรรค (T):\n{st.session_state.threats}")
        pdf.ln(5)

        pdf.cell(200, 10, txt="3. กลยุทธ์การพัฒนา (TOWS Strategy):", ln=True)
        pdf.multi_cell(0, 10, txt=f"เชิงรุก (SO): {st.session_state.so_strat}")
        pdf.multi_cell(0, 10, txt=f"เชิงแก้ไข (WO): {st.session_state.wo_strat}")
        pdf.multi_cell(0, 10, txt=f"เชิงป้องกัน (ST): {st.session_state.st_strat}")
        pdf.multi_cell(0, 10, txt=f"เชิงรับ (WT): {st.session_state.wt_strat}")
        
        pdf.output("maehongson_cd_plan.pdf")

    if st.button("ประมวลผลข้อมูลสร้างไฟล์ PDF"):
        generate_pdf()
        with open("maehongson_cd_plan.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.success("✅ สร้างไฟล์สำเร็จ!")
        st.download_button(
            label="📥 ดาวน์โหลดไฟล์แผนพัฒนา (PDF)",
            data=PDFbyte,
            file_name="MaeHongSon_CD_Plan.pdf",
            mime='application/octet-stream'
        )
