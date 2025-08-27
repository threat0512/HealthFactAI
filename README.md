 🧠 HealthFact AI

HealthFact AI is a fact-checking and learning platform designed to fight health misinformation.  
Users can check claims, play quizzes, and learn simple tips for spotting false health advice.  

---

🚀 Features

 ✅ Core Features (MVP)
- **Claim Checker**  
  - Input a health claim → get verdict (`True/False`) + explanation + trusted source.  
  - Uses FastAPI backend, NLP rules (spaCy + regex), and limited web scraping.

- **Quiz / Game Mode**  
  - 5–10 quiz questions per session.  
  - Tracks score locally.  
  - Shows learning tips after each answer.

- **Learning Tips (MIL Framework)**  
  - Short, practical cards after fact-check/quiz.  
  - Example: “Always check if the claim links to WHO or CDC.”

 ⏳ Advanced (Future)
- User login + progress tracking  
- Dashboard with charts (progress over time)  
- Admin panel to add/update misinformation claims  
- Multilingual support (English/Hindi)  
- AI-powered classification (Hugging Face Transformers)

---

 🛠️ Tech Stack

- **FastAPI** → API backend (fast, auto-docs, async support)  
- **Streamlit** → UI for claim checker, quiz, dashboard  
- **SQLite** → lightweight DB for claims + quiz bank  
- **spaCy + Regex** → language processing & pattern matching  
- **Requests + BeautifulSoup4** → scrape trusted sources (WHO, CDC, etc.)  
- *(Later: Django + PostgreSQL for advanced features)*  

---
📜 License

MIT License © 2025 HealthFact AI Team

---
