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
    
    # Fallback message if API is unavailable
    return {
        "category": "General",
        "confidence": "100%",
        "title": "Ready to Learn",
        "summary": "Start searching to know more about health and wellness topics.",
        "sources": [],
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

def get_auth_headers() -> Dict[str, str]:
    """Get authentication headers from session state"""
    token = st.session_state.get("access_token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def search_health_claims(query: str) -> Optional[List[Dict]]:
    """Search for health claims and return results in fact card format"""
    try:
        headers = {"Content-Type": "application/json"}
        headers.update(get_auth_headers())
        
        response = requests.post(
            f"{API_URL}/search/verify", 
            json={"claim": query}, 
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Convert to fact card format
            fact_card = {
                "title": f"Search: {query}",
                "summary": data.get("explanation", "No explanation available"),
                "category": "Health Research",
                "confidence": f"{int(data.get('confidence', 0) * 100)}%",
                "sources": [
                    {
                        "name": source.get("title", "Source"),
                        "url": source.get("url", "#")
                    } for source in data.get("sources", [])
                ]
            }
            
            return [fact_card]
        elif response.status_code == 401:
            st.error("🔐 Authentication required. Please log in to search.")
            return None
        elif response.status_code == 404:
            st.error("🔍 Search endpoint not found. Please check your backend configuration.")
            return None
        elif response.status_code >= 500:
            st.error("🚨 Backend server error. Please try again later.")
            return None
        else:
            st.error(f"Search failed: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("⏰ Search timed out. Please try again.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to backend. Please check if the server is running.")
        return None
    except Exception as e:
        st.error(f"❌ Error searching claims: {e}")
        return None

def get_user_progress() -> Optional[Dict]:
    """Get user's progress data"""
    try:
        headers = get_auth_headers()
        if not headers:
            return None
            
        response = requests.get(
            f"{API_URL}/progress/", 
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
            f"{API_URL}/quiz/generate",
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
            f"{API_URL}/quiz/submit",
            json={"quiz_id": quiz_id, "answers": answers},
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error submitting quiz: {e}")
    return None
