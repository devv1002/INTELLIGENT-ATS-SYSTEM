# TalentLens AI — AI-Powered Resume Screening & Candidate Ranking System

TalentLens AI is an intelligent ATS-style resume screening platform that evaluates resumes against job descriptions using LLM-powered analysis, semantic understanding, skill extraction, and rubric-based AI scoring.

The platform helps recruiters automatically:
- Screen resumes
- Match candidates with job descriptions
- Rank applicants intelligently
- Detect missing skills
- Generate ATS-style evaluations
- Produce recruiter-ready reports

---

# Features

- AI Resume Parsing
- ATS-Style Candidate Evaluation
- Resume vs JD Matching
- Semantic Skill Analysis
- AI-Powered Scoring Engine
- Candidate Ranking System
- PDF Report Generation
- Recruiter Workflow UI
- Vector Embedding Storage
- FastAPI + React Full Stack Architecture

---

# Tech Stack

## Frontend
- React.js
- Tailwind CSS
- Axios
- jsPDF

## Backend
- FastAPI
- Python
- Node.js / Express
- Multer

## AI / ML Stack
- Groq API
- Llama 3.3 70B Versatile
- Sentence Transformers
- ChromaDB
- Semantic Embeddings

---

# System Architecture

User → React Frontend → Express Upload API → FastAPI AI Engine → Groq LLM + Embedding Models → ChromaDB → Ranked Results → Frontend Dashboard

---

# Project Workflow

1. Recruiter enters Job Description
2. Recruiter uploads resumes
3. Backend parses resumes
4. Skills are extracted
5. Embeddings are generated
6. Resume vectors stored in ChromaDB
7. LLM evaluates resume against JD
8. AI scoring engine calculates rubric scores
9. Candidates ranked by final ATS score
10. Frontend displays recruiter dashboard

---

# Mandatory Technical Disclosures



---

# 1. LLM Chosen

## Model
- Llama 3.3 70B Versatile

## Provider
- Groq

## Why This Model?

The project uses Groq-hosted Llama 3.3 70B because:

### Advantages
- Extremely fast inference
- Large context handling
- Strong reasoning capabilities
- High-quality JSON generation
- Cost-effective compared to GPT-4
- Reliable ATS-style resume analysis
- Good prompt adherence

### Why Not Alternatives?

| Model | Reason Not Selected |
|---|---|
| GPT-4 | Higher cost |
| Gemini | Less consistent JSON formatting |
| Claude | Slower API response |
| Local LLMs | Limited compute resources |

---

# 2. Agent Framework

## Framework Used
- FastAPI-based modular AI pipeline

## Architecture Style
- Plan-and-execute pipeline
- Modular service architecture

## Internal AI Flow

Resume Upload
↓
Resume Parsing
↓
Skill Extraction
↓
Embedding Generation
↓
Vector Storage
↓
LLM Evaluation
↓
Rubric Scoring
↓
Candidate Ranking
↓
Frontend Dashboard

## Modules

| Module | Responsibility |
|---|---|
| parsers | Resume text extraction |
| embeddings | Semantic vector generation |
| chroma | Vector DB storage |
| services/ai_scorer.py | AI ATS scoring |
| services/groq_analyzer.py | Resume analysis |
| matcher.py | Similarity calculations |

---

# 3. Prompt Design

The project uses strict ATS-style prompts to ensure realistic recruiter evaluation.

## Prompt Goals

- Strict JD-resume matching
- Technology relevance validation
- Missing skill detection
- ATS-style evaluation
- JSON-safe structured output
- Rubric-based scoring

## Prompt Engineering Strategy

### Guardrails Applied
- Scores restricted to 0-10
- Forced JSON output
- Strict JD relevance enforcement
- Hallucination reduction instructions
- Conservative scoring policy
- Technology mismatch penalties

### Evaluation Dimensions
- Skills Match
- Experience Relevance
- Education & Certifications
- Projects & Portfolio
- Communication Quality

### AI Behavior Rules
- Missing JD skills reduce score
- Irrelevant projects reduce score
- Generic resumes do not receive high scores
- Production-level projects improve score

---

# 4. Security Mitigations

The system includes several security-focused design decisions.

## File Upload Security
- Restricted file types
- PDF/DOC/DOCX validation
- Multer upload middleware
- Controlled upload directory

## Environment Security
- API keys stored in `.env`
- No secrets exposed to frontend

## Prompt Injection Mitigation
- Structured prompts
- Restricted output format
- JSON-only response enforcement

## Backend Security
- CORS protection
- Request validation using Pydantic
- Controlled API routes

## Data Protection
- No permanent sensitive resume storage
- Vector embeddings stored locally
- Minimal logging

---

# AI Scoring Rubric

| Dimension | Weight |
|---|---|
| Skills Match | 30% |
| Experience Relevance | 25% |
| Education & Certifications | 15% |
| Projects & Portfolio | 20% |
| Communication Quality | 10% |

---

# Final Score Formula

```python
final_score =
(skills_score * 0.30) +
(experience_score * 0.25) +
(education_score * 0.15) +
(project_score * 0.20) +
(communication_score * 0.10)
```

---

# API Endpoints

## Analyze Resume

```http
POST /analyze-resume
```

### Request
```json
{
  "job_description": "...",
  "resume_paths": []
}
```

---

# Folder Structure

```bash
talentlens-ai/
│
├── ai-service/
│   ├── chroma/
│   ├── embeddings/
│   ├── parsers/
│   ├── services/
│   ├── main.py
│
├── client/
│   ├── src/
│
├── server/
│   ├── uploads/
```

---

# Future Improvements

- Multi-agent recruiter workflow
- AI interview generation
- Candidate chat assistant
- Recruiter analytics dashboard
- Resume improvement suggestions
- Email automation
- Job recommendation engine
- Fine-tuned ATS model
- Redis queue pipeline
- Docker deployment

---

# Installation

## Backend

```bash
cd ai-service

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload --port 8001
```

## Frontend

```bash
cd client

npm install

npm run dev
```

---

# Environment Variables

```env
GROQ_API_KEY=your_api_key
```

---

# Author

Dev Malik

AI Engineer | Full Stack Developer | AI Systems Builder
