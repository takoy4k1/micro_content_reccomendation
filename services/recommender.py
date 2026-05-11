# recommender.py

from activities import recommend_activities

def get_recommendations(moment_type, last_activity=None):
    return recommend_activities(moment_type, last_activity)
