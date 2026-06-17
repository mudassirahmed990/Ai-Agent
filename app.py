import streamlit as st
from components.sidebar import render_sidebar
from database.database import init_db
from utils.style_loader import load_styles

st.set_page_config(page_title="AI Crime Intelligence Agent", page_icon="🛡️", layout="wide")

load_styles()
init_db()
render_sidebar()

st.switch_page("pages/dashboard.py")
