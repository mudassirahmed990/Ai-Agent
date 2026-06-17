import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

def generate_summary(description: str) -> str:
    """Generates a concise and professional summary of the crime report."""
    prompt = f"""
    Create a concise, professional, one-sentence summary of the following crime report.
    Do not add extra information. Just summarize the key facts (who, what, where).
    
    Report: "{description}"
    
    Summary:
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating summary: {e}")
        if "429" in str(e) or "Quota" in str(e):
            return "Error: API Rate Limit Exceeded (Wait 1 min)."
        return "Error: Summary generation failed."
