# feedback_store.py
from collections import defaultdict
import models.feedback_score as fs
import numpy as np

# Store beta params: {username: {activity: (alpha, beta)}}
_beta_params = defaultdict(lambda: defaultdict(lambda: (1, 1)))  # Default: alpha=1, beta=1 (uniform prior)

def give_feedback(username, moment, activity, liked=True):
    reward = 1 if liked else 0  # Binary reward for bandit
    alpha, beta = _beta_params[username][activity]
    if liked:
        alpha += 1
    else:
        beta += 1
    _beta_params[username][activity] = (alpha, beta)
    fs.save_feedback_beta(username, activity, alpha, beta)

def get_beta_params(username):
    # Load from file if not in memory
    if not _beta_params[username]:
        _beta_params[username] = fs.load_beta_params(username)
    return dict(_beta_params[username])

def sample_scores(username, activities):
    params = get_beta_params(username)
    scores = {}
    for act in activities:
        alpha, beta = params.get(act["name"], (1, 1))
        # Sample from beta distribution
        scores[act["name"]] = np.random.beta(alpha, beta)
    return scores
