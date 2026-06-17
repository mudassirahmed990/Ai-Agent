import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from utils.helpers import parse_ai_json_response

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

def detect_fake_report(description: str) -> dict:
    """Analyzes a report and estimates authenticity."""
    prompt = f"""
    Analyze the following crime report for authenticity, logical consistency, and spam-like patterns.
    Provide an authenticity score (0-100) and a status of either 'Suspicious' or 'Not Suspicious'.
    
    Report: "{description}"
    
    Respond STRICTLY in the following JSON format:
    {{
        "confidence_score": <integer 0-100>,
        "authenticity_score": <integer 0-100>,
        "suspicious_status": "<'Suspicious' or 'Not Suspicious'>"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        result = parse_ai_json_response(response.text)
        if not result:
            raise ValueError("Failed to parse JSON")
            
        return {
            "confidence_score": result.get("confidence_score", 50),
            "authenticity_score": result.get("authenticity_score", 50),
            "suspicious_status": result.get("suspicious_status", "Suspicious")
        }
    except Exception as e:
        print(f"Error detecting fake report: {e}")
        if "429" in str(e) or "Quota" in str(e):
            return {"error": "API Rate Limit Exceeded"}
        return {"error": "Detection generation failed"}
