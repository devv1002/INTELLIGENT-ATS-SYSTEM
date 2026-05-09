import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_resume(resume_text):

    prompt = f"""
    You are an expert ATS AI recruiter.

    Analyze this resume according to the following hiring rubric.

    Give output in this EXACT format:

    1. Candidate Summary

    2. Skills Match Evaluation (/10)
    - Give score
    - Give one-line justification

    3. Experience Relevance Evaluation (/10)
    - Give score
    - Give one-line justification

    4. Education & Certifications Evaluation (/10)
    - Give score
    - Give one-line justification

    5. Project / Portfolio Evaluation (/10)
    - Give score
    - Give one-line justification

    6. Communication Quality Evaluation (/10)
    - Give score
    - Give one-line justification

    7. Strengths

    8. Weaknesses

    9. Recommended Job Roles

    10. Missing Skills / Improvements

    11. Final Hiring Recommendation
    - SHORTLIST / HOLD / REJECT

    IMPORTANT:
    - Keep response ATS-style
    - Keep response concise
    - Do NOT generate markdown tables
    - Do NOT generate percentages
    - Do NOT generate weighted scores
    - Keep professional HR tone

    Resume:
    {resume_text}
    """

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content