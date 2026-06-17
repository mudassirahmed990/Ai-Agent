import streamlit as st

def render_sidebar():
    st.sidebar.markdown("""
    <div style="padding: 16px 0 8px 0; text-align:center;">
        <div style="font-size:2rem; margin-bottom:4px;">🛡️</div>
        <p style="font-family:'Syne',sans-serif; font-weight:800; font-size:1.1rem;
                  background:linear-gradient(135deg,#a78bfa,#06b6d4);
                  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                  margin:0;">AI Crime Intelligence</p>
        <p style="color:#4a5080; font-size:0.68rem; letter-spacing:2px; text-transform:uppercase; margin:4px 0 0 0;">Agent Platform</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.page_link("pages/dashboard.py",        label="📊  Analytics Dashboard")
    st.sidebar.page_link("pages/admin_panel.py",      label="🔒  Admin Panel")
    st.sidebar.page_link("pages/hotspot_analysis.py", label="🗺️  Hotspot Prediction")
    st.sidebar.page_link("pages/safe_route.py",       label="🛣️  AI Safe Route")
    st.sidebar.page_link("pages/patrol_route.py",     label="🚓  AI Patrolling Agent")
    st.sidebar.markdown("---")

    st.sidebar.markdown("""
    <div style="padding: 12px; background:rgba(124,58,237,0.08); border:1px solid rgba(124,58,237,0.2);
                border-radius:12px; text-align:center;">
        <p style="color:#a78bfa; font-size:0.72rem; font-weight:600; letter-spacing:1px;
                  text-transform:uppercase; margin:0 0 4px 0;">Powered By</p>
        <p style="color:#f0f0ff; font-size:0.85rem; font-weight:700; margin:0;">Google Gemini AI</p>
        <p style="color:#4a5080; font-size:0.7rem; margin:4px 0 0 0;">gemini-2.5-flash</p>
    </div>
    """, unsafe_allow_html=True)
