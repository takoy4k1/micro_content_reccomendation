# llm_activity_generator.py
import json
import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")

def generate_ai_activities(context, avoid, prefer, n=3):
    prompt = f"""
Generate {n} realistic human activities.

Context:
Time: {context['time_of_day']}
Energy: {context['energy']}
Location: {context['location']}
Time available: {context['time_available']} minutes

Avoid: {avoid}
Prefer: {prefer}

Return JSON list with:
name, description, tags, works_for
"""

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    try:
        return json.loads(response.text)
    except:
        return []
