# AI Chat Assistant API

A production-ready **FastAPI-based REST API** that allows users to register, authenticate using JWT, and interact with an AI assistant.  
The application includes persistent chat history, automated testing, CI/CD, and a live deployment.

---

## 🚀 Features

- User registration and login with **JWT authentication**
- Secure password hashing using **bcrypt**
- AI-powered chat endpoint using an external **LLM API**
- Chat history stored in **SQLite**
- Users can access **only their own data**
- Graceful fallback if LLM API fails
- Automated testing with **pytest**
- Code quality checks using **flake8**
- Continuous Integration using **GitHub Actions**
- Live deployment on **Render**

---

## 🛠️ Tech Stack

- **Backend Framework:** FastAPI  
- **Database:** SQLite + SQLAlchemy  
- **Authentication:** JWT  
- **Password Security:** argon2  
- **LLM Integration:** External LLM API  
- **Testing:** pytest, pytest-cov  
- **Linting:** flake8  
- **CI/CD:** GitHub Actions  
- **Deployment:** Render (free tier)

---

## 📁 Project Structure

```
Ai_chat_assistant_api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth/
│   ├── chat/
│   └── core/
├── tests/
├── .github/workflows/ci.yml
├── .env.example
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔐 Authentication Flow

1. User registers with username, email, and password
2. Password is hashed and stored securely
3. User logs in with valid credentials
4. API returns a **JWT access token (1-hour expiry)**
5. Token is required for all chat endpoints

---

## 📡 API Endpoints

### Register
`POST /api/auth/register`

### Login
`POST /api/auth/login`

### Chat (JWT Required)
- `POST /api/chat`
- `GET /api/chat/history`
- `GET /api/chat/{chat_id}`
- `DELETE /api/chat/{chat_id}`

---

## 🧪 Testing & Verification

### Setup

```bash
python -m venv venv
#Linux
source venv/bin/activate 

#Windows
venv\scripts\activate.bat
pip install -r requirements.txt
```

### Environment Variables

```env
SECRET_KEY=your-secret-key
LLM_API_KEY=your-llm-api-key
```

### Run App

```bash
uvicorn app.main:app --reload
```

### Run Tests

```bash
pytest --cov=app
```

### Lint

```bash
flake8 app
```

---

## 🔁 CI/CD

- Runs on every push / PR to main
- Executes linting and tests
- Enforced via GitHub Actions

---

## 🌐 Deployment

- Hosted on Render (free tier)
- HTTPS via Cloudflare
- Cold starts possible after inactivity
https://ai-chat-assistant-api.onrender.com/
---


## 📄 License

For evaluation and learning purposes.

