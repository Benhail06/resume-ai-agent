🚀 Resume AI Agent
An AI-powered resume evaluation system that analyzes candidate resumes against job descriptions using LLM-based skill extraction and deterministic matching logic.
🔗 Live App: https://resume-ai-agent-dkznxmfoaphmc5qbogriev.streamlit.app
📌 Overview
Resume AI Agent is a cloud-deployed Streamlit application that:
Extracts structured skills from resumes (PDF input)
Analyzes job descriptions
Calculates skill match percentage
Identifies missing skills
Generates AI-based career recommendations
Produces likely interview questions
The system combines LLM reasoning with deterministic scoring logic for explainable and stable evaluation.
🧠 Architecture
1️⃣ Input Layer
Upload Resume (PDF)
Paste Job Description
2️⃣ Extraction Layer
PDF → Text (PyPDF)
LLM → Structured skill extraction
LLM → JD requirement extraction
3️⃣ Matching Layer
Skill normalization
Partial string matching logic
Match percentage calculation
Missing skill detection
4️⃣ Intelligence Layer
AI-generated improvement suggestions
Learning recommendations
Interview question generation
5️⃣ Presentation Layer
Streamlit UI
Progress bar visualization
Secure API key handling via secrets
Robust fallback handling for LLM formatting issues
⚙️ Tech Stack
Python
Streamlit
Groq LLM API
PyPDF
Scikit-learn (initial similarity experiments)
Deterministic skill-matching logic
🔐 Secure API Handling
The application uses:
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.getenv("GROQ_API_KEY")
This ensures:
Secure cloud deployment via Streamlit secrets
Local development support via environment variables
🧮 Matching Logic
Match Score =
(Matched Required Skills / Total Required Skills) × 100
Uses partial string matching for improved alignment between resume and job description terminology.
🚀 Deployment
Deployed on Streamlit Community Cloud.
To run locally:
export GROQ_API_KEY="your_api_key"
python -m streamlit run app.py
📈 Future Improvements
Embedding-based semantic similarity scoring
Resume ranking system for recruiters
Multi-resume batch processing
Database integration for persistent storage
Analytics dashboard for HR use case
💡 Why This Project
This project demonstrates:
LLM orchestration
Prompt engineering
Deterministic scoring systems
Secure API handling
Real-world deployment
Robust error handling
It reflects a production-oriented AI engineering mindset rather than a simple demo application.
👨‍💻 Author
Built by Ben
Aspiring AI Engineer | Machine Learning Enthusiast | Builder


