import os
import json
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import PyPDF2

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# 📄 Extract text from PDF
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


# 🤖 Resume Analysis
@st.cache_data(show_spinner=False)
def analyze_resume(text):

    prompt = f"""
    You are an expert ATS resume analyzer.

    Analyze the resume and return ONLY valid JSON.

    Rules:
    - Score between 0 and 10
    - No markdown
    - Short points

    Format:
    {{
      "score": number,
      "strengths": ["point1", "point2"],
      "weaknesses": ["point1", "point2"],
      "suggestions": ["point1", "point2"],
      "roles": ["role1", "role2"]
    }}

    Resume:
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    result = response.choices[0].message.content.strip()

    # 🔥 clean markdown if present
    if result.startswith("```"):
        result = result.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(result)

        # 🔥 FIX SCORE RANGE
        data["score"] = float(data.get("score", 0))
        data["score"] = max(0, min(10, data["score"]))

        return data

    except:
        return {
            "score": 0,
            "strengths": ["Error parsing response"],
            "weaknesses": [],
            "suggestions": ["Try again"],
            "roles": []
        }


# 🎯 Job Match
@st.cache_data(show_spinner=False)
def match_resume_with_jd(resume_text, jd_text):

    prompt = f"""
    Match resume with job description.

    Return ONLY JSON.

    Format:
    {{
      "match_score": number,
      "missing_skills": ["skill1", "skill2"],
      "improvement_tips": ["tip1", "tip2"]
    }}

    Resume:
    {resume_text}

    Job Description:
    {jd_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    result = response.choices[0].message.content.strip()

    if result.startswith("```"):
        result = result.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(result)

        data["match_score"] = float(data.get("match_score", 0))
        data["match_score"] = max(0, min(100, data["match_score"]))

        return data

    except:
        return {
            "match_score": 0,
            "missing_skills": [],
            "improvement_tips": []
        }