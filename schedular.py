import schedule
import time
from token_client import call_api
from email_sender import send_email

def job():
    response = call_api()
    if response.status_code != 200:
        send_email(
            "API Error",
            f"API failed with status {response.status_code}\n\n{response.text}"
        )
        return
    data = response.json()
    profile = data.get("data", {})

    balance = profile.get("balance", "N/A")

    print(data["data"]["balance"]) 

    email_body = f"""
Reseller Profile Summary
Provider    : "Esimfx"
Balance : {balance}
"""
    send_email(
        "Scheduled Reseller Profile",
        email_body
    )

schedule.every().day.at("18:10").do(job)

print("Scheduler started...")

while True:
    schedule.run_pending()
    time.sleep(60)
