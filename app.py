# app.py - AI Business Idea Generator
from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

client = Groq(api_key="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")

def build_prompt(skills, budget, interest, experience, business_type):
    return f"""You are an expert business consultant and startup advisor.

A person wants to start a business with the following details:
- Skills: {skills}
- Interests/Passions: {interest}
- Available Budget: {budget}
- Experience Level: {experience}
- Preferred Business Type: {business_type}

Please suggest exactly 3 unique and practical business ideas tailored to this person.

For each idea use EXACTLY this format:

---
### Idea [number]: [Business Name]
**Business Type:** {business_type}
**Budget Required:** {budget}
**Difficulty Level:** [Easy / Medium / Hard]
**Monthly Income Potential:** [estimated range in INR]
**Time to First Income:** [e.g. 1-3 months]

**What is this business?**
[2-3 lines explaining the business idea clearly]

**Why it suits you?**
[Explain why this matches their skills, budget and interests]

**How to Start - Step by Step:**
1. [step]
2. [step]
3. [step]
4. [step]
5. [step]

**Tools / Resources Needed:**
- [tool or resource]
- [tool or resource]

**Pro Tips:**
- [practical tip to succeed]
- [practical tip to succeed]
---

Make ideas realistic, actionable, and specific to the Indian market. Be encouraging and motivating!
"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get-ideas", methods=["POST"])
def get_ideas():
    data = request.get_json()
    skills        = data.get("skills", "").strip()
    budget        = data.get("budget", "Low").strip()
    interest      = data.get("interest", "").strip()
    experience    = data.get("experience", "Beginner").strip()
    business_type = data.get("business_type", "Online").strip()

    if not skills:
        return jsonify({"error": "Please enter your skills!"}), 400
    if not interest:
        return jsonify({"error": "Please enter your interests!"}), 400

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": build_prompt(skills, budget, interest, experience, business_type)}],
            model="llama-3.3-70b-versatile",
            temperature=0.8,
            max_tokens=3000,
        )
        ideas_text = chat_completion.choices[0].message.content
        return jsonify({"ideas": ideas_text})
    except Exception as e:
        return jsonify({"error": f"AI error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
