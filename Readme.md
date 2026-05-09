# TalentLens AI — Intelligent Resume Screening & ATS Evaluation System

## Project Overview

TalentLens AI is an AI-powered resume screening and candidate ranking platform designed for modern technical recruitment workflows.

The system allows recruiters to:

- Upload multiple resumes (PDF/DOCX)
- Enter a Job Description (JD)
- Perform AI-based ATS evaluation
- Rank candidates automatically
- Identify matched and missing skills
- Generate shortlist/reject recommendations
- Export candidate reports as PDF

The project combines:

- MERN Stack
- FastAPI AI microservice
- Large Language Models (LLMs)
- Semantic resume analysis
- ATS-style scoring pipeline

---

# Tech Stack

## Frontend
- React.js
- Vite
- Tailwind CSS
- Axios

## Backend
- Node.js
- Express.js
- MongoDB
- JWT Authentication
- Multer File Uploads

## AI Service
- FastAPI
- Sentence Transformers
- Groq API
- Llama 3.3 70B Versatile

---

# LLM Chosen

## Model
- Llama-3.3-70B-Versatile
- Provider: Groq

## Why This Model?

The model was selected because:

- Extremely fast inference speed
- Strong reasoning capability
- Low latency for resume analysis
- Excellent structured JSON generation
- Cost-effective compared to GPT-4
- Suitable for ATS-style evaluation pipelines

---

# Agent Framework

## Architecture Style
Single-agent AI evaluation pipeline.

The AI service acts as an intelligent ATS recruiter.

---

# Agent Workflow

```text
User Uploads Resume
        ↓
Node.js Backend
        ↓
Resume Parsing
        ↓
FastAPI AI Service
        ↓
Skill Extraction
        ↓
ATS Scoring Engine
        ↓
LLM Evaluation
        ↓
Candidate Ranking
        ↓
Frontend Dashboard
```

---

# Prompt Design

The AI prompt was carefully engineered to simulate a strict ATS recruiter.

## Prompt Features

- Rubric-based scoring
- Structured JSON output
- Strict rejection logic
- Skill gap detection
- Experience relevance validation
- Domain-specific filtering

## ATS Evaluation Categories

| Category | Weight |
|---|---|
| Skills Match | 30% |
| Experience Relevance | 25% |
| Education | 15% |
| Projects | 20% |
| Communication | 10% |

---

# Strict ATS Rules

The system includes hard ATS filtering logic:

- Missing critical JD skills lowers score aggressively
- Generic resumes are penalized
- Experience mismatch reduces score
- Recommendation automatically becomes REJECT if major skills are absent
- Final score reflects actual job fit rather than generic resume quality

---

# Security Mitigations

## 1. Prompt Injection Protection

### Risk
Malicious users may try to manipulate AI behavior.

### Mitigation
- Input sanitization
- Structured JSON outputs
- Output validation
- Fixed ATS evaluation rules

---

## 2. Data Privacy / PII Protection

### Risk
Resumes contain personal data.

### Mitigation
- Local resume processing
- Sensitive data not logged
- No plaintext PII stored in prompts
- Secure backend architecture

---

## 3. API Key Exposure

### Risk
Leaking Groq or database credentials.

### Mitigation
- `.env` variables
- `.gitignore` protection
- Environment-based secret management

---

## 4. Hallucination Risk

### Risk
LLM generating unrealistic scores.

### Mitigation
- Strict ATS prompt
- Rule-based validation
- JSON schema enforcement
- Recommendation constraints

---

## 5. Unauthorized Access

### Risk
Public abuse of AI endpoints.

### Mitigation
- JWT Authentication
- API key verification
- Rate limiting with SlowAPI
- Protected routes

---

## 6. File Upload Security

### Risk
Malicious file uploads.

### Mitigation
- PDF/DOCX validation
- File size restrictions
- Upload filtering
- Secure storage handling

---

# Project Structure

```text
talentlens-ai/
│
├── client/                 # React Frontend
├── server/                 # Node.js Backend
├── ai-service/             # FastAPI AI Service
│
├── uploads/
├── embeddings/
├── chroma/
│
├── README.md
├── .env.example
└── requirements.txt
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <repo-url>
cd talentlens-ai
```

---

## 2. Install Frontend Dependencies

```bash
cd client
npm install
```

---

## 3. Install Backend Dependencies

```bash
cd ../server
npm install
```

---

## 4. Setup AI Service

```bash
cd ../ai-service

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

---

## 5. Configure Environment Variables

Create `.env` files.

### Backend `.env`

```env
MONGO_URI=
JWT_SECRET=
```

### AI Service `.env`

```env
GROQ_API_KEY=
AI_SERVICE_API_KEY=
```

---

## 6. Run Backend

```bash
cd server
npm run server
```

---

## 7. Run Frontend

```bash
cd client
npm run dev
```

---

## 8. Run AI Service

```bash
cd ai-service

source venv/bin/activate

python -m uvicorn main:app --reload --port 8001
```

---

# Features

- Multi Resume Upload
- AI ATS Scoring
- Candidate Ranking
- Skill Matching
- Missing Skill Detection
- Resume Parsing
- PDF Report Generation
- JWT Authentication
- FastAPI AI Integration
- Strict ATS Evaluation Logic

---

# Sample Output

## Example Candidate Evaluation

```json
{
  "skills_score": 6,
  "experience_score": 4,
  "education_score": 8,
  "project_score": 8,
  "communication_score": 7,
  "recommendation": "HOLD"
}
```

---

# Demo

The system supports:

- End-to-end resume screening
- Live ATS ranking
- PDF export
- Candidate recommendation workflow

---

# Future Improvements

- RAG-based candidate memory
- Interview question generation
- AI recruiter chatbot
- Resume-job semantic search
- Multi-agent recruiter pipeline
- Recruiter analytics dashboard

---

# Author

Dev Malik

---

# License

This project is developed for academic and learning purposes.