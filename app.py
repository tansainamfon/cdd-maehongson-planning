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

# กำหนดค่าเริ่มต้นของ O และ T
if 'opps' not in st.session_state:
    st.session_state.opps = "- นโยบายส่งเสริมการท่องเที่ยวเมืองรองและการท่องเที่ยวเชิงวัฒนธรรม\n- การขับเคลื่อนแนวคิด 'ฮ่องสอน ฮอมฮัก' เพื่อสร้างองค์กรแห่งความสุข"
if 'threats' not in st.session_state:
    st.session_state.threats = "- สภาพภูมิประเทศเป็นภูเขาสูงชัน ทำให้การคมนาคมขนส่งเข้าถึงยากลำบาก\n- ปัญหาหมอกควันไฟป่า (PM 2.5)"

# ตัวแปรเก็บกลยุทธ์ TOWS
if 'so_strat' not in st.session_state: st.session_state.so_strat = ""
if 'wo_strat' not in st.session_state: st.session_state.wo_strat = ""
if 'st_strat' not in st.session_state: st.session_state.st_strat = ""
if 'wt_strat' not in st.session_state: st.session_state.wt_strat = ""
if 'auto_generated' not in st.session_state: st.session_state.auto_generated = False

# --- Sidebar: Navigation ---
st.sidebar.title("ระบบแผนพัฒนาชุมชน")
st.sidebar.caption("สำนักงานพัฒนาชุมชนจังหวัดแม่ฮ่องสอน")
step = st.sidebar.radio("เลือกขั้นตอนการทำงาน", [
    "Step 1: IP Matrix (ปัจจัยภายใน)",
    "Step 2: Policy Alignment",
    "Step 3: SWOT Analysis",
    "Step 4: TOWS Matrix (วิเคราะห์อัตโนมัติ)",
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
            st.session_state.auto_generated = False # รีเซ็ตการสร้างคำอัตโนมัติเมื่อข้อมูลเปลี่ยน

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
    if not st.session_state.ip_data.empty:
        for index, row in st.session_state.ip_data.iterrows():
            with st.expander(f"📌 ประเด็นวิเคราะห์: {row['ประเด็น']}"):
                st.markdown(f"""
                *   🏢 **แผนพัฒนาจังหวัดแม่ฮ่องสอน:** ยกระดับคุณภาพชีวิตและส่งเสริมเศรษฐกิจชุมชน รองรับเมืองท่องเที่ยว
                *   📊 **แผนพัฒนาเศรษฐกิจฯ ฉบับที่ 13:** หมุดหมายที่ 8 (ไทยมีพื้นที่และเมืองอัจฉริยะที่น่าอยู่ ปลอดภัย)
                *   🇹🇭 **แผนยุทธศาสตร์ชาติ 20 ปี:** ยุทธศาสตร์ที่ 4 (การสร้างโอกาสและความเสมอภาคทางสังคม)
                """)
    else:
        st.warning("กรุณากรอกข้อมูลใน Step 1 เพื่อวิเคราะห์ความเชื่อมโยง")

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
        if strengths:
            for s in strengths: st.success(f"✔️ {s}")
        else: st.info("ยังไม่มีข้อมูลจุดแข็ง")
    with col2:
        st.subheader("⚠️ จุดอ่อน (Weaknesses)")
        if weaknesses:
            for w in weaknesses: st.error(f"❌ {w}")
        else: st.info("ยังไม่มีข้อมูลจุดอ่อน")

    st.markdown("---")
    st.subheader("🌍 ปัจจัยภายนอก (Opportunities & Threats)")
    col3, col4 = st.columns(2)
    with col3:
        new_opps = st.text_area("🌟 โอกาส (Opportunities)", value=st.session_state.opps, height=150)
        if new_opps != st.session_state.opps:
            st.session_state.opps = new_opps
            st.session_state.auto_generated = False
    with col4:
        new_threats = st.text_area("🔥 อุปสรรค (Threats)", value=st.session_state.threats, height=150)
        if new_threats != st.session_state.threats:
            st.session_state.threats = new_threats
            st.session_state.auto_generated = False

# --- STEP 4: TOWS MATRIX ---
elif step == "Step 4: TOWS Matrix (วิเคราะห์อัตโนมัติ)":
    st.header("🧠 ขั้นตอนที่ 4: การจัดทำแผนกลยุทธ์ (Auto TOWS Matrix)")
    st.write("ระบบวิเคราะห์กลยุทธ์ให้เบื้องต้น จากจุดแข็ง-จุดอ่อน (Step 1) และ โอกาส-อุปสรรค (Step 3)")
    
    # --- Logic สร้างกลยุทธ์อัตโนมัติ ---
    if not st.session_state.auto_generated:
        strengths, weaknesses = [], []
        if not st.session_state.ip_data.empty:
            for index, row in st.session_state.ip_data.iterrows():
                if row['Importance'] >= 3 and row['Performance'] >= 3:
                    strengths.append(row['ประเด็น'])
                elif row['Importance'] >= 3 and row['Performance'] < 3:
                    weaknesses.append(row['ประเด็น'])

        # ฟังก์ชันสกัดคำสำคัญจาก O และ T
        def extract_keyword(text):
            if not text: return "โอกาส/อุปสรรคในพื้นที่"
            lines = text.split('\n')
            first_line = [l.replace('-','').strip() for l in lines if l.strip()]
            return first_line[0] if first_line else "โอกาส/อุปสรรคในพื้นที่"

        s_text = " และ ".join(strengths) if strengths else "ทุนชุมชนที่มี"
        w_text = " และ ".join(weaknesses) if weaknesses else "ประเด็นข้อจำกัด"
        o_text = extract_keyword(st.session_state.opps)
        t_text = extract_keyword(st.session_state.threats)

        # ร่างประโยคกลยุทธ์
        st.session_state.so_strat = f"ผลักดัน {s_text} เพื่อยกระดับและใช้ประโยชน์จาก {o_text}"
        st.session_state.wo_strat = f"ขอรับการสนับสนุนจาก {o_text} เพื่อมาแก้ปัญหาและพัฒนา {w_text}"
        st.session_state.st_strat = f"ใช้เครือข่ายความเข้มแข็งของ {s_text} เพื่อรับมือและลดผลกระทบจาก {t_text}"
        st.session_state.wt_strat = f"ปรับรูปแบบการดำเนินงาน {w_text} เพื่อหลีกเลี่ยงความเสี่ยงจาก {t_text}"
        st.session_state.auto_generated = True

    # แสดงผลและให้ผู้ใช้แก้ไขได้
    col1, col2 = st.columns(2)
    with col1:
        st.success("🎯 SO Strategy (กลยุทธ์เชิงรุก)")
        st.session_state.so_strat = st.text_area("รุก (S+O)", value=st.session_state.so_strat, height=100)
    with col2:
        st.info("🛠️ WO Strategy (กลยุทธ์เชิงแก้ไข)")
        st.session_state.wo_strat = st.text_area("แก้ไข (W+O)", value=st.session_state.wo_strat, height=100)
    with col1:
        st.warning("🛡️ ST Strategy (กลยุทธ์เชิงป้องกัน)")
        st.session_state.st_strat = st.text_area("ป้องกัน (S+T)", value=st.session_state.st_strat, height=100)
    with col2:
        st.error("⚠️ WT Strategy (กลยุทธ์เชิงรับ)")
        st.session_state.wt_strat = st.text_area("รับ (W+T)", value=st.session_state.wt_strat, height=100)

    if st.button("🔄 สั่งระบบคิดกลยุทธ์ใหม่ (Regenerate)"):
        st.session_state.auto_generated = False
        st.rerun()

# --- STEP 7: EXPORT PDF ---
elif step == "Step 7: สรุปและ Export PDF":
    st.header("📊 ขั้นตอนที่ 7: สรุปแผนพัฒนาเชิงพื้นที่แบบบูรณาการ")
    st.write("ตรวจสอบความถูกต้องของข้อมูลทั้งหมดก่อนทำการ Export เป็นไฟล์รายงาน")

    # ==========================================
    # ส่วนที่ 1: แสดงผลข้อมูลสรุปบนหน้าเว็บไซต์ (Web Preview)
    # ==========================================
    with st.container(border=True):
        st.subheader("📍 1. ความเชื่อมโยงยุทธศาสตร์ (Strategic Alignment)")
        st.info("สอดคล้องกับแผนพัฒนาจังหวัดแม่ฮ่องสอน, แผนพัฒนาเศรษฐกิจและสังคมแห่งชาติ ฉบับที่ 13 และยุทธศาสตร์ชาติ 20 ปี")

        st.subheader("🌍 2. ปัจจัยภายนอก (บริบทพื้นที่แม่ฮ่องสอน)")
        col_o, col_t = st.columns(2)
        with col_o:
            st.markdown("**🌟 โอกาส (Opportunities):**")
            st.write(st.session_state.opps)
        with col_t:
            st.markdown("**🔥 อุปสรรค (Threats):**")
            st.write(st.session_state.threats)

        st.subheader("🧠 3. กลยุทธ์การพัฒนา (TOWS Strategy)")
        st.success(f"**🎯 เชิงรุก (SO):** {st.session_state.so_strat}")
        st.info(f"**🛠️ เชิงแก้ไข (WO):** {st.session_state.wo_strat}")
        st.warning(f"**🛡️ เชิงป้องกัน (ST):** {st.session_state.st_strat}")
        st.error(f"**⚠️ เชิงรับ (WT):** {st.session_state.wt_strat}")

    st.markdown("---")

    # ==========================================
    # ส่วนที่ 2: ระบบ Export ไฟล์ PDF
    # ==========================================
    st.header("📄 สร้างและดาวน์โหลดเอกสาร (PDF Export)")
    st.write("หากข้อมูลด้านบนถูกต้องแล้ว สามารถกดปุ่มด้านล่างเพื่อสร้างไฟล์รายงาน PDF ได้เลยครับ")
    
    def generate_pdf():
        pdf = FPDF()
        pdf.add_page()
        
        # ผูกฟอนต์ภาษาไทย
        pdf.add_font('THSarabunNew', '', 'THSarabunNew.ttf', uni=True)
        pdf.set_font('THSarabunNew', '', 18)
            
        pdf.cell(200, 10, txt="รายงานการวิเคราะห์แผนพัฒนาชุมชนเชิงพื้นที่แบบบูรณาการ", ln=True, align='C')
        pdf.cell(200, 10, txt="(จังหวัดแม่ฮ่องสอน)", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font('THSarabunNew', '', 16)
        
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

    # สร้างปุ่มกดเพื่อออกเอกสาร
    if st.button("🖨️ ประมวลผลข้อมูลสร้างไฟล์ PDF"):
        # เช็คก่อนว่ามีไฟล์ฟอนต์ในระบบหรือยัง
        if not os.path.exists("THSarabunNew.ttf"):
            st.error("❌ ระบบไม่พบไฟล์ฟอนต์ 'THSarabunNew.ttf' กรุณาอัปโหลดไฟล์ลงใน GitHub ก่อนครับ")
        else:
            try:
                generate_pdf()
                with open("maehongson_cd_plan.pdf", "rb") as pdf_file:
                    PDFbyte = pdf_file.read()

                st.success("✅ สร้างไฟล์สำเร็จ! กรุณากดปุ่มด้านล่างเพื่อดาวน์โหลด")
                st.download_button(
                    label="📥 ดาวน์โหลดไฟล์แผนพัฒนา (PDF)",
                    data=PDFbyte,
                    file_name="MaeHongSon_CD_Plan.pdf",
                    mime='application/octet-stream'
                )
            except Exception as e:
                st.error(f"❌ เกิดข้อผิดพลาดในการสร้างเอกสาร: {e}")
       
           
