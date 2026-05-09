from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from parsers.resume_parser import parse_resume
from embeddings.embedder import generate_embedding

from chroma.vector_store import (
    store_resume_embedding,
)

from services.skill_extractor import (
    extract_skills,
)

from services.groq_analyzer import analyze_resume
from services.matcher import calculate_similarity


app = FastAPI()


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# REQUEST MODEL
class JDRequest(BaseModel):
    job_description: str


@app.get("/")
def root():

    return {
        "message": "TalentLens AI Service Running"
    }


# AI RESUME ANALYSIS
@app.post("/analyze-resume")
def analyze_resume_api(data: JDRequest):

    # JOB DESCRIPTION FROM FRONTEND
    job_description = data.job_description

    # RESUME FILE PATH
    file_path = "../server/uploads/1778312489131-771821297.pdf"

    # PARSE RESUME
    resume_text = parse_resume(file_path)

    # EXTRACT SKILLS
    resume_skills = extract_skills(
        resume_text
    )

    jd_skills = extract_skills(
        job_description
    )

    # MATCHED SKILLS
    matched_skills = list(
        set(resume_skills) &
        set(jd_skills)
    )

    # MISSING SKILLS
    missing_skills = list(
        set(jd_skills) -
        set(resume_skills)
    )

    # GENERATE RESUME EMBEDDING
    resume_embedding = generate_embedding(
        resume_text
    )

    # GENERATE JD EMBEDDING
    jd_embedding = generate_embedding(
        job_description
    )

    # STORE VECTOR
    store_resume_embedding(
        candidate_id="candidate_1",
        embedding=resume_embedding,
        resume_text=resume_text
    )

    # SEMANTIC SCORE
    semantic_score = calculate_similarity(
        resume_embedding,
        jd_embedding
    )

    # SKILL SCORE
    skill_score = (
        len(matched_skills) /
        len(jd_skills)
    ) * 100 if jd_skills else 0

    # FINAL HYBRID SCORE
    match_score = round(
        (semantic_score * 0.7) +
        (skill_score * 0.3),
        2
    )

    # AI ANALYSIS
    analysis = analyze_resume(
        resume_text
    )

    return {
        "success": True,

        "analysis": analysis,

        "match_score": f"{match_score}%",

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,
    }

# OPTIONAL TEST ROUTE
@app.get("/match-resume")
def match_resume():

    job_description = """
    Looking for AI Engineer with NLP,
    RAG, Python, FastAPI,
    and Vector Database experience.
    """

    file_path = "../server/uploads/1778312489131-771821297.pdf"

    resume_text = parse_resume(file_path)

    resume_embedding = generate_embedding(
        resume_text
    )

    jd_embedding = generate_embedding(
        job_description
    )

    match_score = calculate_similarity(
        resume_embedding,
        jd_embedding
    )

    return {
        "success": True,
        "match_score": f"{match_score}%",

        "job_description": job_description
    }