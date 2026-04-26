# AI Talent Scouting & Engagement Agent

## Overview
This project is an AI-powered recruitment agent that:
- Parses job descriptions
- Matches candidates based on skills and experience
- Simulates candidate interest
- Produces a ranked shortlist

## Features
- JD parsing using regex
- Skill + experience-based scoring
- Simulated conversational interest
- Final ranking with explainability

## Tech Stack
- Python
- Streamlit

## How to Run

1. Install dependencies:
pip install -r requirements.txt

2. Run app:
streamlit run app.py

## Sample Input
"We need a Python developer with 2+ years experience in SQL and APIs"

## Output
Ranked candidates with:
- Match Score
- Interest Score
- Final Score

## Architecture
JD Input → Parser → Candidate Matching → Interest Simulation → Ranking → UI

## Trade-offs
- Used rule-based scoring for speed and explainability
- Simulated conversation instead of real API calls due to free-tier constraints
