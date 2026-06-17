import math
import requests
import pandas as pd
from typing import List, Tuple, Dict

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OSRM_URL = "http://router.project-osrm.org/route/v1/driving"

def geocode_location(location_name: str) -> Tuple[float, float]:
    """Convert a place name to (lat, lon) using OpenStreetMap Nominatim."""
    try:
        resp = requests.get(NOMINATIM_URL, params={
            "q": location_name,
            "format": "json",
            "limit": 1
        }, headers={"User-Agent": "CrimeIntelligenceAgent/1.0"}, timeout=10)
        data = resp.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception as e:
        print(f"Geocoding error: {e}")
    return None, None


def get_routes_from_osrm(src_lat: float, src_lon: float,
                          dst_lat: float, dst_lon: float) -> List[Dict]:
    """Get up to 3 alternative routes from OSRM."""
    try:
        url = f"{OSRM_URL}/{src_lon},{src_lat};{dst_lon},{dst_lat}"
        params = {
            "overview": "full",
            "geometries": "geojson",
            "alternatives": "true",
            "steps": "false"
        }
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()

        routes = []
        if data.get("code") == "Ok":
            for i, route in enumerate(data.get("routes", [])):
                coords = route["geometry"]["coordinates"]
                # OSRM returns [lon, lat] — swap to [lat, lon]
                latlon_coords = [(c[1], c[0]) for c in coords]
                routes.append({
                    "index": i,
                    "coords": latlon_coords,
                    "distance_km": round(route["distance"] / 1000, 2),
                    "duration_min": round(route["duration"] / 60, 1)
                })
        return routes
    except Exception as e:
        print(f"OSRM error: {e}")
        return []


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in km between two coordinates."""
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))


def calculate_route_risk(route_coords: List[Tuple], crime_df: pd.DataFrame,
                          radius_km: float = 0.4) -> Dict:
    """
    Calculate a risk score for a route based on crime incidents within radius_km
    of any point on the route. Samples every Nth point for performance.
    """
    if crime_df.empty:
        return {"risk_score": 0, "crime_count": 0, "high_priority_count": 0}

    # Sample points (every 10th to keep it fast)
    sample_coords = route_coords[::10] if len(route_coords) > 20 else route_coords

    crime_lats = crime_df['latitude'].values
    crime_lons = crime_df['longitude'].values
    priorities = crime_df['priority'].values if 'priority' in crime_df.columns else ['Low Priority'] * len(crime_df)

    nearby_crimes = set()
    high_priority_near = 0

    for r_lat, r_lon in sample_coords:
        for i, (c_lat, c_lon) in enumerate(zip(crime_lats, crime_lons)):
            dist = haversine_distance(r_lat, r_lon, c_lat, c_lon)
            if dist <= radius_km and i not in nearby_crimes:
                nearby_crimes.add(i)
                if priorities[i] == 'High Priority':
                    high_priority_near += 1

    crime_count = len(nearby_crimes)
    raw_score = (crime_count * 2.5) + (high_priority_near * 6.0)
    
    # Exponential decay curve to map to 0-100 without hard capping early
    # raw_score of 50 -> ~63/100. raw_score of 100 -> ~86/100.
    risk_score = int(100 * (1 - math.exp(-raw_score / 50.0)))
    
    # Ensure it stays within bounds just in case
    risk_score = max(0, min(risk_score, 100))

    return {
        "risk_score": risk_score,
        "crime_count": crime_count,
        "high_priority_count": high_priority_near
    }


def classify_risk_level(risk_score: int) -> Dict:
    """Classify a numeric risk score into a level with color and label."""
    if risk_score <= 30:
        return {"level": "Safe Route",    "color": "#10b981", "emoji": "✅", "css_class": "safe"}
    elif risk_score <= 60:
        return {"level": "Moderate Route","color": "#f59e0b", "emoji": "⚠️", "css_class": "moderate"}
    else:
        return {"level": "High Risk — Avoid", "color": "#f43f5e", "emoji": "🚫", "css_class": "danger"}

def classify_patrol_utility(risk_score: int) -> Dict:
    """Classify a numeric risk score into a utility level for police patrolling."""
    if risk_score >= 70:
        return {"level": "Optimal Patrol", "color": "#3b82f6", "emoji": "🚓", "css_class": "optimal"}
    elif risk_score >= 40:
        return {"level": "Standard Patrol", "color": "#f59e0b", "emoji": "🛡️", "css_class": "standard"}
    else:
        return {"level": "Low Utility Patrol", "color": "#f43f5e", "emoji": "📉", "css_class": "low-utility"}

