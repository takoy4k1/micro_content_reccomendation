import sqlite3
import os
from datetime import datetime
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, "feedback.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    username TEXT,
                    moment_type TEXT,
                    activity TEXT,
                    feedback INTEGER
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS beta_params (
                    username TEXT,
                    activity TEXT,
                    alpha REAL,
                    beta REAL,
                    PRIMARY KEY (username, activity)
                )''')
    conn.commit()
    conn.close()

init_db()

def save_feedback(username, moment_type, activity_name, feedback):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO feedback (timestamp, username, moment_type, activity, feedback) VALUES (?, ?, ?, ?, ?)",
              (datetime.now().isoformat(), username, moment_type, activity_name, 1 if feedback else 0))
    conn.commit()
    conn.close()

def load_feedback_scores(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT moment_type, activity, feedback FROM feedback WHERE username = ?", (username,))
    rows = c.fetchall()
    conn.close()
    scores = {}
    for moment, activity, fb in rows:
        key = (moment, activity)
        scores[key] = scores.get(key, 0) + (1 if fb else -1)
    return scores

def save_feedback_beta(username, activity, alpha, beta):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO beta_params (username, activity, alpha, beta) VALUES (?, ?, ?, ?)",
              (username, activity, alpha, beta))
    conn.commit()
    conn.close()

def load_beta_params(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT activity, alpha, beta FROM beta_params WHERE username = ?", (username,))
    rows = c.fetchall()
    conn.close()
    params = defaultdict(lambda: (1, 1))
    for activity, alpha, beta in rows:
        params[activity] = (alpha, beta)
    return params
