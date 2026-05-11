# llm.py
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def explain_recommendation(context, activity_name):
    # Simple explanation generation (static + context)
    explanation = f"This activity fits your energy level ({context['energy']}), time ({context['time_available']} mins), location ({context['location']})."
    if context.get("preferred_tags"):
        explanation += f" You wanted: {', '.join(context['preferred_tags'])}."
    return explanation

def generate_activity_from_input(prefer_tags, avoid_tags, time_available, username="default_user"):
    """
    Generate 1–2 activities using LLM based on prefer/avoid tags and user history
    """
    import models.feedback_score as fs
    history = fs.load_feedback_scores(username)
    liked_activities = [act_name for (moment, act_name), score in history.items() if score > 0]
    disliked_activities = [act_name for (moment, act_name), score in history.items() if score < 0]
    
    history_str = ""
    if liked_activities:
        history_str += f"User has liked: {', '.join(liked_activities[:5])}. "
    if disliked_activities:
        history_str += f"User has disliked: {', '.join(disliked_activities[:5])}. "
    
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"""
You are an AI assistant suggesting simple activities for {time_available} minutes.
The user wants activities related to: {prefer_tags}.
The user does NOT want activities related to: {avoid_tags}.
{history_str}
Return 2 activities ONLY in JSON array format:
[
    {{
        "name": "<activity_name>",
        "description": "<activity_description>",
        "works_for": ["general_free_time"],
        "tags": ["<tag1>", "<tag2>"]
    }}
]
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        activities = json.loads(text)
        return activities
    except Exception as e:
        # fallback static placeholder
        return [
            {"name": "Try something new", "description": f"Explore a random task for {time_available} minutes.", "works_for": ["general_free_time"], "tags": ["general"]}
        ]
