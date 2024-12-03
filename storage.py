import os
import json
from transformers import pipeline

def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

def load_history(token, section):
    history_file = f"history_{token}_{section}.json"
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            history_data = json.load(f)
            return history_data.get("history", []), history_data.get("title")
    return [], None

def save_history(token, history, section, title=None):
    history_file = f"history_{token}_{section}.json"
    with open(history_file, "w") as f:
        json.dump({"history": history, "title": title}, f)

summarizer = pipeline("summarization")

def generate_title(first_turn):
    return summarizer(first_turn, max_length=30, min_length=10, do_sample=False)[0]['summary_text']

def format_history(history_json, username="You"):
    formatted_text = ""
    history = json.loads(history_json)
    if history:
        for turn in history:
            formatted_text += f"{username}: {turn['user']}\n"
            formatted_text += f"PlaygroundAI: {turn['bot']}\n\n"
    else:
        formatted_text = "No history found for this section."
    return formatted_text