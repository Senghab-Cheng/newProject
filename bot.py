import streamlit as st
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from io import BytesIO

st.set_page_config(page_title="ប្រព័ន្ធឆ្នោត", layout="wide")

# Initialize session state
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'admin_username' not in st.session_state:
    st.session_state.admin_username = ""
if 'lottery_name_set' not in st.session_state:
    st.session_state.lottery_name_set = False
if 'lottery_name' not in st.session_state:
    st.session_state.lottery_name = ""
if 'lotteries' not in st.session_state:
    st.session_state.lotteries = []
if 'show_form' not in st.session_state:
    st.session_state.show_form = False

# Login Page
if not st.session_state.admin_logged_in:
    st.markdown("<h1 style='text-align: center;'>ប្រព័ន្ធឆ្នោត</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'></p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("បញ្ចូលឈ្មោះអ្នកគ្រប់គ្រង")
        password = st.text_input("បញ្ចូលលេខសម្ងាត់", type="password")
        if st.button("ចូលប្រព័ន្ធ"):
            if username.strip() and password == "88889999":
                st.session_state.admin_username = username
                st.session_state.admin_logged_in = True
                st.rerun()
            elif password != "88889999":
                st.error("លេខសម្ងាត់មិនត្រឹមត្រូវ!")
            else:
                st.error("សូមបញ្ចូលឈ្មោះអ្នកគ្រប់គ្រង")
    st.stop()

# Lottery Name Setup
if not st.session_state.lottery_name_set:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("<h2>កំណត់ឈ្មោះក្រដាសឆ្នោត</h2>", unsafe_allow_html=True)
    with col2:
        if st.button("ចាកចេញ"):
            st.session_state.admin_logged_in = False
            st.session_state.admin_username = ""
            st.rerun()
    
    st.markdown(f"**ស្វាគមន៍, {st.session_state.admin_username}**")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        lottery_name = st.text_input("បញ្ចូលឈ្មោះក្រដាសឆ្នោត")
        if st.button("បន្ត"):
            if lottery_name.strip():
                st.session_state.lottery_name = lottery_name
                st.session_state.lottery_name_set = True
                st.rerun()
            else:
                st.error("សូមបញ្ចូលឈ្មោះក្រដាសឆ្នោត")
    st.stop()

# Main Dashboard
st.markdown(f"<h1>{st.session_state.lottery_name}</h1>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

with col1:
    st.markdown(f"**អ្នកគ្រប់គ្រង: {st.session_state.admin_username}**")

with col3:
    if st.button("ផ្លាស់ប្តូរឆ្នោត"):
        st.session_state.lottery_name_set = False
        st.session_state.lottery_name = ""
        st.session_state.lotteries = []
        st.session_state.show_form = False
        st.rerun()

with col4:
    if st.button("ចាកចេញ"):
        st.session_state.admin_logged_in = False
        st.session_state.admin_username = ""
        st.session_state.lottery_name_set = False
        st.session_state.lottery_name = ""
        st.session_state.lotteries = []
        st.session_state.show_form = False
        st.rerun()

st.divider()

# Add New Entry
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("➕ បន្ថែមក្រដាសថ្មី"):
        st.session_state.show_form = not st.session_state.show_form

with col2:
    if len(st.session_state.lotteries) > 0:
        if st.button("⬇️ នាំចេញទិន្នន័យ"):
            data = {
                "lottery_name": st.session_state.lottery_name,
                "lotteries": st.session_state.lotteries
            }
            json_str = json.dumps(data, ensure_ascii=False, indent=2)
            st.download_button(
                label="ទាញយក JSON",
                data=json_str,
                file_name=f"{st.session_state.lottery_name}_data.json",
                mime="application/json"
            )

st.divider()

# Form to add new entry
if st.session_state.show_form:
    with st.form("lottery_form"):
        st.subheader("បន្ថែមលម្អិតឆ្នោតថ្មី")
        
        date = st.date_input("ថ្ងៃ")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            result_1pm = st.text_input("លទ្ធផល ១:០០ PM(ពេលថ្ងៃ)")
        with col2:
            result_4pm = st.text_input("លទ្ធផល ៤:០០ PM(ពេលថ្ងៃ)")
        with col3:
            result_6pm = st.text_input("លទ្ធផល ៦:០០ PM(ពេលថ្ងៃ)")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("✅ បញ្ចូន ក៏ បន្ថែម")
        with col2:
            cancel = st.form_submit_button("❌ បោះបង់")
        
        if submit:
            if date and (result_1pm or result_4pm or result_6pm):
                new_lottery = {
                    "date": str(date),
                    "time1": {"time": "1 PM", "result": result_1pm},
                    "time4": {"time": "4 PM", "result": result_4pm},
                    "time6": {"time": "6 PM", "result": result_6pm}
                }
                st.session_state.lotteries.append(new_lottery)
                st.session_state.show_form = False
                st.success("បានបន្ថែមហេីយ!")
                st.rerun()
            else:
                st.error("បំពេញលេខឆ្នោតយ៉ាងតិចមួយ")
        
        if cancel:
            st.session_state.show_form = False
            st.rerun()

st.divider()

# Display Lotteries
if not st.session_state.lotteries:
    st.info("អត់មានឆ្នោត។ ចុច 'បន្ថែមឆ្នោត' ម្តងទៀត")
else:
    for idx, lottery in enumerate(st.session_state.lotteries):
        with st.expander(f"📅 ថ្ងៃ: {lottery['date']}", expanded=False):
            
            # Display results
            st.subheader("លទ្ធផល")
            
            cols = st.columns(3)
            
            if lottery['time1']['result']:
                with cols[0]:
                    st.info(f"**{lottery['time1']['time']}**\n\n{lottery['time1']['result']}", icon="🎰")
            
            if lottery['time4']['result']:
                with cols[1]:
                    st.warning(f"**{lottery['time4']['time']}**\n\n{lottery['time4']['result']}", icon="🎰")
            
            if lottery['time6']['result']:
                with cols[2]:
                    st.success(f"**{lottery['time6']['time']}**\n\n{lottery['time6']['result']}", icon="🎰")
            
            st.divider()
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("✏️ កែប្រែ(Edit -,-)", key=f"edit_{idx}"):
                    pass
            
            with col2:
                # Generate PDF
                try:
                    pdf_buffer = BytesIO()
                    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
                    elements = []
                    styles = getSampleStyleSheet()
                    
                    # Title
                    title_style = ParagraphStyle(
                        'CustomTitle',
                        parent=styles['Heading1'],
                        fontSize=20,
                        textColor=colors.HexColor('#1f77b4'),
                        spaceAfter=20,
                        alignment=1
                    )
                    elements.append(Paragraph(st.session_state.lottery_name, title_style))
                    elements.append(Spacer(1, 0.2*inch))
                    
                    # Date
                    date_style = ParagraphStyle('DateStyle', parent=styles['Normal'], fontSize=12, spaceAfter=15)
                    elements.append(Paragraph(f"<b>DATE: {lottery['date']}</b>", date_style))
                    elements.append(Spacer(1, 0.15*inch))
                    
                    # Results table
                    table_data = [["time", "result"]]
                    if lottery['time1']['result']:
                        table_data.append([lottery['time1']['time'], lottery['time1']['result']])
                    if lottery['time4']['result']:
                        table_data.append([lottery['time4']['time'], lottery['time4']['result']])
                    if lottery['time6']['result']:
                        table_data.append([lottery['time6']['time'], lottery['time6']['result']])
                    
                    table = Table(table_data, colWidths=[2.5*inch, 2.5*inch])
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 1), (-1, -1), 14),
                        ('ROWHEIGHTS', (0, 0), (-1, -1), 0.4*inch),
                    ]))
                    elements.append(table)
                    
                    doc.build(elements)
                    pdf_buffer.seek(0)
                    
                    st.download_button(
                        label="📄 ទាញយក PDF",
                        data=pdf_buffer,
                        file_name=f"{st.session_state.lottery_name}_{lottery['date']}.pdf",
                        mime="application/pdf",
                        key=f"pdf_{idx}"
                    )
                except Exception as e:
                    st.error(f"Error creating PDF: {e}")
            
            with col3:
                if st.button("🗑️ លុប", key=f"delete_{idx}"):
                    st.session_state.lotteries.pop(idx)
                    st.success("បានលុបដោយជោគជ័យ!")
                    st.rerun()