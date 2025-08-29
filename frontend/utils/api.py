import requests
from typing import Dict, List, Optional
from config import API_URL
import streamlit as st

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
        response = requests.get(f"{API_URL}/api/v1/health", timeout=2)
        return response.status_code == 200
    except Exception:
        return False

def get_auth_headers() -> Dict[str, str]:
    """Get authentication headers from session state"""
    token = st.session_state.get("access_token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def search_and_verify_claim(claim: str) -> Optional[Dict]:
    """Search and verify a health claim using the new API"""
    try:
        headers = {"Content-Type": "application/json"}
        headers.update(get_auth_headers())
        
        response = requests.post(
            f"{API_URL}/api/v1/search/verify", 
            json={"claim": claim}, 
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error searching claim: {e}")
    return None

def get_user_progress() -> Optional[Dict]:
    """Get user's progress data"""
    try:
        headers = get_auth_headers()
        if not headers:
            return None
            
        response = requests.get(
            f"{API_URL}/api/v1/progress/", 
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error fetching progress: {e}")
    return None

def generate_quiz(claim: str) -> Optional[Dict]:
    """Generate a quiz from a health claim"""
    try:
        headers = {"Content-Type": "application/json"}
        headers.update(get_auth_headers())
        
        response = requests.post(
            f"{API_URL}/api/v1/quiz/generate",
            json={"claim": claim},
            headers=headers,
            timeout=15
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error generating quiz: {e}")
    return None

def submit_quiz_answers(quiz_id: str, answers: List[str]) -> Optional[Dict]:
    """Submit quiz answers for grading"""
    try:
        headers = {"Content-Type": "application/json"}
        headers.update(get_auth_headers())
        
        response = requests.post(
            f"{API_URL}/api/v1/quiz/submit",
            json={"quiz_id": quiz_id, "answers": answers},
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error submitting quiz: {e}")
    return None
