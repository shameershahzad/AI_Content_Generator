# AI Content Generator (LangChain + FastAPI + React)

A full-stack AI application that generates tailored social media content based on user topics and selected platforms.

## 🚀 How it Works
1. **Frontend (React):** The user enters a topic and selects a platform (LinkedIn, Instagram, etc.).
2. **Backend (FastAPI):** Receives the request and processes the prompt.
3. **AI Engine (LangChain):** Uses LangChain to structure the prompt and call the LLM (Large Language Model).
4. **Response:** The generated content is sent back and displayed on a modern "Glassmorphism" UI.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React.js, CSS3 (Glassmorphism) |
| **Backend** | FastAPI (Python) |
| **AI Framework** | LangChain |
| **LLM** | OpenAI / Google Gemini |

---

## 📦 Installation

### Backend Setup
1. Navigate to the backend folder: `cd backend`
2. Create a virtual environment: `python -m venv .venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the server: `uvicorn main:app --reload`

### Frontend Setup
1. Navigate to the frontend folder: `cd frontend`
2. Install packages: `npm install`
3. Start the app: `npm start`

---

## 🌟 Features
* **Platform-Specific Tuning:** Generates different tones for LinkedIn vs. Instagram vs. Meta vs. Youtube.
* **Fast Execution:** Asynchronous API calls for quick content generation.
