import requests
from token_storage import load_tokens
from auth_esimfx import login_and_get_token
import time
from email_sender import send_email

API_URL = "https://api.esimfx.com/account/api/v1/reseller/get_profile"

def call_api():
    token_data = load_tokens("esimfx")

    # No token yet → login
    if not token_data:
        login_and_get_token()
        token_data = load_tokens("esimfx")

    headers = {
        "Authorization": f"Bearer {token_data['access_token']}",
        "Accept": "application/json"
    }

    response = requests.get(API_URL, headers=headers, timeout=10)

    # Token expired → login again
    if response.status_code in (401, 403):
        login_and_get_token()
        token_data = load_tokens("esimfx")

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