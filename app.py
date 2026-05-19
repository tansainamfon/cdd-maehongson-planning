import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Integrated CD Planner (Mae Hong Son)", layout="wide")

# --- ส่วนของการเก็บข้อมูล (Session State) ---
if 'ip_data' not in st.session_state: st.session_state.ip_data = pd.DataFrame(columns=['ประเด็น', 'Importance', 'Performance'])
if 'manual_s' not in st.session_state: st.session_state.manual_s = ""
if 'manual_w' not in st.session_state: st.session_state.manual_w = ""
if 'opps' not in st.session_state: st.session_state.opps = "- นโยบายส่งเสริมการท่องเที่ยวเมืองรอง\n- การขับเคลื่อนแนวคิด 'ฮ่องสอน ฮอมฮัก'"
if 'threats' not in st.session_state: st.session_state.threats = "- สภาพภูมิประเทศเป็นภูเขาสูงชัน\n- ปัญหาหมอกควันไฟป่า (PM 2.5)"

# ตัวแปรเก็บข้อความประมวลผล
if 's_txt' not in st.session_state: st.session_state.s_txt = "ทุนชุมชน"
if 'w_txt' not in st.session_state: st.session_state.w_txt = "ข้อจำกัด"
if 'so_strat' not in st.session_state: st.session_state.so_strat = ""
if 'wo_strat' not in st.session_state: st.session_state.wo_strat = ""
if 'st_strat' not in st.session_state: st.session_state.st_strat = ""
if 'wt_strat' not in st.session_state: st.session_state.wt_strat = ""
if 'auto_generated' not in st.session_state: st.session_state.auto_generated = False

# Session State สำหรับ Step 5 และ 6
if 'vision' not in st.session_state: st.session_state.vision = "มุ่งสู่องค์กรแห่งความสุข 'ฮ่องสอน ฮอมฮัก' ชุมชนเข้มแข็ง เศรษฐกิจฐานรากมั่นคง"
if 'mission' not in st.session_state: st.session_state.mission = "1. ยกระดับคุณภาพชีวิตชุมชน\n2. ส่งเสริมสัมมาชีพและรายได้\n3. บูรณาการภาคีเครือข่ายการพัฒนา"
if 'kpi' not in st.session_state: st.session_state.kpi = "รายได้เฉลี่ยของชุมชนเป้าหมายเพิ่มขึ้นร้อยละ 5 ต่อปี"
if 'projects' not in st.session_state: st.session_state.projects = pd.DataFrame(columns=['ชื่อโครงการ', 'งบประมาณ', 'กลยุทธ์ที่รองรับ'])

# --- Sidebar: Navigation ---
st.sidebar.title("ระบบแผนพัฒนาชุมชน")
st.sidebar.caption("สำนักงานพัฒนาชุมชนจังหวัดแม่ฮ่องสอน")
step = st.sidebar.radio("เลือกขั้นตอนการทำงาน", [
    "Step 1: IP Matrix (ปัจจัยภายใน)",
    "Step 2: Policy Alignment",
    "Step 3: SWOT Analysis",
    "Step 4: TOWS Matrix (วิเคราะห์กลยุทธ์)",
    "Step 5: วิเคราะห์ทิศทางและวิสัยทัศน์",
    "Step 6: โครงการสำคัญ (Action Plan)",
    "Step 7: สรุปและ Export PDF"
])

# --- STEP 1: IP MATRIX ---
if step == "Step 1: IP Matrix (ปัจจัยภายใน)":
    st.header("📍 ขั้นตอนที่ 1: วิเคราะห์งานพัฒนาชุมชน (IP Matrix)")
    with st.form("ip_form"):
        col1, col2, col3 = st.columns([3, 1, 1])
        topic = col1.text_input("ประเด็นการพัฒนาพื้นที่")
        imp = col2.slider("Importance (ความสำคัญ)", 1, 5, 3)
        perf = col3.slider("Performance (ผลงานที่ทำได้จริง)", 1, 5, 3)
        submit = st.form_submit_button("บันทึกข้อมูล")
        if submit and topic:
            new_data = pd.DataFrame({'ประเด็น': [topic], 'Importance': [imp], 'Performance': [perf]})
            st.session_state.ip_data = pd.concat([st.session_state.ip_data, new_data], ignore_index=True)
            st.session_state.auto_generated = False

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
                st.markdown(f"* 🏢 **แผนพัฒนาจังหวัดแม่ฮ่องสอน:** ยกระดับคุณภาพชีวิตและส่งเสริมเศรษฐกิจชุมชน\n* 📊 **แผนพัฒนาเศรษฐกิจฯ ฉบับที่ 13:** หมุดหมายที่ 8\n* 🇹🇭 **แผนยุทธศาสตร์ชาติ 20 ปี:** ยุทธศาสตร์ที่ 4")
    else:
        st.warning("กรุณากรอกข้อมูลใน Step 1 ก่อน")

# --- STEP 3: SWOT ANALYSIS ---
elif step == "Step 3: SWOT Analysis":
    st.header("🔍 ขั้นตอนที่ 3: วิเคราะห์สภาพแวดล้อม (SWOT Analysis)")
    
    auto_s, auto_w = [], []
    if not st.session_state.ip_data.empty:
        for index, row in st.session_state.ip_data.iterrows():
            if row['Importance'] >= 3 and row['Performance'] >= 3: auto_s.append(row['ประเด็น'])
            elif row['Importance'] >= 3 and row['Performance'] < 3: auto_w.append(row['ประเด็น'])

    st.subheader("🏢 ปัจจัยภายใน (Internal Factors)")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**💪 จุดแข็ง (Strengths)**")
        if auto_s:
            for s in auto_s: st.success(f"✔️ {s}")
        new_man_s = st.text_area("➕ เพิ่มจุดแข็งอื่นๆ", value=st.session_state.manual_s, height=80)
        if new_man_s != st.session_state.manual_s:
            st.session_state.manual_s, st.session_state.auto_generated = new_man_s, False
            
    with col2:
        st.markdown("**⚠️ จุดอ่อน (Weaknesses)**")
        if auto_w:
            for w in auto_w: st.error(f"❌ {w}")
        new_man_w = st.text_area("➕ เพิ่มจุดอ่อนอื่นๆ", value=st.session_state.manual_w, height=80)
        if new_man_w != st.session_state.manual_w:
            st.session_state.manual_w, st.session_state.auto_generated = new_man_w, False

    st.markdown("---")
    st.subheader("🌍 ปัจจัยภายนอก (External Factors)")
    col3, col4 = st.columns(2)
    with col3:
        new_opps = st.text_area("🌟 โอกาส (Opportunities)", value=st.session_state.opps, height=120)
        if new_opps != st.session_state.opps:
            st.session_state.opps, st.session_state.auto_generated = new_opps, False
    with col4:
        new_threats = st.text_area("🔥 อุปสรรค (Threats)", value=st.session_state.threats, height=120)
        if new_threats != st.session_state.threats:
            st.session_state.threats, st.session_state.auto_generated = new_threats, False

# --- STEP 4: TOWS MATRIX ---
elif step == "Step 4: TOWS Matrix (วิเคราะห์กลยุทธ์)":
    st.header("🧠 ขั้นตอนที่ 4: สรุปกลยุทธ์ที่มีความเป็นไปได้ (TOWS Matrix)")
    if not st.session_state.auto_generated:
        auto_s, auto_w = [], []
        if not st.session_state.ip_data.empty:
            for index, row in st.session_state.ip_data.iterrows():
                if row['Importance'] >= 3 and row['Performance'] >= 3: auto_s.append(row['ประเด็น'])
                elif row['Importance'] >= 3 and row['Performance'] < 3: auto_w.append(row['ประเด็น'])
        
        man_s_list = [s.strip() for s in st.session_state.manual_s.split('\n') if s.strip()]
        man_w_list = [w.strip() for w in st.session_state.manual_w.split('\n') if w.strip()]
        
        all_s = auto_s + man_s_list
        all_w = auto_w + man_w_list
        
        def ex_kw(text): return [l.replace('-','').strip() for l in text.split('\n') if l.strip()][0] if text else "โอกาสภายนอก"
        
        st.session_state.s_txt = " และ ".join(all_s) if all_s else "ทุนชุมชน"
        st.session_state.w_txt = " และ ".join(all_w) if all_w else "ข้อจำกัด"
        o_kw = ex_kw(st.session_state.opps)
        t_kw = ex_kw(st.session_state.threats)
        
        # สรุปกลยุทธ์เป็นข้อๆ ที่ปฏิบัติได้จริง
        st.session_state.so_strat = f"1. ยกระดับ {st.session_state.s_txt} โดยใช้ประโยชน์จาก {o_kw}\n2. ขยายผลต้นแบบชุมชนเพื่อสร้างมูลค่าเพิ่มทางเศรษฐกิจ"
        st.session_state.wo_strat = f"1. บูรณาการความร่วมมือกับ {o_kw} เพื่อแก้ปัญหา {st.session_state.w_txt}\n2. พัฒนาศักยภาพและเสริมทักษะเทคโนโลยีให้ผู้นำชุมชน"
        st.session_state.st_strat = f"1. ใช้ความเข้มแข็งของ {st.session_state.s_txt} เป็นเกราะป้องกัน {t_kw}\n2. สร้างเครือข่ายเฝ้าระวังระดับตำบล"
        st.session_state.wt_strat = f"1. ปรับโครงสร้าง {st.session_state.w_txt} เพื่อลดความเสี่ยงจาก {t_kw}\n2. ชะลอกิจกรรมที่มีความเสี่ยงและเน้นการรวมกลุ่มช่วยเหลือเกื้อกูล"
        st.session_state.auto_generated = True

    col1, col2 = st.columns(2)
    with col1: st.session_state.so_strat = st.text_area("🎯 เชิงรุก (SO) - สรุปเป็นข้อ", value=st.session_state.so_strat, height=130)
    with col2: st.session_state.wo_strat = st.text_area("🛠️ เชิงแก้ไข (WO) - สรุปเป็นข้อ", value=st.session_state.wo_strat, height=130)
    with col1: st.session_state.st_strat = st.text_area("🛡️ เชิงป้องกัน (ST) - สรุปเป็นข้อ", value=st.session_state.st_strat, height=130)
    with col2: st.session_state.wt_strat = st.text_area("⚠️ เชิงรับ (WT) - สรุปเป็นข้อ", value=st.session_state.wt_strat, height=130)
    if st.button("🔄 ประมวลผลกลยุทธ์ใหม่"):
        st.session_state.auto_generated = False
        st.rerun()

# --- STEP 5: VISION, DIRECTION & KPI ---
elif step == "Step 5: วิเคราะห์ทิศทางและวิสัยทัศน์":
    st.header("🧭 ขั้นตอนที่ 5: วิเคราะห์ทิศทางการพัฒนาและเป้าประสงค์")
    
    # ระบบวิเคราะห์ทิศทางอัตโนมัติจากข้อมูล Step 4
    st.subheader("💡 บทวิเคราะห์ทิศทางการพัฒนา (Strategic Direction Analysis)")
    direction_analysis = f"จากการประมวลผลข้อมูล TOWS Matrix ทิศทางหลักที่ควรให้ความสำคัญในระยะนี้ คือการนำทุนชุมชน ได้แก่ **'{st.session_state.s_txt}'** มาเป็นตัวขับเคลื่อนหลัก (Growth Engine) ผสานกับนโยบายภาครัฐ ในขณะเดียวกันต้องเร่งอุดช่องโหว่ด้าน **'{st.session_state.w_txt}'** ด้วยการสร้างภาคีเครือข่าย เพื่อสร้างภูมิคุ้มกันต่อบริบทความเปลี่ยนแปลงของพื้นที่"
    st.info(direction_analysis)
    
    st.markdown("---")
    st.session_state.vision = st.text_input("👁️ วิสัยทัศน์ (Vision)", value=st.session_state.vision)
    st.session_state.mission = st.text_area("🚀 พันธกิจ (Mission)", value=st.session_state.mission, height=100)
    st.session_state.kpi = st.text_input("📈 ตัวชี้วัดเชิงยุทธศาสตร์ (KPIs)", value=st.session_state.kpi)

# --- STEP 6: ACTION PLAN ---
elif step == "Step 6: โครงการสำคัญ (Action Plan)":
    st.header("🚀 ขั้นตอนที่ 6: กำหนดแนวทางและโครงการสำคัญ")
    with st.form("project_form"):
        col1, col2, col3 = st.columns([2, 1, 1])
        proj_name = col1.text_input("ชื่อโครงการสำคัญ")
        budget = col2.text_input("งบประมาณ (บาท)", value="0")
        strat_ref = col3.selectbox("รองรับกลยุทธ์", ["เชิงรุก (SO)", "เชิงแก้ไข (WO)", "เชิงป้องกัน (ST)", "เชิงรับ (WT)"])
        submit_proj = st.form_submit_button("เพิ่มโครงการ")
        
        if submit_proj and proj_name:
            new_proj = pd.DataFrame({'ชื่อโครงการ': [proj_name], 'งบประมาณ': [budget], 'กลยุทธ์ที่รองรับ': [strat_ref]})
            st.session_state.projects = pd.concat([st.session_state.projects, new_proj], ignore_index=True)
            st.success(f"เพิ่มโครงการ '{proj_name}' สำเร็จ!")

    st.subheader("📋 ทะเบียนโครงการสำคัญ")
    if not st.session_state.projects.empty:
        st.table(st.session_state.projects)
        if st.button("ล้างข้อมูลโครงการทั้งหมด"):
            st.session_state.projects = pd.DataFrame(columns=['ชื่อโครงการ', 'งบประมาณ', 'กลยุทธ์ที่รองรับ'])
            st.rerun()
    else:
        st.info("ยังไม่มีข้อมูลโครงการ กรุณาเพิ่มข้อมูลด้านบน")

# --- STEP 7: EXPORT PDF ---
elif step == "Step 7: สรุปและ Export PDF":
    st.header("📊 ขั้นตอนที่ 7: สรุปแผนพัฒนาเชิงพื้นที่แบบบูรณาการ")
    
    with st.container(border=True):
        st.subheader("📍 1. วิสัยทัศน์และเป้าประสงค์")
        st.write(f"**วิสัยทัศน์:** {st.session_state.vision}")
        st.write(f"**ตัวชี้วัด:** {st.session_state.kpi}")
        
        st.subheader("🧠 2. กลยุทธ์การพัฒนา (TOWS Strategy)")
        st.success(f"**🎯 เชิงรุก (SO):**\n{st.session_state.so_strat}")
        st.info(f"**🛠️ เชิงแก้ไข (WO):**\n{st.session_state.wo_strat}")
        
        st.subheader("🚀 3. โครงการสำคัญ (Flagship Projects)")
        if not st.session_state.projects.empty: st.dataframe(st.session_state.projects, use_container_width=True)
        else: st.write("- ยังไม่ได้ระบุโครงการ -")

    st.markdown("---")
    st.header("📄 สร้างและดาวน์โหลดเอกสาร (PDF Export)")
    
    def generate_pdf():
        pdf = FPDF()
        pdf.add_page()
        
        if os.path.exists("THSarabunNew.ttf"):
            pdf.add_font('THSarabunNew', '', 'THSarabunNew.ttf', uni=True)
            pdf.set_font('THSarabunNew', '', 18)
        else: pdf.set_font('Arial', 'B', 16)
            
        pdf.cell(200, 10, txt="รายงานการวิเคราะห์แผนพัฒนาชุมชนเชิงพื้นที่แบบบูรณาการ", ln=True, align='C')
        pdf.cell(200, 10, txt="(จังหวัดแม่ฮ่องสอน)", ln=True, align='C')
        pdf.ln(5)
        
        pdf.set_font('THSarabunNew', '', 16) if os.path.exists("THSarabunNew.ttf") else pdf.set_font('Arial', '', 12)
        
        pdf.cell(200, 10, txt="1. ทิศทาง วิสัยทัศน์ และเป้าประสงค์:", ln=True)
        pdf.multi_cell(0, 8, txt=f"วิสัยทัศน์: {st.session_state.vision}\nตัวชี้วัด (KPIs): {st.session_state.kpi}")
        pdf.ln(2)

        pdf.cell(200, 10, txt="2. กลยุทธ์การพัฒนา (TOWS Strategy):", ln=True)
        pdf.multi_cell(0, 8, txt=f"[เชิงรุก - SO]\n{st.session_state.so_strat}\n\n[เชิงแก้ไข - WO]\n{st.session_state.wo_strat}\n\n[เชิงป้องกัน - ST]\n{st.session_state.st_strat}\n\n[เชิงรับ - WT]\n{st.session_state.wt_strat}")
        pdf.ln(2)
        
        pdf.cell(200, 10, txt="3. โครงการสำคัญ (Action Plan):", ln=True)
        if not st.session_state.projects.empty:
            for idx, row in st.session_state.projects.iterrows():
                pdf.multi_cell(0, 8, txt=f"- {row['ชื่อโครงการ']} (งบ: {row['งบประมาณ']} บ.) [{row['กลยุทธ์ที่รองรับ']}]")
        else:
            pdf.multi_cell(0, 8, txt="- ยังไม่ได้ระบุโครงการ -")
            
        pdf.output("maehongson_cd_plan.pdf")

    if st.button("🖨️ ประมวลผลข้อมูลสร้างไฟล์ PDF"):
        if not os.path.exists("THSarabunNew.ttf"): st.error("❌ ไม่พบไฟล์ฟอนต์ 'THSarabunNew.ttf' ใน GitHub")
        else:
            try:
                generate_pdf()
                with open("maehongson_cd_plan.pdf", "rb") as pdf_file: PDFbyte = pdf_file.read()
                st.success("✅ สร้างไฟล์สำเร็จ!")
                st.download_button("📥 ดาวน์โหลดรายงาน (PDF)", data=PDFbyte, file_name="MaeHongSon_CD_Plan.pdf", mime='application/octet-stream')
            except Exception as e: st.error(f"❌ Error: {e}")
