import requests
from typing import Dict, List, Optional
from config import API_URL

def fetch_featured_fact(query: str = "") -> Dict:
    """Fetch a featured health fact from the backend"""
    try:
        if query:
            response = requests.get(f"{API_URL}/search", params={"q": query}, timeout=2)
            if response.status_code == 200:
                return response.json()
    except Exception:
        pass
    
    # Fallback to default fact if API is unavailable
    return {
        "category": "Nutrition",
        "confidence": "92%",
        "title": "The Power of Mediterranean Diet on Brain Health",
        "summary": (
            "Research shows that following a Mediterranean diet rich in olive oil, fish, nuts, "
            "and vegetables can reduce the risk of cognitive decline by up to 35%. The omega-3 "
            "fatty acids and antioxidants in these foods help protect brain cells and improve memory function."
        ),
        "sources": [
            {"name": "Harvard Health", "url": "https://www.health.harvard.edu/"},
            {"name": "Mayo Clinic", "url": "https://www.mayoclinic.org/"},
            {"name": "Nature Medicine", "url": "https://www.nature.com/nm/"},
        ],
    }

def check_health_claim(claim: str) -> Optional[Dict]:
    """Check a health claim against the backend"""
    try:
        response = requests.post(f"{API_URL}/check_claim", json={"claim": claim}, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None

def fetch_quiz_questions() -> Optional[List[Dict]]:
    """Fetch quiz questions from the backend"""
    try:
        response = requests.get(f"{API_URL}/quiz", timeout=10)
        if response.status_code == 200:
            return response.json().get("questions", [])
    except Exception:
        pass
    return None

def submit_claim(claim_data: Dict) -> bool:
    """Submit a new claim to the backend"""
    try:
        response = requests.post(f"{API_URL}/claims", json=claim_data, timeout=3)
        return response.status_code == 200
    except Exception:
        return False

def update_claim(claim_id: int, claim_data: Dict) -> bool:
    """Update an existing claim in the backend"""
    try:
        response = requests.put(f"{API_URL}/claims/{claim_id}", json=claim_data, timeout=3)
        return response.status_code == 200
    except Exception:
        return False

def is_backend_available() -> bool:
    """Check if the backend API is available"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except Exception:
        return False
