import json
import os

TOKEN_FILE = "token.json"

def save_tokens(provider, token_data):
    # Load existing tokens if file exists
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            try:
                all_tokens = json.load(f)
            except json.JSONDecodeError:
                all_tokens = {}
    else:
        all_tokens = {}

    # Update only this provider
    all_tokens[provider] = token_data

    # Save back
    with open(TOKEN_FILE, "w") as f:
        json.dump(all_tokens, f, indent=4)


def load_tokens(provider):
    if not os.path.exists(TOKEN_FILE):
        return None

    with open(TOKEN_FILE, "r") as f:
        all_tokens = json.load(f)

    return all_tokens.get(provider)
