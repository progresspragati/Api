import schedule
import time
from token_client_esimfx import call_api as call_esimfx
from token_client_zetexa import call_api as call_zetexa
from email_sender import send_email

def job():

    email_body = "Reseller Balance Summary\n\n"

    # --------------------
    # ESIMFX
    # --------------------
    try:
        esimfx_response = call_esimfx()

        if esimfx_response.status_code == 200:
            data = esimfx_response.json()
            balance = data.get("data", {}).get("balance", "N/A")
            try:
                balance_value = float(balance)
                if balance_value < 10:
                    balance = f"{balance_value}  ⚠️ LOW BALANCE"
            except:
                balance = "Invalid balance format"
        else:
            balance = f"API Error ({esimfx_response.status_code})"

    except Exception as e:
        balance = f"Error: {str(e)}"

    email_body += f"Provider : Esimfx\nBalance  : {balance}\n\n"


    # --------------------
    # ZETEXA
    # --------------------
    try:
        zetexa_response = call_zetexa()

        if zetexa_response.status_code == 200:
            data = zetexa_response.json()
            balance = data.get("balance", "N/A")
            try:
                balance_value = float(balance)
                if balance_value < 10:
                    balance = f"{balance_value}  ⚠️ LOW BALANCE"
            except:
                balance = "Invalid balance format"
        else:
            balance = f"API Error ({zetexa_response.status_code})"

    except Exception as e:
        balance = f"Error: {str(e)}"

    email_body += f"Provider : Zetexa\nBalance  : {balance}\n\n"


    send_email("Daily Reseller Balance", email_body)
schedule.every().day.at("10:45").do(job)

print("Scheduler started...")

while True:
    schedule.run_pending()
    time.sleep(60)
