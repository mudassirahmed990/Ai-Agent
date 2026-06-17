import json

def parse_ai_json_response(response_text: str) -> dict:
    """Safely parse JSON from Gemini's response, handling potential markdown wrappers."""
    try:
        # Remove potential markdown code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
            
        return json.loads(response_text)
    except Exception as e:
        print(f"Error parsing JSON: {e}\nRaw Response: {response_text}")
        return {}
