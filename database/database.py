from .db_config import get_db_connection
from .models import CrimeReport

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            name TEXT,
            contact_no TEXT,
            witness_info TEXT,
            location TEXT,
            category TEXT,
            priority TEXT,
            summary TEXT,
            authenticity_score INTEGER,
            suspicious_status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def drop_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS reports')
    conn.commit()
    conn.close()

def insert_report(report: CrimeReport) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reports (description, latitude, longitude, status, timestamp, 
                             name, contact_no, witness_info, location,
                             category, priority, summary, authenticity_score, suspicious_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        report.description, report.latitude, report.longitude, report.status, report.timestamp,
        report.name, report.contact_no, report.witness_info, report.location,
        report.category, report.priority, report.summary, report.authenticity_score, report.suspicious_status
    ))
    conn.commit()
    report_id = cursor.lastrowid
    conn.close()
    return report_id

def get_all_reports():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reports ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_report_by_id(report_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reports WHERE id = ?', (report_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_report_status(report_id: int, new_status: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE reports SET status = ? WHERE id = ?', (new_status, report_id))
    conn.commit()
    conn.close()

def update_ai_insights(report_id: int, summary: str, authenticity_score: int, suspicious_status: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE reports 
        SET summary = ?, authenticity_score = ?, suspicious_status = ? 
        WHERE id = ?
    ''', (summary, authenticity_score, suspicious_status, report_id))
    conn.commit()
    conn.close()

def delete_report(report_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reports WHERE id = ?', (report_id,))
    conn.commit()
    conn.close()
