import streamlit as st
import pandas as pd
from components.sidebar import render_sidebar
from components.cards import render_metric_card
from components.maps import render_hotspot_map
from database.database import get_all_reports
from ai_engine.hotspot_predictor import get_hotspot_statistics
from utils.style_loader import load_styles

st.set_page_config(page_title="AI Crime Intelligence | Hotspot", page_icon="🗺️", layout="wide")

load_styles()
render_sidebar()

st.markdown("""
<div style="padding: 10px 0 30px 0;">
    <h1 style="font-size:2.4rem; margin-bottom:4px;">🗺️ Crime Hotspot Prediction</h1>
    <p style="color:#7c83a8; font-size:1rem; margin-top:0;">Geospatial heatmap analysis of high-risk crime zones</p>
</div>
""", unsafe_allow_html=True)

reports = get_all_reports()

if not reports:
    st.info("No data available for hotspot analysis.")
else:
    df = pd.DataFrame([dict(row) for row in reports])
    stats = get_hotspot_statistics(df)

    # Stats Row
    col1, col2, col3 = st.columns(3)
    with col1:
        render_metric_card("📍 Total Mapped Reports", str(stats['total_reports']))
    with col2:
        render_metric_card("🔴 High Risk Reports", str(stats['high_risk_areas']))
    with col3:
        render_metric_card("⚠️ Most Common Crime", stats['most_common_crime'])

    st.markdown("---")

    # Crime Distribution
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("<h3>Crime Distribution</h3>", unsafe_allow_html=True)
        crime_counts = df['category'].value_counts().reset_index()
        crime_counts.columns = ['Crime Type', 'Count']
        for _, row in crime_counts.iterrows():
            pct = int((row['Count'] / len(df)) * 100)
            color = "#a78bfa" if pct > 20 else "#06b6d4" if pct > 10 else "#10b981"
            st.markdown(f"""
            <div style="margin-bottom: 10px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <span style="color:#f0f0ff; font-size:0.85rem;">{row['Crime Type']}</span>
                    <span style="color:{color}; font-weight:700; font-size:0.85rem;">{row['Count']} ({pct}%)</span>
                </div>
                <div style="background:rgba(255,255,255,0.06); border-radius:100px; height:6px;">
                    <div style="background:linear-gradient(90deg, {color}, rgba(6,182,212,0.6)); width:{pct}%; height:6px; border-radius:100px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(
            '<div style="display:flex; justify-content:space-between; align-items:center;">'
            '<h3 style="margin:0;">Crime Map</h3>'
            '</div>', 
            unsafe_allow_html=True
        )
        
        show_heatmap = st.toggle("🔥 Show Heatmap (Hide Markers)", value=True)
        
        import folium
        from folium.plugins import HeatMap
        from streamlit_folium import st_folium
        
        if df.empty:
            m = folium.Map(location=[0, 0], zoom_start=2, tiles="CartoDB dark_matter")
            st_folium(m, width="100%", height=480, returned_objects=[])
        else:
            center_lat = df['latitude'].mean()
            center_lon = df['longitude'].mean()

            m = folium.Map(
                location=[center_lat, center_lon],
                zoom_start=12,
                tiles="CartoDB dark_matter"
            )
            
            if show_heatmap:
                heat_data = [[row['latitude'], row['longitude']] for _, row in df.iterrows()]
                HeatMap(
                    heat_data, 
                    radius=25, 
                    blur=25, 
                    max_zoom=1,
                    gradient={
                        '0.2': '#312e81', 
                        '0.4': '#4338ca', 
                        '0.6': '#7c3aed', 
                        '0.8': '#e11d48', 
                        '1.0': '#fbbf24'
                    }
                ).add_to(m)
            else:
                for _, row in df.iterrows():
                    p = row.get('priority', '')
                    if p == 'High Priority':
                        color = '#f43f5e'
                    elif p == 'Medium Priority':
                        color = '#f59e0b'
                    else:
                        color = '#10b981'

                    folium.CircleMarker(
                        location=[row['latitude'], row['longitude']],
                        radius=5,
                        popup=folium.Popup(
                            f"<b>{row.get('category','Crime')}</b><br>{row.get('location','')}<br>{p}",
                            max_width=200
                        ),
                        color=color,
                        fill=True,
                        fill_color=color,
                        fill_opacity=0.85,
                        weight=1.5
                    ).add_to(m)

            st_folium(m, width="100%", height=480, returned_objects=[])
