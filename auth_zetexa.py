import requests
from token_storage import save_tokens
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
CLIENT_API_KEY = os.getenv("CLIENT_API_KEY")

LOGIN_URL = "https://api.zetexa.com/v1/Create-Token"

def login_and_get_token():
    Headers = {
        "AccessToken": CLIENT_API_KEY
    }

    payload = {
      "email": EMAIL,
      "password": PASSWORD
    }
    
    response = requests.post(LOGIN_URL, headers = Headers, json=payload, timeout = 10)
    
    data = response.json()

    if not data.get("success"):
        raise Exception(f"Login failed: {data}")

    token = data.get("session_token")

    if not token:
        raise Exception("Token missing in response")

    save_tokens("zetexa", {
        "access_token": token
    })
    print("Zetexa token saved successfully")

if __name__ == "__main__":
    login_and_get_token()