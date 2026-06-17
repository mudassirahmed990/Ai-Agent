import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

def classify_crime(description: str) -> str:
    """Classifies a crime report into predefined categories."""
    prompt = f"""
    Analyze the following crime report and classify it into EXACTLY ONE of the following categories:
    - Theft
    - Robbery
    - Snatching
    - Kidnapping
    - Assault
    - Harassment
    - Accident
    - Drug Activity
    - Vandalism
    - Other
    
    Report: "{description}"
    
    Respond with ONLY the category name. No other text.
    """
    
    try:
        response = model.generate_content(prompt)
        category = response.text.strip()
        # Fallback validation
        valid_categories = ["Theft", "Robbery", "Snatching", "Kidnapping", "Assault", 
                            "Harassment", "Accident", "Drug Activity", "Vandalism", "Other"]
        if category not in valid_categories:
            return "Other"
        return category
    except Exception as e:
        print(f"Error classifying crime: {e}")
        return "Other"
