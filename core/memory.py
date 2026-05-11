# memory.py
_last_activities = {}

def get_last_activity(username):
    return _last_activities.get(username)

def save_last_activity(username, activity):
    _last_activities[username] = activity
