import streamlit as st
from components.sidebar import render_sidebar
from components.cards import render_report_card
from database.database import get_all_reports, update_report_status, update_ai_insights
from ai_engine.summary_generator import generate_summary
from ai_engine.fake_report_detector import detect_fake_report
from utils.style_loader import load_styles

st.set_page_config(page_title="AI Crime Intelligence | Admin", page_icon="🔒", layout="wide")

load_styles()
render_sidebar()

st.markdown("""
<div style="padding: 10px 0 30px 0;">
    <h1 style="font-size:2.4rem; margin-bottom:4px;">🔒 Admin Panel</h1>
    <p style="color:#7c83a8; font-size:1rem; margin-top:0;">Review, analyze and manage all crime reports</p>
</div>
""", unsafe_allow_html=True)

reports = get_all_reports()

if not reports:
    st.info("No pending reports.")
else:
    # Pagination
    page_size = 20
    total_pages = (len(reports) // page_size) + 1

    col_pg, _ = st.columns([1, 3])
    with col_pg:
        page_num = st.number_input("Page", min_value=1, max_value=total_pages, value=1)

    st.markdown(f"<p style='color:#7c83a8; font-size:0.85rem; margin-bottom:16px;'>Showing {page_size} of {len(reports)} reports — Page {page_num}/{total_pages}</p>", unsafe_allow_html=True)

    start_idx = (page_num - 1) * page_size
    end_idx = start_idx + page_size
    paginated_reports = reports[start_idx:end_idx]



    for row in paginated_reports:
        report = dict(row)
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                render_report_card(report)
            with col2:
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                if report.get('summary') is not None:
                    st.markdown(f"""
                    <div class="glass-card" style="padding:14px 18px;">
                        <p style="color:#7c83a8; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px; margin:0 0 6px 0;">AI Summary</p>
                        <p style="color:#f0f0ff; font-size:0.88rem; margin:0 0 12px 0;">{report['summary']}</p>
                        <p style="color:#7c83a8; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px; margin:0 0 4px 0;">Authenticity Score</p>
                        <p style="color:#a78bfa; font-weight:700; font-size:1.1rem; margin:0;">{report['authenticity_score']}% <span style="color:#7c83a8; font-size:0.8rem; font-weight:400;">({report['suspicious_status']})</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="glass-card" style="padding:14px 18px; text-align:center;">
                        <p style="color:#7c83a8; font-size:0.85rem; margin:0 0 10px 0;">🤖 AI Insights Not Generated</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("⚡ Generate AI Insights", key=f"ai_btn_{report['id']}"):
                        with st.spinner("Gemini AI is analyzing..."):
                            summary = generate_summary(report['description'])
                            fake_data = detect_fake_report(report['description'])
                            if summary.startswith("Error:") or "error" in fake_data:
                                err_msg = summary if summary.startswith("Error:") else fake_data.get("error")
                                st.error(f"⚠️ {err_msg}. Please wait or try again later.")
                            else:
                                update_ai_insights(report['id'], summary, fake_data['authenticity_score'], fake_data['suspicious_status'])
                                st.rerun()


        st.markdown("---")
