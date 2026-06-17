from dataclasses import dataclass
from typing import Optional

@dataclass
class CrimeReport:
    id: Optional[int]
    description: str
    latitude: float
    longitude: float
    status: str  # Pending, Confirmed
    timestamp: str
    
    # Optional CSV Fields
    name: Optional[str] = None
    contact_no: Optional[str] = None
    witness_info: Optional[str] = None
    location: Optional[str] = None
    
    # AI Generated Fields
    category: Optional[str] = None
    priority: Optional[str] = None
    summary: Optional[str] = None
    authenticity_score: Optional[int] = None
    suspicious_status: Optional[str] = None
