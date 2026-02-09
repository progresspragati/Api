# token_storage.py
import json
import os

TOKEN_FILE = "token.json"

def save_tokens(token_data):
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)

def load_tokens():
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, "r") as f:
        return json.load(f)