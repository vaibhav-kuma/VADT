import json
import os

def load_attack_categories(path=None):
    if path is None:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_dir, "rules", "attack_categories.json")
    with open(path, "r") as f:
        return json.load(f)

def detect_attack_type(cmdline, categories):
    matches = []
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in cmdline.lower():
                matches.append(category)
                break  # One match is enough per category
    return matches or ["Unknown"]
