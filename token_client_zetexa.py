import requests
from token_storage import load_tokens
from auth_zetexa import login_and_get_token
import time
from email_sender import send_email
from dotenv import load_dotenv
import os

API_URL = "https://api.zetexa.com/v1/Reseller-Balance"
load_dotenv()
CLIENT_API_KEY = os.getenv("CLIENT_API_KEY")

def call_api():
    token_data = load_tokens("zetexa")

    # No token yet → login
    if not token_data:
        login_and_get_token()
        token_data = load_tokens("zetexa")

    headers = {
        "AccessToken": CLIENT_API_KEY,
        "Authorization": f"Bearer {token_data['access_token']}",
        "Accept": "application/json"
    }

    response = requests.post(API_URL, headers=headers, timeout=10)

    # Token expired → login again
    if response.status_code in (401, 403):
        login_and_get_token()
        token_data = load_tokens("zetexa")

        headers["Authorization"] = f"Bearer {token_data['access_token']}"
        response = requests.get(API_URL, headers=headers, timeout=10)

    return response

if __name__ == "__main__":
    response = call_api()
    print(response.status_code)
    print(response.text)

    subject = "API Response: Reseller Profile"
    body = f"""
Status Code: {response.status_code}

Response Body:
{response.text}
"""

    send_email(subject, body)

    print("Email sent successfully")