# AI Content Generator (LangChain + FastAPI + React)

A full-stack AI application that generates tailored social media content based on user topics and selected platforms.

## 🚀 How it Works
1. **Frontend (React):** The user enters a topic and selects a platform (LinkedIn, Instagram, etc.).
2. **Backend (FastAPI):** Receives the request and processes the prompt.
3. **AI Engine (LangChain):** Uses LangChain to structure the prompt and call the LLM (Google Gemini).
4. **Response:** The generated content is sent back and displayed on a modern "Glassmorphism" UI.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React.js, CSS3 (Glassmorphism) |
| **Backend** | FastAPI (Python) |
| **AI Framework** | LangChain |
| **LLM** | Google Gemini |

---

## 📦 Installation

### 1. Get a Google Gemini API key
Create a free key at [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Backend Setup
```bash
cd LangChain
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

Copy `.env.example` to `.env` inside the `LangChain` folder and add your key:
```
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

Run the server:
```bash
uvicorn main:app --reload
```
Backend runs at `http://localhost:8000`.

### 3. Frontend Setup
```bash
cd Frontend
npm install
npm run dev
```
Frontend runs at `http://localhost:5173`.

---

## 🌟 Features
* **Platform-Specific Tuning:** Generates different tones for LinkedIn vs. Instagram vs. Meta vs. YouTube.
* **Fast Execution:** Asynchronous API calls for quick content generation.
