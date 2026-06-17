import pandas as pd

def get_hotspot_statistics(df: pd.DataFrame) -> dict:
    """Generates statistics for hotspot prediction based on the data."""
    if df.empty:
        return {
            "total_reports": 0,
            "high_risk_areas": 0,
            "most_common_crime": "N/A"
        }
        
    total_reports = len(df)
    high_risk_areas = len(df[df['priority'] == 'High Priority'])
    most_common_crime = df['category'].mode()[0] if not df['category'].empty else "N/A"
    
    return {
        "total_reports": total_reports,
        "high_risk_areas": high_risk_areas,
        "most_common_crime": most_common_crime
    }
