import streamlit as st

def render_header(title: str, subtitle: str = ""):
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p style='color: #94a3b8;'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown("---")
