import requests
from token_storage import save_tokens
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("API_CLIENT_ID")
CLIENT_KEY = os.getenv("API_CLIENT_KEY")

LOGIN_URL = "https://api.esimfx.com/account/api/v1/auth"

def login_and_get_token():
    payload = {
      "client_id": CLIENT_ID,
      "client_key": CLIENT_KEY
    }
    
    response = requests.post(LOGIN_URL, json=payload, timeout = 10)
    
    if response.status_code != 200:
            raise Exception("Login failed. Check credentials.")
    
    data = response.json()
    print("LOGIN RESPONSE:", data)
    save_tokens("esimfx",{
        "access_token": data["data"]["access_token"],
    })
    
if __name__ == "__main__":
    login_and_get_token()