# activities.py
import random
import json
import os
from services.llm import generate_activity_from_input  # New helper to call LLM

# Load activities from dataset
DATASET_FILE = "activities_dataset.json"
if os.path.exists(DATASET_FILE):
    with open(DATASET_FILE, "r") as f:
        activities = json.load(f)
else:
    activities = []  # Fallback if file missing

# =========================
# RECOMMENDATION ENGINE
# =========================

def recommend_activities(moment_type, time_available=20, avoid_tags=None, prefer_tags=None, last_activity=None, username="default_user"):
    avoid_tags = avoid_tags or []
    prefer_tags = prefer_tags or []
    
    # Get candidate activities for the moment
    candidates = [act for act in activities if moment_type in act["works_for"]]
    # Filter by tags
    candidates = [act for act in candidates if not any(tag in act.get("tags", []) for tag in avoid_tags)]
    if prefer_tags:
        candidates = [act for act in candidates if any(tag in act.get("tags", []) for tag in prefer_tags)] or candidates  # Boost preferred, but don't exclude if none match
    
    # Avoid repeating last activity
    if last_activity:
        candidates = [act for act in candidates if act["name"] != last_activity]
    
    if not candidates:
        # Fallback to LLM
        new_activities = generate_activity_from_input(prefer_tags, avoid_tags, time_available)
        candidates = new_activities
    
    # Use Thompson Sampling to score and select top 3
    import models.feedback_store as fb
    scores = fb.sample_scores(username, candidates)
    scored = []
    for act in candidates:
        base_score = scores.get(act["name"], 0.5)
        # Hybrid: Boost score if preferred tags match
        boost = 0.2 if prefer_tags and any(tag in act.get("tags", []) for tag in prefer_tags) else 0
        final_score = base_score + boost
        scored.append((final_score, act))
    
    scored.sort(key=lambda x: x[0], reverse=True)
    
    results = [act for _, act in scored[:3]]
    
    # FALLBACK to LLM generation if no matches
    if len(results) < 3:
        new_activities = generate_activity_from_input(prefer_tags, avoid_tags, time_available, username)
        results.extend(new_activities[:3-len(results)])
    
    return results
