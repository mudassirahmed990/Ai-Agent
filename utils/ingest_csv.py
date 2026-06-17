import sys
import os
import pandas as pd

# Add parent directory to path so we can import from database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import init_db, drop_db, insert_report
from database.models import CrimeReport

def ingest_data(csv_file_path="crime_data.csv"):
    if not os.path.exists(csv_file_path):
        print(f"Error: {csv_file_path} not found.")
        return

    print("Re-initializing database...")
    drop_db()
    init_db()
    
    print(f"Reading {csv_file_path}...")
    df = pd.read_csv(csv_file_path)
    
    # Optional mapping for Intensity Level to Priority
    intensity_to_priority = {
        "High": "High Priority",
        "Critical": "High Priority",
        "Medium": "Medium Priority",
        "Low": "Low Priority"
    }

    print(f"Ingesting {len(df)} records...")
    for index, row in df.iterrows():
        # Map fields
        intensity = str(row.get('Intensity_Level', 'Medium'))
        priority = intensity_to_priority.get(intensity, "Medium Priority")
        
        report = CrimeReport(
            id=None,
            description=str(row.get('Description', '')),
            latitude=float(row.get('Latitude', 0.0)),
            longitude=float(row.get('Longitude', 0.0)),
            status="Pending",
            timestamp=str(row.get('Timestamp', '')),
            name=str(row.get('Name', '')),
            contact_no=str(row.get('Contact_No', '')),
            witness_info=str(row.get('Witness_Info', '[]')),
            location=str(row.get('Location', '')),
            category=str(row.get('Crime_Type', 'Other')),
            priority=priority,
            # Leave these blank for on-demand generation
            summary=None,
            authenticity_score=None,
            suspicious_status=None
        )
        insert_report(report)
        
    print("Ingestion complete.")

if __name__ == "__main__":
    ingest_data()
