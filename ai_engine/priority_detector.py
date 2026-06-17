import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

def detect_priority(description: str) -> str:
    """Detects priority level from report description."""
    prompt = f"""
    Analyze the threat level, violence indicators, severity, public safety risk, and urgency of the following crime report.
    Classify it into EXACTLY ONE of the following priorities:
    - High Priority
    - Medium Priority
    - Low Priority
    
    Report: "{description}"
    
    Respond with ONLY the priority name. No other text.
    """
    
    try:
        response = model.generate_content(prompt)
        priority = response.text.strip()
        
        valid_priorities = ["High Priority", "Medium Priority", "Low Priority"]
        if priority not in valid_priorities:
            if "High" in priority: return "High Priority"
            if "Low" in priority: return "Low Priority"
            return "Medium Priority"
            
        return priority
    except Exception as e:
        print(f"Error detecting priority: {e}")
        return "Medium Priority"
