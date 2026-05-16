import json

from services.openai_service import get_ai_response
from utils.prompts import resume_analysis_prompt

def analyze_resume(resume_text):

    prompt = resume_analysis_prompt(resume_text)

    result = get_ai_response(prompt)

    try:

        cleaned = result.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        )

        data = json.loads(cleaned)

        score = float(data.get("score", 0))

        # FIX SCORE
        if score > 10:
            score = score / 10

        data["score"] = round(score, 1)

        return data

    except:

        return {

            "score": 0,

            "summary": "Error parsing AI response",

            "strengths": [],

            "weaknesses": [],

            "suggestions": [],

            "recommended_roles": []
        }