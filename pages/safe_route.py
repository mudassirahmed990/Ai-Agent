import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from database.database import get_all_reports
from ai_engine.route_engine import (
    geocode_location, get_routes_from_osrm,
    calculate_route_risk, classify_risk_level
)
from ai_engine.route_analyzer import explain_route_safety
from utils.style_loader import load_styles
from components.sidebar import render_sidebar

st.set_page_config(page_title="AI Crime Intelligence | Safe Route", page_icon="🛣️", layout="wide")
load_styles()
render_sidebar()

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 10px 0 30px 0;">
    <h1 style="font-size:2.4rem; margin-bottom:4px;">🛣️ AI Safe Route System</h1>
    <p style="color:#7c83a8; font-size:1rem; margin-top:0;">
        Crime-aware intelligent route recommendation powered by Google Gemini AI
    </p>
</div>
""", unsafe_allow_html=True)

# ── Load Crime Data ──────────────────────────────────────────────────────────
reports = get_all_reports()
if reports:
    crime_df = pd.DataFrame([dict(r) for r in reports])
else:
    crime_df = pd.DataFrame()

# ── Input Form ───────────────────────────────────────────────────────────────
st.markdown("<h3>📍 Enter Your Journey Details</h3>", unsafe_allow_html=True)

with st.form("route_form"):
    col1, col2 = st.columns(2)
    with col1:
        source = st.text_input("🟢 Source Location", placeholder="e.g. Jinnah Road, Quetta")
    with col2:
        destination = st.text_input("🔴 Destination Location", placeholder="e.g. Satellite Town, Quetta")

    col3, col4 = st.columns(2)
    with col3:
        use_ai_explain = st.checkbox("🤖 Generate AI Safety Explanation", value=True,
                                     help="Uses Gemini API — uncheck to save API calls")
    with col4:
        crime_radius = st.slider("Crime Detection Radius (km)", 0.1, 1.5, 0.4, 0.1,
                                  help="How close to the route a crime must be to count")

    submitted = st.form_submit_button("🔍 Analyze Routes", use_container_width=True)

# ── Analysis ─────────────────────────────────────────────────────────────────
if submitted:
    if not source.strip() or not destination.strip():
        st.error("Please enter both Source and Destination locations.")
        st.stop()

    with st.spinner("📡 Locating addresses via OpenStreetMap..."):
        src_lat, src_lon = geocode_location(source)
        dst_lat, dst_lon = geocode_location(destination)

    if not src_lat or not dst_lat:
        st.error("❌ Could not locate one or both addresses. Please try more specific location names (e.g. add city name).")
        st.stop()

    with st.spinner("🗺️ Fetching route options via OpenStreetMap OSRM..."):
        routes = get_routes_from_osrm(src_lat, src_lon, dst_lat, dst_lon)

    if not routes:
        st.error("❌ No routes found between the given locations. Please try different addresses.")
        st.stop()

    # Score each route
    scored_routes = []
    for route in routes:
        risk_data = calculate_route_risk(route["coords"], crime_df, crime_radius)
        classification = classify_risk_level(risk_data["risk_score"])
        scored_routes.append({**route, **risk_data, **classification})

    # Sort: safest first (lowest risk, then fewest high priority, then fewest crimes, then shortest duration)
    scored_routes.sort(key=lambda r: (r["risk_score"], r["high_priority_count"], r["crime_count"], r["duration_min"]))
    
    # Keep only the single most optimal route
    scored_routes = scored_routes[:1]

    # ── AI Explanations ──────────────────────────────────────────────────────
    if use_ai_explain:
        with st.spinner("🤖 Gemini AI is analyzing route safety..."):
            for r in scored_routes:
                r["ai_explanation"] = explain_route_safety(
                    r["index"], r["risk_score"], r["level"],
                    r["crime_count"], r["high_priority_count"],
                    r["distance_km"], r["duration_min"],
                    source, destination
                )
    else:
        for r in scored_routes:
            r["ai_explanation"] = None

    # ── Map ──────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("<h3>🗺️ Route Map</h3>", unsafe_allow_html=True)

    map_center = [(src_lat + dst_lat) / 2, (src_lon + dst_lon) / 2]
    m = folium.Map(location=map_center, zoom_start=13, tiles="CartoDB dark_matter")

    # Crime heatmap layer
    if not crime_df.empty:
        from folium.plugins import HeatMap
        heat_data = [[r['latitude'], r['longitude']] for _, r in crime_df.iterrows()]
        HeatMap(heat_data, radius=12, blur=18, max_zoom=1, opacity=0.5,
                gradient={'0.3': '#7c3aed', '0.6': '#f59e0b', '1.0': '#f43f5e'}).add_to(m)

    # Draw routes (reverse order so safest is on top)
    for route in reversed(scored_routes):
        folium.PolyLine(
            locations=route["coords"],
            color=route["color"],
            weight=5 if route["risk_score"] <= 30 else 4,
            opacity=0.9 if route["risk_score"] <= 30 else 0.6,
            tooltip=f"{route['level']} | Risk: {route['risk_score']}/100 | {route['distance_km']} km"
        ).add_to(m)

    # Source & Destination Markers
    folium.Marker(
        [src_lat, src_lon],
        popup=f"<b>Start:</b> {source}",
        icon=folium.Icon(color="green", icon="play", prefix="fa")
    ).add_to(m)

    folium.Marker(
        [dst_lat, dst_lon],
        popup=f"<b>End:</b> {destination}",
        icon=folium.Icon(color="red", icon="flag", prefix="fa")
    ).add_to(m)

    st_folium(m, width="100%", height=500, returned_objects=[])

    # ── Route Cards ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("<h3>📋 Route Analysis Report</h3>", unsafe_allow_html=True)

    # Recommended route badge
    best = scored_routes[0]
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, rgba(16,185,129,0.12), rgba(6,182,212,0.08));
                border:1px solid rgba(16,185,129,0.3); border-radius:14px; padding:16px 20px;
                margin-bottom:24px; display:flex; align-items:center; gap:16px;">
        <span style="font-size:2rem;">✅</span>
        <div>
            <p style="color:#34d399; font-family:'Syne',sans-serif; font-weight:800;
                      font-size:1rem; margin:0 0 2px 0;">AI RECOMMENDED ROUTE</p>
            <p style="color:#f0f0ff; font-size:0.9rem; margin:0;">
                Route #{best['index']+1} — {best['distance_km']} km · {best['duration_min']} min ·
                Risk Score: <b style="color:#34d399;">{best['risk_score']}/100</b>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Individual route cards
    label_map = {0: "1st", 1: "2nd", 2: "3rd"}
    for i, route in enumerate(scored_routes):
        rank = label_map.get(i, f"{i+1}th")
        border_color = route["color"]
        bg_alpha = "0.10" if route["risk_score"] <= 30 else "0.08"

        # Risk bar
        bar_color = route["color"]
        risk_pct = route["risk_score"]

        ai_html = ""
        if route.get('ai_explanation'):
            ai_html = f'<div style="background:rgba(124,58,237,0.08); border:1px solid rgba(124,58,237,0.15); border-radius:10px; padding:12px 16px; margin-top:12px;"><p style="color:#a78bfa; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px; margin:0 0 6px 0;">🤖 AI Safety Assessment</p><p style="color:#c4c9e8; font-size:0.88rem; line-height:1.6; margin:0;">{route["ai_explanation"]}</p></div>'

        with st.container():
            st.markdown(f'<div class="glass-card" style="border-left: 4px solid {border_color};"><div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;"><div><p style="color:#7c83a8; font-size:0.72rem; text-transform:uppercase; letter-spacing:1.5px; margin:0 0 4px 0;">{rank} Option</p><h3 style="margin:0; font-size:1.2rem;">{route["emoji"]} {route["level"]}</h3></div><div style="display:flex; gap:24px; flex-wrap:wrap;"><div style="text-align:center;"><p style="color:#7c83a8; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; margin:0;">Distance</p><p style="color:#f0f0ff; font-weight:700; font-size:1rem; margin:0;">{route["distance_km"]} km</p></div><div style="text-align:center;"><p style="color:#7c83a8; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; margin:0;">Duration</p><p style="color:#f0f0ff; font-weight:700; font-size:1rem; margin:0;">{route["duration_min"]} min</p></div><div style="text-align:center;"><p style="color:#7c83a8; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; margin:0;">Nearby Crimes</p><p style="color:#f0f0ff; font-weight:700; font-size:1rem; margin:0;">{route["crime_count"]}</p></div><div style="text-align:center;"><p style="color:#7c83a8; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; margin:0;">High Priority</p><p style="color:{border_color}; font-weight:700; font-size:1rem; margin:0;">{route["high_priority_count"]}</p></div></div></div><div style="margin:16px 0 12px 0;"><div style="display:flex; justify-content:space-between; margin-bottom:6px;"><span style="color:#7c83a8; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px;">Risk Score</span><span style="color:{bar_color}; font-weight:700; font-size:0.85rem;">{risk_pct}/100</span></div><div style="background:rgba(255,255,255,0.06); border-radius:100px; height:8px;"><div style="background:linear-gradient(90deg, {bar_color}, rgba(255,255,255,0.4)); width:{risk_pct}%; height:8px; border-radius:100px; transition: width 1s ease;"></div></div></div>{ai_html}</div>', unsafe_allow_html=True)

    # ── Safety Tips ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("""
    <div class="glass-card">
        <h3 style="margin-top:0;">🔰 General Safety Tips</h3>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:12px;">
            <p style="color:#c4c9e8; font-size:0.85rem; margin:0;">✅ Always prefer well-lit and busy streets</p>
            <p style="color:#c4c9e8; font-size:0.85rem; margin:0;">✅ Share your route with someone you trust</p>
            <p style="color:#c4c9e8; font-size:0.85rem; margin:0;">⚠️ Avoid isolated roads at night</p>
            <p style="color:#c4c9e8; font-size:0.85rem; margin:0;">⚠️ Stay alert in areas with recent incidents</p>
            <p style="color:#c4c9e8; font-size:0.85rem; margin:0;">🚫 Do not stop in high-crime hotspot zones</p>
            <p style="color:#c4c9e8; font-size:0.85rem; margin:0;">🚫 Avoid the red-marked routes shown on map</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
