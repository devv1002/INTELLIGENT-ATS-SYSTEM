import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_resume(resume_text):

    prompt = f"""
    Analyze this resume professionally.

    Give:
    1. Candidate Summary
    2. Technical Skills
    3. Strengths
    4. Weaknesses
    5. Suitability Score out of 100

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