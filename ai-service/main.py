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

app = FastAPI()                                                             # Creates the FastAPI server. 

limiter = Limiter(
    key_func=get_remote_address
)
app.state.limiter = limiter                                                 #Limiter Prevent abuse.

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],                                # Allows React frontend to call FastAPI.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "TalentLens AI Service Running"
    }


from pydantic import BaseModel

# REQUEST MODEL
class ResumeRequest(BaseModel):
    resume_paths: list[str]                                                # FastAPI automatically validates it.
    job_description: str

@limiter.limit("5/minute")                                    # 5 APIs Request per minute per IP Address


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
    jd_embedding = generate_embedding(                                     # Converts text into vectors.
        job_description
    )

    for resume_path in resume_paths:                                       # Processes every uploaded resume.
        try:
            # PARSE RESUME
            absolute_resume_path = os.path.abspath(                        # Python converts that relative path into an absolute path.
                f"../server/{resume_path}"
            )

            print("READING FILE:", absolute_resume_path)

            resume_text = parse_resume(                                    # Resume parsing i.e Reading document/PDF
                absolute_resume_path
            )

            # SANITIZE INPUTS
            resume_text = sanitize_input(                                  # Removes dangerous characters , it is Security layer , it Protects against prompt injection.
                resume_text
            )

            job_description = sanitize_input(
                job_description
            )

            # EXTRACT SKILLS                                               # It is extracting skills from skill_extractor.py
            resume_skills = extract_skills(
                resume_text
            )

            # MATCHED SKILLS
            matched_skills = list(                                         # It is matching skills from resume and JD which are common.
                set(resume_skills) &
                set(jd_skills)
            )

            # MISSING SKILLS
            missing_skills = list(                                         # Missing Skills , Therefore we use minus
                set(jd_skills) -
                set(resume_skills)
            )

            # RESUME EMBEDDING
            resume_embedding = generate_embedding(                         # Creates vector for resume.
                resume_text
            )

            # STORE VECTOR
            store_resume_embedding(                                        # Stores in Chroma DB
                candidate_id=resume_path,
                embedding=resume_embedding,
                resume_text=resume_text
            )

            # =========================
            # SEMANTIC SCORE
            # =========================
            semantic_score = calculate_similarity(
                resume_embedding,                                          # Compares vectors.
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
            ai_scores = ai_resume_scorer(                                  # This is the AI brain , Likely sends data to LLM.
                resume_text,                                               # It is doing job on the basis of ai_resume_scorer fucntion inside ai_scorer.py
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
                    (experience_score * 25) +                              # Since the weights add up to 100:
                    (education_score * 15) +
                    (project_score * 20) +
                    (communication_score * 10)
                ) / 10,
                2                                                          # 2 is round upto 87.5 means 87.50
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
            safe_resume_text = mask_sensitive_data(                       # john@gmail.com becomes ***@gmail.com
                resume_text
            )

            analysis = analyze_resume(
                safe_resume_text                                          # Generates detailed report.
            )


            #This is what react recieves
            ranked_candidates.append({
                "resume_path": resume_path,
                "final_score": final_score,
                "semantic_score": round(semantic_score,2),
                "skills_score": round(skills_score, 2),
                "experience_score": round(experience_score,2),
                "education_score": round(education_score,2),
                "project_score": round(project_score,2),
                "communication_score": round(communication_score,2),

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

    return {                                                               # Response sent to React:
        "success": True,
        "total_candidates": len(ranked_candidates),
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