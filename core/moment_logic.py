import json
from services.gemini_client import model

ALLOWED_MOMENTS = [
    "low_energy_evening",
    "high_energy_morning",
    "tired_afternoon",
    "commute_mode",
    "calm_night",
    "general_free_time"
]

def get_moment_type(time_of_day, energy_level, location):
    time_of_day = time_of_day.lower()
    energy_level = energy_level.lower()
    location = location.lower()

    if energy_level == "low" and time_of_day in ["evening", "night"]:
        return "low_energy_evening"
    if energy_level == "high" and time_of_day == "morning":
        return "high_energy_morning"
    if location == "commute":
        return "commute_mode"
    if energy_level == "low" and time_of_day == "afternoon":
        return "tired_afternoon"
    if energy_level == "medium" and time_of_day == "night":
        return "calm_night"
    return "general_free_time"


def ai_get_moment_type(time_of_day, energy_level, location):
    prompt = f"""
You are an AI system that classifies a user's current micro-context.

Inputs:
- Time of day: {time_of_day}
- Energy level: {energy_level}
- Location: {location}

Choose ONE value from:
{ALLOWED_MOMENTS}

Respond ONLY in valid JSON:
{{"moment_type": "<value>"}}
"""

    try:
        response = model.generate_content(prompt)
        data = json.loads(response.text.strip())
        moment = data.get("moment_type", "general_free_time")
        if moment in ALLOWED_MOMENTS:
            return moment
        return "general_free_time"
    except Exception:
        return "general_free_time"


def explain_decision(moment_type):
    explanations = {
        "low_energy_evening":
            "User is likely mentally fatigued; low-stimulation, comforting actions are optimal.",
        "high_energy_morning":
            "User has high focus and motivation; challenging or creative tasks are suitable.",
        "tired_afternoon":
            "Attention is limited; low-effort progress helps avoid burnout.",
        "commute_mode":
            "User is mobile; passive or audio-based activities fit best.",
        "calm_night":
            "User is winding down; reflective or planning activities are effective.",
        "general_free_time":
            "No strong constraints detected; flexible actions are recommended."
    }
    return explanations.get(moment_type, "")
