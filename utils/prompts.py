def resume_analysis_prompt(resume_text):

    return f"""
Analyze the following resume professionally.

Return ONLY valid JSON.

Format:

{{
    "score": number,
    "summary": "short summary",
    "strengths": [],
    "weaknesses": [],
    "suggestions": [],
    "recommended_roles": []
}}

Resume:
{resume_text}
"""