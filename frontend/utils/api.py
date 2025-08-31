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
    
    # Simple fallback when no search is active
    return {
        "category": "General",
        "confidence": "100%",
        "title": "Welcome to HealthFact AI",
        "summary": "Use the search bar above to discover evidence-based health information.",
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
                "title": data.get("claim", query),  # Use the original claim or query as title
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
        elif response.status_code == 401:
            st.error("🔐 Authentication required. Please log in to view progress.")
            return None
        elif response.status_code == 404:
            # User has no progress yet, return empty data
            return {
                "total_facts": 0,
                "current_streak": 0,
                "longest_streak": 0,
                "categories": {},
                "last_activity": None,
                "facts_this_week": 0
            }
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to backend. Please check if the server is running.")
        return None
    except Exception as e:
        st.error(f"❌ Error fetching progress: {e}")
        return None
    return None

def get_categories_breakdown() -> Optional[Dict]:
    """Get user's categories breakdown for charts"""
    try:
        headers = get_auth_headers()
        if not headers:
            return None
            
        response = requests.get(
            f"{API_URL}/progress/categories", 
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            # User has no categories yet
            return {"categories": {}, "total": 0}
    except Exception as e:
        st.error(f"❌ Error fetching categories: {e}")
        return None
    return None

def track_search_activity(claim: str) -> bool:
    """Track search activity in user progress"""
    try:
        headers = {"Content-Type": "application/json"}
        headers.update(get_auth_headers())
        
        if not headers.get("Authorization"):
            return False
        
        response = requests.post(
            f"{API_URL}/progress/search",
            json={"claim": claim},
            headers=headers,
            timeout=5
        )
        return response.status_code == 200
    except Exception:
        # Silently fail - progress tracking shouldn't break main functionality
        return False

def track_quiz_activity(claim: str, questions_count: int = 0) -> bool:
    """Track quiz generation activity in user progress"""
    try:
        headers = {"Content-Type": "application/json"}
        headers.update(get_auth_headers())
        
        if not headers.get("Authorization"):
            return False
        
        response = requests.post(
            f"{API_URL}/progress/quiz",
            json={"claim": claim, "questions_count": questions_count},
            headers=headers,
            timeout=5
        )
        return response.status_code == 200
    except Exception:
        # Silently fail - progress tracking shouldn't break main functionality
        return False

def track_quiz_answers(answers: List[str], correct_answers: List[str]) -> bool:
    """Track quiz answers in user progress"""
    try:
        headers = {"Content-Type": "application/json"}
        headers.update(get_auth_headers())
        
        if not headers.get("Authorization"):
            return False
        
        response = requests.post(
            f"{API_URL}/progress/quiz_answers",
            json={"answers": answers, "correct_answers": correct_answers},
            headers=headers,
            timeout=5
        )
        return response.status_code == 200
    except Exception:
        # Silently fail - progress tracking shouldn't break main functionality
        return False

def generate_quiz(claim: str) -> Optional[Dict]:
    """Generate a quiz from a health claim"""
    try:
        headers = {"Content-Type": "application/json"}
        headers.update(get_auth_headers())
        
        response = requests.post(
            f"{API_URL}/quiz/generate",
            json={"claim": claim},
            headers=headers,
            timeout=60  # Increased timeout for quiz generation
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

def save_fact_card(search_query: str, search_result: Dict) -> bool:
    """Save a search result as a fact card"""
    try:
        headers = {"Content-Type": "application/json"}
        headers.update(get_auth_headers())
        
        if not headers.get("Authorization"):
            return False
        
        response = requests.post(
            f"{API_URL}/fact-cards/save",
            json={"search_query": search_query, "search_result": search_result},
            headers=headers,
            timeout=5
        )
        return response.status_code == 200
    except Exception:
        # Silently fail - fact card saving shouldn't break main functionality
        return False

def get_user_fact_cards(category: str = "All", limit: int = 20, offset: int = 0) -> Optional[Dict]:
    """Get user's saved fact cards"""
    try:
        headers = get_auth_headers()
        if not headers:
            return None
        
        params = {"category": category, "limit": limit, "offset": offset}
        response = requests.get(
            f"{API_URL}/fact-cards/",
            headers=headers,
            params=params,
            timeout=30  # Increased timeout for database operations
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.error("🔐 Authentication required. Please log in to view fact cards.")
            return None
    except Exception as e:
        st.error(f"❌ Error fetching fact cards: {e}")
        return None
    return None

def get_fact_card_categories() -> List[str]:
    """Get all categories that have fact cards for the user"""
    try:
        headers = get_auth_headers()
        if not headers:
            return ["All"]
        
        response = requests.get(
            f"{API_URL}/fact-cards/categories",
            headers=headers,
            timeout=30  # Increased timeout for database operations
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("categories", ["All"])
    except Exception:
        pass
    return ["All"]

def search_fact_cards(query: str, category: Optional[str] = None, limit: int = 20) -> Optional[List[Dict]]:
    """Search user's fact cards"""
    try:
        headers = get_auth_headers()
        if not headers:
            return None
        
        params = {"q": query, "limit": limit}
        if category:
            params["category"] = category
        
        response = requests.get(
            f"{API_URL}/fact-cards/search",
            headers=headers,
            params=params,
            timeout=30  # Increased timeout for database operations
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("fact_cards", [])
    except Exception as e:
        st.error(f"❌ Error searching fact cards: {e}")
        return None
    return None

def delete_fact_card(fact_card_id: int) -> bool:
    """Delete a fact card"""
    try:
        headers = get_auth_headers()
        if not headers:
            return False
        
        response = requests.delete(
            f"{API_URL}/fact-cards/{fact_card_id}",
            headers=headers,
            timeout=15  # Reasonable timeout for delete operations
        )
        return response.status_code == 200
    except Exception:
        return False
