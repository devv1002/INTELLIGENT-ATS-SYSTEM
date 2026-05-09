from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import Depends
from middleware.auth import verify_api_key
from slowapi import Limiter
from slowapi.util import get_remote_address

from services.ai_scorer import (
    ai_resume_scorer,
)

import os

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

from services.security import (

    sanitize_input,

    mask_sensitive_data
)


app = FastAPI()

limiter = Limiter(
    key_func=get_remote_address
)

app.state.limiter = limiter

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
    resume_paths: list[str]


@app.get("/")
def root():

    return {
        "message": "TalentLens AI Service Running"
    }


from pydantic import BaseModel

class ResumeRequest(BaseModel):

    resume_paths: list[str]

    job_description: str

@limiter.limit("5/minute")
# AI RESUME ANALYSIS
@app.post(
    "/analyze-resume",
    dependencies=[Depends(
        verify_api_key
    )]
)
async def analyze_resume_api(
    request: Request,
    data: ResumeRequest
):

    job_description = data.job_description

    resume_paths = data.resume_paths

    ranked_candidates = []

    # JD SKILLS
    jd_skills = extract_skills(
        job_description
    )

    # JD EMBEDDING
    jd_embedding = generate_embedding(
        job_description
    )

    for resume_path in resume_paths:

        try:

            # PARSE RESUME
            absolute_resume_path = os.path.abspath(
                f"../server/{resume_path}"
            )

            print("READING FILE:", absolute_resume_path)

            resume_text = parse_resume(
                absolute_resume_path
            )

            # SANITIZE INPUTS
            resume_text = sanitize_input(
                resume_text
            )

            job_description = sanitize_input(
                job_description
            )

            # EXTRACT SKILLS
            resume_skills = extract_skills(
                resume_text
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

            # RESUME EMBEDDING
            resume_embedding = generate_embedding(
                resume_text
            )

            # STORE VECTOR
            store_resume_embedding(
                candidate_id=resume_path,
                embedding=resume_embedding,
                resume_text=resume_text
            )

            # =========================
            # SEMANTIC SCORE
            # =========================
            semantic_score = calculate_similarity(
                resume_embedding,
                jd_embedding
            )

            # =========================
            # SKILLS SCORE
            # =========================
            skills_score = (
                len(matched_skills) /
                len(jd_skills)
            ) * 100 if jd_skills else 0

            # =========================
            # EXPERIENCE SCORE
            # =========================
            # REAL AI RUBRIC SCORING
            ai_scores = ai_resume_scorer(
                resume_text,
                job_description
            )

            skills_score = ai_scores["skills_score"]

            experience_score = ai_scores["experience_score"]

            education_score = ai_scores["education_score"]

            project_score = ai_scores["project_score"]

            communication_score = ai_scores["communication_score"]

            recommendation = ai_scores["recommendation"]

            summary = ai_scores["summary"]

            # =========================
            # FINAL RUBRIC SCORE
            # =========================
            final_score = round(

                (
                    (skills_score * 30) +

                    (experience_score * 25) +

                    (education_score * 15) +

                    (project_score * 20) +

                    (communication_score * 10)

                ) / 10,

                2
            )

            # =========================
            # RECOMMENDATION
            # =========================
            if final_score >= 80:

                recommendation = "SHORTLIST"

            elif final_score >= 60:

                recommendation = "HOLD"

            else:

                recommendation = "REJECT"

            # =========================
            # AI ANALYSIS
            # =========================
            safe_resume_text = mask_sensitive_data(
                resume_text
            )

            analysis = analyze_resume(
                safe_resume_text
            )

            ranked_candidates.append({

                "resume_path": resume_path,

                "final_score": final_score,

                "semantic_score": round(
                    semantic_score,
                    2
                ),

                "skills_score": round(skills_score, 2),

                "experience_score": round(
                    experience_score,
                    2
                ),

                "education_score": round(
                    education_score,
                    2
                ),

                "project_score": round(
                    project_score,
                    2
                ),

                "communication_score": round(
                    communication_score,
                    2
                ),

                "recommendation": recommendation,

                "matched_skills": matched_skills,

                "missing_skills": missing_skills,

                "analysis": analysis,

                "summary": summary,
            })

        except Exception as e:

            import traceback

            traceback.print_exc()

            # print("ERROR:", e)

    # SORT CANDIDATES
    ranked_candidates.sort(

        key=lambda x: x["final_score"],

        reverse=True
    )

    return {

        "success": True,

        "total_candidates": len(
            ranked_candidates
        ),

        "ranked_candidates": ranked_candidates
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