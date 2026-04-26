import streamlit as st
import json
import re
import os

# -------- LOAD DATA --------
file_path = os.path.join(os.path.dirname(__file__), "candidates.json")

with open(file_path, "r") as f:
    candidates = json.load(f)

# -------- JD PARSER --------
def parse_jd(jd_text):
    common_skills = [
        "Python", "SQL", "Java", "React", "Node.js",
        "Machine Learning", "APIs", "Pandas", "Django"
    ]

    jd_lower = jd_text.lower()

    skills = [skill for skill in common_skills if skill.lower() in jd_lower]

    exp_match = re.search(r'(\d+)\+?\s*years?', jd_text.lower())
    experience = int(exp_match.group(1)) if exp_match else 0

    return skills, experience

# -------- MATCH SCORE --------
def calculate_match_score(jd_skills, jd_exp, candidate):
    if len(jd_skills) == 0:
        return 0, 0

    overlap = len(set(jd_skills).intersection(set(candidate["skills"])))
    skill_score = (overlap / len(jd_skills)) * 100
    exp_score = min(candidate["experience"] / max(jd_exp, 1), 1) * 100

    match_score = 0.7 * skill_score + 0.3 * exp_score
    return round(match_score, 2), overlap

# -------- RULE-BASED INTEREST (NO AI) --------
def simulate_interest(jd_skills, candidate, overlap):
    
    total_skills = len(jd_skills)

    if total_skills == 0:
        return "No", 0, "No skills matched", "Not interested"

    match_ratio = overlap / total_skills

    # Interest logic
    if match_ratio >= 0.75:
        interest = "Yes"
        score = 85
        reason = "Strong skill match"
        message = "This role aligns well with my experience. I'm interested."

    elif match_ratio >= 0.5:
        interest = "Yes"
        score = 65
        reason = "Partial match"
        message = "I have relevant experience and would consider this opportunity."

    elif match_ratio >= 0.25:
        interest = "No"
        score = 40
        reason = "Limited match"
        message = "Some skills match, but not a strong fit for me."

    else:
        interest = "No"
        score = 20
        reason = "Poor match"
        message = "This role does not match my current skill set."

    return interest, score, reason, message

# -------- UI --------
st.title("🤖 AI Talent Scouting & Engagement Agent")

jd_input = st.text_area("Enter Job Description:")

if st.button("Run Agent"):

    jd_skills, jd_exp = parse_jd(jd_input)

    results = []

    for c in candidates:
        match_score, overlap = calculate_match_score(jd_skills, jd_exp, c)

        interest, interest_score, reason, message = simulate_interest(jd_skills, c, overlap)

        final_score = round(0.6 * match_score + 0.4 * interest_score, 2)

        results.append({
            "Name": c["name"],
            "Match Score": match_score,
            "Interest Score": interest_score,
            "Final Score": final_score,
            "Interest": interest,
            "Skill Match": f"{overlap}/{len(jd_skills)}",
            "Explanation": f"{reason}, Exp: {c['experience']} yrs",
            "Candidate Reply": message
        })

    results = sorted(results, key=lambda x: x["Final Score"], reverse=True)

    st.success(f"🏆 Top Candidate: {results[0]['Name']}")

    st.subheader("📊 Ranked Candidates")
    st.table(results)

    st.subheader("🔍 JD Insights")
    st.write(f"Extracted Skills: {jd_skills}")
    st.write(f"Required Experience: {jd_exp} years")