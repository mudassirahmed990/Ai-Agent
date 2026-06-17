import streamlit as st
import pandas as pd
from components.sidebar import render_sidebar
from components.navbar import render_header
from components.cards import render_metric_card
from components.charts import render_category_chart, render_priority_pie_chart
from database.database import get_all_reports
from utils.style_loader import load_styles

st.set_page_config(page_title="AI Crime Intelligence | Dashboard", page_icon="🛡️", layout="wide")

load_styles()
render_sidebar()

# Hero Header
st.markdown("""
<div style="padding: 10px 0 30px 0;">
    <h1 style="font-size:2.4rem; margin-bottom:4px;">📊 Analytics Dashboard</h1>
    <p style="color:#7c83a8; font-size:1rem; margin-top:0;">Real-time overview of crime intelligence metrics</p>
</div>
""", unsafe_allow_html=True)

reports = get_all_reports()
if not reports:
    st.info("No reports available.")
else:
    df = pd.DataFrame([dict(row) for row in reports])

    # ── KPI Row ──
    col1, col2, col3 = st.columns(3)
    with col1:
        render_metric_card("Total Reports", str(len(df)))
    with col2:
        high_priority = len(df[df['priority'] == 'High Priority'])
        render_metric_card("High Priority", str(high_priority))
    with col3:
        suspicious = len(df[df['suspicious_status'] == 'Suspicious'])
        render_metric_card("Suspicious Reports", str(suspicious))

    st.markdown("---")

    # ── Charts Row ──
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h3>Crime Categories</h3>", unsafe_allow_html=True)
        render_category_chart(df)
    with col2:
        st.markdown("<h3>Priority Distribution</h3>", unsafe_allow_html=True)
        render_priority_pie_chart(df)
