import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import pandas as pd

def render_hotspot_map(df: pd.DataFrame):
    if df.empty:
        m = folium.Map(location=[0, 0], zoom_start=2, tiles="CartoDB dark_matter")
        st_folium(m, width="100%", height=480, returned_objects=[])
        return

    center_lat = df['latitude'].mean()
    center_lon = df['longitude'].mean()

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles="CartoDB dark_matter"
    )

    # Heatmap layer
    heat_data = [[row['latitude'], row['longitude']] for _, row in df.iterrows()]
    HeatMap(heat_data, radius=18, blur=22, max_zoom=1,
            gradient={'0.3': '#7c3aed', '0.6': '#06b6d4', '1.0': '#f43f5e'}).add_to(m)

    # Individual markers
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
            radius=4,
            popup=folium.Popup(
                f"<b>{row.get('category','Crime')}</b><br>{row.get('location','')}<br>{p}",
                max_width=200
            ),
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.75,
            weight=1
        ).add_to(m)

    st_folium(m, width="100%", height=480, returned_objects=[])
