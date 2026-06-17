import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

def explain_route_safety(route_index: int, risk_score: int, risk_level: str,
                          crime_count: int, high_priority_count: int,
                          distance_km: float, duration_min: float,
                          src: str, dst: str) -> str:
    """Use Gemini AI to explain why a route is safe or unsafe."""
    prompt = f"""
You are a public safety AI analyzing a travel route in an urban area.

Route Details:
- Route: {src} → {dst}
- Route Option: #{route_index + 1}
- Distance: {distance_km} km
- Estimated Time: {duration_min} minutes
- Crime Risk Score: {risk_score}/100
- Safety Level: {risk_level}
- Total Nearby Crime Incidents: {crime_count}
- High Priority Incidents Nearby: {high_priority_count}

Write a concise 2-3 sentence safety assessment for this route.
Explain why it is classified as "{risk_level}".
Be specific about risk factors. 
If safe, mention what makes it safer.
If risky, warn about the danger clearly.
Do NOT add any markdown formatting, just plain text.
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"AI explanation error: {e}")
        err = str(e).lower()
        quota_warn = "[Gemini API Quota Exceeded] " if "quota" in err or "429" in err else ""
        if risk_score <= 30:
            return f"{quota_warn}This route passes through relatively low-crime areas with only {crime_count} reported incidents nearby. It is considered safe for travel."
        elif risk_score <= 60:
            return f"{quota_warn}This route passes near {crime_count} crime incidents including {high_priority_count} high-priority cases. Exercise caution and remain alert while traveling."
        else:
            return f"{quota_warn}This route is flagged as HIGH RISK due to {crime_count} nearby crime incidents, including {high_priority_count} high-priority cases. Avoid this route if possible."

def explain_patrol_utility(route_index: int, risk_score: int, patrol_level: str,
                          crime_count: int, high_priority_count: int,
                          distance_km: float, duration_min: float,
                          src: str, dst: str) -> str:
    """Use Gemini AI to explain why a route is good or bad for a police patrol."""
    prompt = f"""
You are a law enforcement AI analyzing a patrol route in an urban area.

Route Details:
- Route: {src} → {dst}
- Route Option: #{route_index + 1}
- Distance: {distance_km} km
- Estimated Time: {duration_min} minutes
- Crime Risk Score (Patrol Utility): {risk_score}/100
- Patrol Utility Level: {patrol_level}
- Total Nearby Crime Incidents: {crime_count}
- High Priority Incidents Nearby: {high_priority_count}

Write a concise 2-3 sentence assessment for this patrol route.
Explain why it is classified as "{patrol_level}".
If the utility is high, highlight the strategic value of patrolling this area (e.g., covering hotspots).
If the utility is low, mention that the area already has low crime or fewer high-priority targets.
Do NOT add any markdown formatting, just plain text.
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"AI explanation error: {e}")
        err = str(e).lower()
        quota_warn = "[Gemini API Quota Exceeded] " if "quota" in err or "429" in err else ""
        if risk_score >= 70:
            return f"{quota_warn}This route provides optimal patrol utility by covering {crime_count} crime incidents including {high_priority_count} high-priority cases. Highly recommended for active patrolling."
        elif risk_score >= 40:
            return f"{quota_warn}This route offers standard patrol coverage with {crime_count} nearby incidents. It provides moderate visibility in the area."
        else:
            return f"{quota_warn}This route has low patrol utility as it passes through relatively low-crime areas with only {crime_count} reported incidents. Deployment may be better utilized elsewhere."
