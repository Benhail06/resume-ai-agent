from pypdf import PdfReader

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

import os
import json
import re
from openai import OpenAI

from groq import Groq
import os

import streamlit as st
import os
import streamlit as st
from groq import Groq

try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)



def clean_json_response(response_text):
    import json
    import re

    # Remove markdown code blocks if present
    response_text = response_text.strip()

    if response_text.startswith("```"):
        response_text = re.sub(r"```json|```", "", response_text).strip()

    # Extract JSON object
    match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if match:
        json_str = match.group()
        try:
            return json_str
        except:
            pass

    # If still failing, print raw response for debugging
    print("RAW MODEL RESPONSE:\n", response_text)

    raise ValueError("No valid JSON found in response")


def extract_skills_from_text(text):

    prompt = f"""
You are an AI resume parser.

Extract the following:

1. Technical Skills (programming languages, frameworks, tools)
2. Soft Skills
3. Experience Level (junior/mid/senior estimate)
4. Primary Domain (AI, backend, data, etc.)

Return ONLY valid JSON in this exact format:

{{
  "technical_skills": [],
  "soft_skills": [],
  "experience_level": "",
  "primary_domain": ""
}}

Resume Text:
{text}
"""

    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)

    content = response.choices[0].message.content

    clean_json = clean_json_response(content)

    return json.loads(clean_json)

def extract_requirements_from_jd(jd_text):

    prompt = f"""
You are an AI job description analyzer.

Extract:

1. Required Technical Skills
2. Preferred Skills
3. Experience Level Required
4. Primary Domain

Return ONLY valid JSON in this format:

{{
  "required_skills": [],
  "preferred_skills": [],
  "experience_level_required": "",
  "primary_domain": ""
}}

Job Description:
{jd_text}
"""
    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)
    content = response.choices[0].message.content

    clean_json = clean_json_response(content)

    return json.loads(clean_json)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_skills, jd_required_skills):

    if not resume_skills or not jd_required_skills:
        return 0.0

    resume_skills = [s.lower() for s in resume_skills]
    jd_required_skills = [s.lower() for s in jd_required_skills]

    matched = 0

    for jd_skill in jd_required_skills:
        for resume_skill in resume_skills:
            if jd_skill in resume_skill or resume_skill in jd_skill:
                matched += 1
                break

    score = (matched / len(jd_required_skills)) * 100

    return round(score, 2)





def find_missing_skills(resume_skills, jd_required_skills):

    resume_set = set(skill.lower() for skill in resume_skills)
    jd_set = set(skill.lower() for skill in jd_required_skills)

    missing = jd_set - resume_set

    return list(missing)


def generate_recommendations(resume_data, jd_data, missing_skills):

    prompt = f"""
You are a career advisor.

Based on the following:

Resume Skills: {resume_data["technical_skills"]}
Required Skills: {jd_data["required_skills"]}
Missing Skills: {missing_skills}

Give:

1. Three improvement suggestions
2. Three learning recommendations
3. One short strategy paragraph

Keep response simple and clean.
Do not use JSON.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    content = response.choices[0].message.content

    return content



def generate_interview_questions(jd_data):

    prompt = f"""
You are a technical interviewer.

Based on this job requirement:

{jd_data["required_skills"]}

Generate 5 likely interview questions.

Return JSON:
{{
  "questions": []
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    content = response.choices[0].message.content
    try:
        clean_json = clean_json_response(content)
        return json.loads(clean_json)
    except:
    # Fallback: treat raw content as plain text list
        lines = content.split("\n")
        questions = [line.strip("- ").strip() for line in lines if len(line.strip()) > 10]

        return {
            "questions": questions[:5]
    }

