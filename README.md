# AI Crime Intelligence Agent

This project transforms a traditional Crime Reporting System into an AI-powered Crime Intelligence Agent using Streamlit and Google Gemini AI.

## Features
1. **Crime Classification:** Automatically categorize reports (e.g., Theft, Robbery, Assault).
2. **Priority Detection:** Determine High/Medium/Low priority based on threat levels.
3. **Auto Summary Generation:** Generate concise summaries for every report.
4. **Fake Report Detection:** Analyze reports to estimate authenticity and give a confidence score.
5. **Crime Hotspot Prediction:** Analyze crime density and highlight high-risk areas on a map.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `streamlit run app.py`

## Architecture
- Built with Streamlit for a modern, responsive UI.
- Uses SQLite for local database persistence.
- Google Gemini AI integration for all intelligence features.
