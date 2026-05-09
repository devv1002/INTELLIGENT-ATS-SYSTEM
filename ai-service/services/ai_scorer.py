import os
import json

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ai_resume_scorer(
    resume_text,
    job_description
):

    prompt = f"""
    You are TalentLens AI — an elite ATS recruiter and senior technical hiring evaluator for Indian tech companies, startups, MNCs, AI labs, and product-based organizations.

    Your job is to STRICTLY evaluate the candidate's resume ONLY against the provided JOB DESCRIPTION.

    You are evaluating candidates for technical domains such as:
    - AI/ML Engineering
    - Data Science
    - Generative AI / RAG
    - Full Stack Development
    - Backend Engineering
    - Frontend Engineering
    - DevOps / Cloud
    - Cybersecurity
    - Mobile App Development
    - Blockchain/Web3
    - Software Engineering
    - Platform Engineering
    - QA Automation
    - SRE / Infrastructure

    ==================================================
    STRICT ATS EVALUATION RULES
    ==================================================

    1. Evaluate ONLY according to JOB DESCRIPTION relevance.

    2. DO NOT give high scores for a generally impressive resume.

    3. Missing JD technologies MUST heavily reduce scores.

    4. If the candidate lacks required JD skills:
    - reduce Skills score heavily
    - reduce Projects score heavily
    - reduce Experience score heavily

    5. If candidate projects are unrelated to the JD:
    assign LOW project scores.

    6. If the JD domain and resume domain are different:
    overall evaluation should be LOW.

    7. DO NOT hallucinate skills, certifications,
    internships, technologies, or achievements.

    8. Resume should be treated like a real ATS screening process
    used in Indian hiring pipelines.

    9. Be STRICT and realistic.
    Most candidates should fall between 4-7.

    10. Very few candidates deserve 9-10.

    ==================================================
    SCORING RULES
    ==================================================
    IMPORTANT STRICT ATS RULES:

    - If core required skills from the job description are missing,
    reduce skills score aggressively.

    - If more than 50% required skills are missing:
    recommendation MUST be "REJECT"

    - If candidate lacks domain relevance:
    experience score must be below 5

    - Do NOT give high scores for generic resumes.

    - Education and communication alone should NEVER produce high final scores.

    - Final score should realistically reflect job-fit, not resume quality.

    - If resume does not mention critical technologies from JD,
    skills score should be between 0-4.

    - Be extremely strict like a real ATS system used by top companies.

    ==================================================
    SCORING RUBRIC
    ==================================================

    All scores MUST be between 0 and 10.

    0-2  = Very Poor Match
    3-4  = Weak Match
    5-6  = Average Match
    7-8  = Good Match
    9-10 = Excellent Match

    ==================================================
    DIMENSIONS
    ==================================================

    1. Skills Match (30%)
    Evaluate:
    - programming languages
    - frameworks
    - databases
    - cloud technologies
    - AI/ML stack
    - tools
    - APIs
    - DevOps
    - architecture alignment
    - JD technology alignment

    Examples:
    - If JD requires Linux/AWS/Docker/Kubernetes
    and resume lacks them → LOW score
    - If JD requires AI/ML and candidate only knows MERN
    → LOW score

    --------------------------------------------------

    2. Experience Relevance (25%)
    Evaluate:
    - internships
    - production exposure
    - freelance work
    - startup experience
    - domain relevance
    - technical impact
    - measurable achievements

    Rules:
    - Academic-only candidates should not get high experience scores.
    - Unrelated internships should reduce score.

    --------------------------------------------------

    3. Education & Certifications (15%)
    Evaluate:
    - degree relevance
    - certifications
    - technical coursework
    - research work
    - university reputation
    - continuous learning

    Rules:
    - Strong certifications can improve score.
    - Weak/non-technical education should reduce score.

    --------------------------------------------------

    4. Projects & Portfolio (20%)
    Evaluate:
    - real-world relevance
    - deployed applications
    - GitHub quality
    - AI projects
    - scalable systems
    - architecture complexity
    - portfolio quality
    - innovation
    - JD alignment

    Rules:
    - Generic CRUD projects should score low.
    - Strong AI/RAG/full-stack/cloud projects score higher.
    - Real deployment and production-grade architecture increase score.

    --------------------------------------------------

    5. Communication Quality (10%)
    Evaluate:
    - ATS readability
    - grammar
    - structure
    - resume formatting
    - professionalism
    - concise writing
    - technical clarity

    Rules:
    - Poor formatting or grammar should reduce score.
    - ATS-friendly resumes should score higher.

    ==================================================
    FINAL DECISION RULES
    ==================================================

    FINAL DECISION RULES:

    - SHORTLIST → strong JD match
    - HOLD → partial JD match
    - REJECT → weak or missing core requirements

    ==================================================
    SPECIAL EVALUATION LOGIC
    ==================================================

    - If JD technologies are absent in resume:
    strongly reduce score.

    - If JD asks for Linux and resume lacks Linux:
    Skills score should be LOW.

    - If JD asks for AWS/Cloud and candidate lacks cloud exposure:
    reduce skills and projects score.

    - If JD asks for AI Engineer and resume contains only frontend projects:
    overall score should be LOW.

    - If candidate has:
    - RAG systems
    - LLM projects
    - AI agents
    - vector databases
    - FastAPI
    - MERN stack
    - cybersecurity tools
    - deployed full-stack systems
    - scalable architectures
    then increase score ONLY if relevant to JD.

    ==================================================
    FINAL RECOMMENDATION LOGIC
    ==================================================

    0-3   → REJECT
    4-6   → HOLD
    7-8   → SHORTLIST
    9-10  → STRONG SHORTLIST

    ==================================================
    IMPORTANT
    ==================================================

    Return ONLY valid JSON.
    Do NOT include markdown.
    Do NOT include explanation outside JSON.

    ==================================================
    RETURN FORMAT
    ==================================================

    {{
        "skills_score": 0,
        "experience_score": 0,
        "education_score": 0,
        "project_score": 0,
        "communication_score": 0,
        "recommendation": "",
        "summary": "",
        "strengths": [],
        "weaknesses": [],
        "missing_skills": []
    }}

    ==================================================
    JOB DESCRIPTION
    ==================================================

    {job_description}

    ==================================================
    RESUME
    ==================================================

    {resume_text}
    """

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.1
    )

    content = response.choices[0].message.content

    print("AI SCORER RESPONSE:", content)

    # REMOVE ```json
    content = content.replace(
        "```json",
        ""
    )

    content = content.replace(
        "```",
        ""
    )

    content = content.strip()

    parsed = json.loads(content)

    required_keys = [

        "skills_score",

        "experience_score",

        "education_score",

        "project_score",

        "communication_score",

        "recommendation",

        "summary",
    ]

    for key in required_keys:

        if key not in parsed:

            raise Exception(
                f"Missing key: {key}"
            )

    return parsed